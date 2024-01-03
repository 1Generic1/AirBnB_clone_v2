#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_hbnb():
    """print web"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """print web"""
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    """print C followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
