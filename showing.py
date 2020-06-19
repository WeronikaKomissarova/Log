import logging
import os
from render import RenderFile
import pandas as pd

from flask import render_template, request, session, make_response, Flask, url_for, redirect
from werkzeug.utils import secure_filename


EXTENSIONS = ['.log']
app = Flask(__name__)
app.config['SECRET_KEY']='some secret key'
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), 'uploads')

log = logging.getLogger('pydrop')


def allow_file(filename):
    _, ext = os.path.splitext(filename)
    return ext in EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           page_name='Main',
                           project_name="pydrop")


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['file']
    if allow_file(file.filename):

        save_path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

        # If the file already exists it's ok if we are appending to it,
        # but not if it's new file that would overwrite the existing one
        if os.path.exists(save_path) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('File already exists', 400))

        try:
            with open(save_path, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
        except OSError:
            # log.exception will include the traceback so we can see what's wrong
            log.exception('Could not write to file')
            return make_response(("Not sure why,"
                                  " but we couldn't write the file to disk", 500))

        total_chunks = int(request.form['dztotalchunkcount'])

        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                log.error(f"File {file.filename} was completed, "
                          f"but has a size mismatch."
                          f"Was {os.path.getsize(save_path)} but we"
                          f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                log.info(f'File {file.filename} has been uploaded successfully')
        else:
            log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
                      f'for file {file.filename} complete')

        name='uploads\%s.pkl' %str(file.filename).split('.')[0]
        RenderFile(save_path).file_to_dataframe().to_pickle(name)
        os.remove(save_path)
        session['file']=os.path.join(os.getcwd(),name)
        return make_response(("Chunk upload successful", 200))
    else:
        return make_response(('Invalid file extension', 300))


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    df=pd.read_pickle(session['file'])
    file = df.to_html(os.path.join(os.getcwd(),'templates/file.html'))

    return render_template('downloads.html', html_file='file.html'

                           )


if __name__ == '__main__':
    app.run()
