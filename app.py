import jinja2.exceptions
from flask import Flask, render_template, abort

app = Flask(__name__)


@app.route('/blog/')
def blogHome():
    return render_template('pages/index.html')


@app.route('/blog/<path>')
def blogPost(path):
    path = path.replace(".", "")
    try:
        return render_template(f'pages/{path}.html')
    except jinja2.exceptions.TemplateNotFound:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
