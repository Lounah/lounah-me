from flask import Flask, render_template, session
from werkzeug.utils import redirect

from core.publications.publication import PublicationType
from core.publications.publications_source import StaticPublicationSource
from core.publications.publications_repository import PublicationsRepository

app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates'
)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'some-secret-key'

source = StaticPublicationSource('web/static/publications')
store = PublicationsRepository(source)


@app.route('/')
def index():
    theme = session.get('theme', 'theme-light')
    return render_template("index.html", theme=theme, content=store.get_all_grouped())


@app.route('/posts')
def posts():
    theme = session.get('theme', 'theme-light')
    return render_template("publications.html", theme=theme, content=store.get_all_by_type(PublicationType.POST))


@app.route('/podcasts')
def podcasts():
    theme = session.get('theme', 'theme-light')
    return render_template("publications.html", theme=theme, content=store.get_all_by_type(PublicationType.PODCAST))


@app.route('/talks')
def talks():
    theme = session.get('theme', 'theme-light')
    return render_template("publications.html", theme=theme, content=store.get_all_by_type(PublicationType.TALK))


@app.route('/blog/<id>')
def post(id):
    theme = session.get('theme', 'theme-light')
    return render_template("publication.html", theme=theme, publication=store.get_by_id(id))


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
