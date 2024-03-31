from flask import Flask, render_template, request, redirect
from update import site_data, scrape_javascript
from urllib.parse import urlparse, parse_qs, quote

app = Flask(__name__)


@app.route('/')
def main():
    site_data_dict = site_data()
    scrape_javascript_dict = scrape_javascript()
    return render_template('index.html',
                           days=site_data_dict['days'],
                           periods=site_data_dict['periods'],
                           submit_button=site_data_dict['submit_button'],
                           courses_array=scrape_javascript_dict['courses_array'],
                           course_modules=scrape_javascript_dict['course_modules'],
                           weeks_array=scrape_javascript_dict['weeks_array'],
                           weeks_next=scrape_javascript_dict['weeks_next'],
                           )


@app.route('/lookup')
def lookup():
    # default values
    formType = 'student+set'
    host = 'spenterpriselive.dkit.ie:8000'
    style = 'individual'

    query = parse_qs(urlparse(request.url).query)

    urls = []
    try:
        weeks = query.get('weeks')[0]
    except:
        weeks = ''

    for id in query.get('id'):
        urls.append(generatePhpURL(host=host,
                                   style=style,
                                   formType=formType,
                                   id=id,
                                   days=query.get('days')[0],
                                   periods=query.get('periods')[0],
                                   weeks=weeks,
                                   ))
    return urls


def generatePhpURL(**kwargs):
    postfix = '%0D%0A'
    dkitURL = 'https://timetables.dkit.ie/process.php?url='
    template = f'{kwargs.get("formType")}+{kwargs.get("style")}'
    objectstr = kwargs.get('id')+postfix
    url = f'http://{kwargs.get("host")}/reporting/{kwargs.get("style")};{kwargs.get("formType")};id;{objectstr}?t={template}&days={kwargs.get("days")}&weeks={kwargs.get("weeks")}&periods={kwargs.get("periods")}&template={template}'
    url = dkitURL+quote(url, safe='')
    return url
