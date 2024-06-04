import sys

# Imports
from flask import Flask, render_template_string, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

# Configuration
DEBUG = True
FLATPAGES_ROOT = 'templates/pages'
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ['.md', '.html']
FREEZER_BASE_URL = "https://finay.github.io/weblog/"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

posts = [page for page in list(pages) if page.path.startswith('posts/')]
tags = set([post['tag'] for post in list(posts) if 'tag' in post.meta.keys()])
timestamped = [post for post in list(posts) if 'date' in post.meta.keys()]
timestamped.sort(key=lambda page: page['date'], reverse=True)


@app.route('/')
def blogHome():
    return render_template_string(pages.get('index').body, pages=timestamped)


@app.route('/about/')
def blogAbout():
    return render_template_string(pages.get('about').body)


@app.route('/messages/')
def blogMessages():
    return render_template_string(pages.get('messages').body)


@app.route('/yearbook/')
def blogYearbook():
    return render_template_string(pages.get('yearbook').body)


@app.route('/status/')
def blogStatus():
    return render_template_string(pages.get('status').body)


@app.route('/tags/')
def blogTags():
    return render_template_string(pages.get('tags').body, tags=tags)


@app.route('/tags/<string:tag>/')
def blogTag(tag):
    pages_with_tag = [page for page in list(pages) if 'tag' in page.meta.keys() and page['tag'] == tag]
    return render_template_string(pages.get('tags').body, pages=pages_with_tag, tag=tag)


@app.route('/<string:page>/')
def blogPost(page):
    page = page.replace(".", "")
    if f'posts/{page}' not in [post.path for post in posts]:
        return render_template_string(pages.get('404').body)
    return render_template_string(pages.get(f'posts/{page}').body)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
