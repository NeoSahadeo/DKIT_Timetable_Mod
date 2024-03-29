from flask import Flask, render_template, request, redirect
from update import updateSiteCoursesData, updateSiteCoursesOverview, getButtonValues
from urllib.parse import urlparse, parse_qs, quote

app = Flask(__name__)


@app.route('/')
def main():

    return render_template('index.html',
                           coursesData=updateSiteCoursesData(),
                           coursesOverview=updateSiteCoursesOverview())


@app.route('/lookup')
def lookup():
    # CONSTANTS
    FORMTYPE = 'student+set'
    HOST = 'spenterpriselive.dkit.ie:8000'

    # default values
    style = 'individual'
    weeks = ''
    days = '1-5'
    periods = '5-40'

    ids = parse_qs(urlparse(request.url).query)

    urls = []

    for id in ids.get('id'):
        id = id[1:-1]
        urls.append(generatePhpURL(host=HOST,
                                   style=style,
                                   formType=FORMTYPE,
                                   id=id,
                                   days=days,
                                   weeks=weeks,
                                   periods=periods))

    return urls


def generatePhpURL(**kwargs):
    postfix = '%0D%0A'
    dkitURL = 'https://timetables.dkit.ie/process.php?url='
    template = f'{kwargs.get("formType")}+{kwargs.get("style")}'
    objectstr = kwargs.get('id')+postfix
    url = f'http://{kwargs.get("host")}/reporting/{kwargs.get("style")};{kwargs.get("formType")};id;{objectstr}?t={template}&days={kwargs.get("days")}&weeks={kwargs.get("weeks")}&periods={kwargs.get("periods")}&template={template}'
    url = dkitURL+quote(url, safe='')
    return url
