import os, argparse
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    session
)
from prompt import Chat
from admin import Vectorstore

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '%s/tmp/' % os.path.dirname(os.path.abspath(__file__))
app.secret_key = '0'
chat = None
vectorstore = None

@app.route('/')
def home():
    return redirect(url_for('prompt'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    if request.method == 'POST' and 'q' in request.json and len(request.json) > 0:
        q = request.json['q']
        a = chat.ask(q)
        if 'history' not in session:
            session['history'] = []
        session['history'].append({'q': q, 'a': a})
        session.modified = True
        return a
    return render_template(
        'prompt.html',
        history=[] if 'history' not in session else session['history']
    )


@app.route('/reset', methods=['POST'])
def reset():
    if request.method == 'POST' and 'action' in request.json and request.json['action'] == 'reset':
        session['history'] = []
        session.modified = True
    return 'ok'


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and 'action' in request.json:
        if request.json['action'] == 'list':
            return vectorstore.list()
        elif request.json['action'] == 'delete' and 'id' in request.json:
            return vectorstore.delete(request.json['id'])
    return render_template('admin.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return vectorstore.add(filename)
    return 'error'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='prompt')
    parser.add_argument('input_path')
    args = parser.parse_args()
    chat = Chat(args.input_path)
    vectorstore = Vectorstore(args.input_path)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
