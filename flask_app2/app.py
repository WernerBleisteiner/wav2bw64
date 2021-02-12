import os
import sys
import subprocess
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from scale_json import scale_json
sys.path.append("../")
from fileio import get_wav_info

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #    flash('No file part')
        #    return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        else:
            print("File uploading")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_wav_info',
                                    filename=filename))
    return render_template('index.html')

@app.route('/show_wav_info/<filename>')
def show_wav_info(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    wav_info = get_wav_info(path)
    if wav_info["Channels"] > 8:
        flash('Supporting only WAV files with up to 8 channels')
        return redirect("/")
    else:
        jsonpath = os.path.splitext(path)[0] + '.json'
        cmd = ["audiowaveform", "-i", path, "-o", jsonpath, "--pixels-per-second", "30", "--bits", "8", "--split-channels"]
        _ = subprocess.run(cmd)
        scale_json(jsonpath)
        return render_template('wav-info.html',
                               path=path,
                               jsonpath=jsonpath,
                               filename=filename,
                               wav_info=wav_info)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
