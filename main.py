from flask import Flask

from sources.application_state import ApplicationState
from sources.pages.main_page import MainPage
from sources.pages.publication_page import PublicationPage
from sources.pages.publications_page import PostsPage, PodcastsPage, TalksPage
from sources.publications.publications_source import StaticPublicationSource
from sources.resources.lang import Lang
from sources.resources.publications import Publications
from sources.resources.strings import Strings

app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates'
)

strings = Strings('web/static/resources/strings.toml')
publications = Publications({
    Lang.RU: StaticPublicationSource('web/static/publications/ru'),
    Lang.EN: StaticPublicationSource('web/static/publications/en')
})
app_state = ApplicationState(strings, publications, default_lang=Lang.RU)


@app.route('/')
def index():
    return MainPage(app_state).create()


@app.route('/posts')
def posts():
    return PostsPage(app_state).create()


@app.route('/podcasts')
def podcasts():
    return PodcastsPage(app_state).create()


@app.route('/talks')
def talks():
    return TalksPage(app_state).create()


@app.route('/publications/<id>')
def publication(id):
    return PublicationPage(id, app_state).create()


if __name__ == "__main__":
    app.run()
