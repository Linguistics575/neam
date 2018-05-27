from flask import Flask
from celery import Celery
import os


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
def neam_annotate(self, filename, email):
    """
    Annotates a document with NEAM

    TODO: Ensure the file exists

    :param filename: The name of the file to annotate
    :param email: An email to send the annotated file to
    :return: A response object that has as its result the name of the annotated file
    """
    new_file = filename + '.xml'

    self.update_state(state='PROGRESS', meta={})
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
        from neam.python.neam import neam
        with open(os.path.join(app.config['UPLOAD_FOLDER'], new_file), 'w') as out:
            out.write(neam(f))

    return {'result': new_file}


from neam.python.app import routes

