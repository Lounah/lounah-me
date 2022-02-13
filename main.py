from flask import Flask, render_template, request, make_response, url_for, session
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='', static_folder='web/static')
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'some-secret-key'


@app.route('/')
def index():
    theme = session.get('theme', 'theme-light')
    return render_template("index.html", theme=theme)


@app.route('/dark')
def dark():
    session['theme'] = 'theme-dark'
    return redirect('/')


@app.route('/light')
def light():
    session['theme'] = 'theme-light'
    return redirect('/')


if __name__ == "__main__":
    app.run()
