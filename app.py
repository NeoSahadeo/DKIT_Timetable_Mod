from flask import Flask, render_template, request, redirect
from update import updateSite

app = Flask(__name__)


@app.route('/')
def main():
    courses = updateSite()
    return render_template('index.html', courses=courses)


@app.route('/lookup', methods=['GET'])
def lookup():
    if request.method == 'GET':
        pass
    return ''
