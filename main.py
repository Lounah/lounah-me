from flask import Flask, render_template, session
from werkzeug.utils import redirect

from core.publications.publications_store import PublicationsStore

app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates'
)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'some-secret-key'

store = PublicationsStore()


@app.route('/')
def index():
    theme = session.get('theme', 'theme-light')
    return render_template("index.html", theme=theme, content=store.get_all_grouped())


@app.route('/posts')
def posts():
    theme = session.get('theme', 'theme-light')
    return render_template("posts.html", theme=theme, content=store.get_posts())


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
