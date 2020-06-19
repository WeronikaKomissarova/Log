import logging
import os
from render import RenderFile

from flask import render_template, Blueprint, request, make_response, Flask, url_for, redirect
from werkzeug.utils import secure_filename

EXTENSIONS = ['.log']

blueprint = Blueprint('templated', __name__, template_folder='templates')

log = logging.getLogger('pydrop')
def allow_file(filename):
    _,ext=os.path.splitext(filename)
    return ext in EXTENSIONS


@blueprint.route('/')
@blueprint.route('/index')
def index():
    # Route to serve the upload form
    return render_template('index.html',
                           page_name='Main',
                           project_name="pydrop")


@blueprint.route('/upload', methods=['GET','POST'])
def upload():
    file = request.files['file']
    if allow_file(file.filename):

        save_path = os.path.join(os.getcwd(), secure_filename(file.filename))
        current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
        #if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
            #return make_response(('File already exists', 400))

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

        return redirect(url_for(show_file,filename=file.filename))
    else:
        return make_response(('Invalid file extension',300 ))

@blueprint.route('/show_file')
def show_file(filename):
    file_path=os.path.join(os.getcwd(),filename)
    df = RenderFile(file_path).file_to_dataframe()
    return render_template('download.html', column_names=df.columns.values, row_data=list(df.values.tolist()),
                            zip=zip)


app =  Flask(__name__)
app.register_blueprint(blueprint)
if __name__=='__main__':
    app.run()