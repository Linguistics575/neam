import os

from flask import render_template, request, send_from_directory, jsonify, url_for, Markup
from markdown import markdown

from neam.python.app import app, celery, neam_annotate


FILE_DIR = os.path.dirname(os.path.realpath(__file__))


@app.route('/')
@app.route('/index')
def index():
    """ Routes the user to the index page """
    return render_template('index.html', title='NEAM Annotate')


@app.route('/about')
def about():
    """ Routes the user to the about page """
    with open(os.path.join(FILE_DIR, '..', '..', '..', 'docs', 'about.md')) as one_pager:
        content = '\n'.join(one_pager.readlines())
    return render_template('about.html', title='About NEAM', content=Markup(markdown(content)))


@app.route('/annotate', methods=['POST'])
def annotate():
    """
    Annotates a document

    TODO: Add validation

    :return: An HTTP response, where the Location key corresponds to the URI to check on
             the annotation process
    """
    # Grab the data from the request
    email = request.form['email']
    f = request.files['file']
    form = {**request.form}
    for k in form:
        if isinstance(form[k], list):
            form[k] = '\n'.join(form[k])
    form['filename'] = f.filename

    # Save the file so the worker can find it
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

    # Fire off a worker to annotate the file
    t = neam_annotate.delay(f.filename, form)

    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=t.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    """
    Checks on the status of a worker

    :param task_id: The ID of the worker
    :type task_id: str
    :return: The status of the worker
    """
    # Find the task
    # TODO: handle invalid queries
    task = neam_annotate.AsyncResult(task_id)

    # Set the values on a response object
    response = { 'state': task.state }
    if task.state == 'PENDING':
        response['status'] = 'Pending'
    elif task.state != 'FAILURE':
        response['status'] = task.info.get('status', '')
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response['status'] = str(task.info)

    return jsonify(response)


@app.route('/download/<filename>')
def download(filename):
    """
    Downloads a file from the server

    TODO: validate the input

    :param filename: The name of the file to download
    :return: The requested file
    """
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename, as_attachment=True)

