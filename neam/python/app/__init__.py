import os
import re

from flask import Flask
from celery import Celery
from jinja2 import Template

from neam.python.neam import neam


FILE_DIR = os.path.dirname(os.path.realpath(__file__))


def make_celery(app):
    """
    Initializes Celery for Flask

    :param app: A Flask application
    :return: A Celery instance
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# Initialize the application and configure it
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/'
app.config['CELERY_BROKER_URL'] = os.environ['REDIS_URL'] if 'REDIS_URL' in os.environ else 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = os.environ['REDIS_URL'] if 'REDIS_URL' in os.environ else 'redis://localhost:6379/0'

celery = make_celery(app)


@celery.task(bind=True)
def neam_annotate(self, filename, form):
    """
    Annotates a document with NEAM

    TODO: Ensure the file exists

    :param filename: The name of the file to annotate
    :param email: The data provided to the HTML form
    :return: A response object that has as its result the name of the annotated file
    """
    new_file = filename + '.xml'
    tab_width = 2
    tab_str = '  '
    tab = tab_str * tab_width

    self.update_state(state='PROGRESS', meta={})

    # Annotate the file
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
        form['body'] = tab_str + re.sub('\n', '\n' + tab_str, neam(f))

    # Embed the file inside a TEI document
    with open(os.path.join(FILE_DIR, 'templates', 'tei.xml')) as template_file:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], new_file), 'w') as out:
            template = Template(''.join(template_file.readlines()))
            out.write(template.render(**form))

    if form['email']:
        # TODO: implement email functionality
        pass

    return {'result': new_file}


from neam.python.app import routes

