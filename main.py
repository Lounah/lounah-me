from enum import Enum

from flask import Flask, render_template, session
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='', static_folder='web/static')
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'some-secret-key'

config = {
    "my_meta": {
        "social": {
            "Github /": "https://github.com/Lounah",
            "Telegram /": "https://t.me/lounvhx",
            "Twitter": "https://twitter.com/lounvhx"
        }
    }
}


class ContentGroup(Enum):
    POST = 0
    PODCAST = 1
    SPEECH = 2


class Content:
    def __init__(self, group: ContentGroup, title: str, url: str, date):
        self.group = group
        self.title = title
        self.url = url
        self.date = date


all_content = [
    Content(ContentGroup.POST, "Отключаем Jetifier и ускоряем сборку: опыт Тинькофф.Бизнес", "https://habr.com/ru/company/tinkoff/blog/535576/", "2020-30-12"),
    Content(ContentGroup.POST, "TeamCity: настраиваем CI/CD в вашей команде", "https://habr.com/ru/company/tinkoff/blog/532546/", "2020-14-12"),
    Content(ContentGroup.POST, "Как Java 8 поддерживается в Android", "https://habr.com/ru/company/tinkoff/blog/478692/", "2019-04-12"),
]

@app.route('/')
def index():
    theme = session.get('theme', 'theme-light')
    return render_template("index.html", theme=theme, meta=config['my_meta']['social'], content=all_content)


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
