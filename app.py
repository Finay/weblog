import jinja2.exceptions
from flask import Flask, render_template, abort
import json
from os import listdir
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)


def getPostInfo(file):
    with open(f'templates/pages/posts/{file}') as fd:
        lines = [i.strip() for i in fd.readlines()]
        if '{#' in lines and '#}' in lines:
            lines = lines[lines.index('{#')+1:lines.index('#}')]
    return json.loads("".join(lines))


def getPostFiles():
    return listdir('templates/pages/posts')


def getPostsInfo():
    post_files = getPostFiles()
    posts_info = [getPostInfo(file) for file in post_files]
    return [*zip(post_files, posts_info)]


@app.route('/blog/')
def blogHome():
    return render_template('pages/index.html')


@app.route('/blog/about')
def blogAbout():
    return render_template('pages/about.html')


@app.route('/blog/tags')
def blogTags():
    return render_template('pages/tags.html')


@app.route('/blog/<path>')
def blogPost(path):
    path = path.replace(".", "")
    try:
        return render_template(f'pages/posts/{path}.html')
    except jinja2.exceptions.TemplateNotFound:
        abort(404)


@app.route('/wip/<path>')
def workInProgress(path):
    path = path.replace(".", "")
    try:
        return render_template(f'wip/{path}.html')
    except jinja2.exceptions.TemplateNotFound:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
