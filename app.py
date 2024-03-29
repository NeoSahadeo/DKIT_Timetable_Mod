from flask import Flask, render_template, request, redirect
from update import updateSiteCoursesData, updateSiteCoursesOverview

app = Flask(__name__)


@app.route('/')
def main():
    # courses = updateSite()
    courseDataArray = []
    courseOverviewArray = []
    return render_template('index.html',
                           coursesData=courseDataArray,
                           coursesOverview=courseOverviewArray)


@app.route('/lookup', methods=['GET'])
def lookup():
    if request.method == 'GET':
        pass
    return ''
