import math
import re
import urllib3
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import datetime


def matrix_generator_2d(rows=0, columns=0, data=[]) -> []:
    matrix = []
    for row in range(0, rows):
        matrix.append([0]*columns)

    row_tracker = 0
    column_tracker = 0
    for index in range(0, columns * rows):
        try:
            matrix[row_tracker][column_tracker] = data[index]
            if column_tracker == (columns-1):
                column_tracker = 0
                row_tracker += 1
            else:
                column_tracker += 1
        except IndexError:
            break

    return matrix


def weeks_generator(weeks_data: []) -> []:
    day, month, year = weeks_data
    epoch = datetime.datetime(int(year), int(month), int(day))
    weeks_delta = datetime.timedelta(days=7)
    weeks_array = []
    next_week = datetime.datetime.today() + weeks_delta
    next_week_int = -1
    # Weeks in a year = 52
    # Also want current week that's why start at 0
    for week in range(0, 52):
        relative_week = epoch+(weeks_delta*week)
        next_week_bool = 0 < int((next_week.date()-relative_week.date()).days) < 7
        if next_week_bool:
            next_week_int = week + 1
        weeks_array.append((relative_week).isoformat())
    return {
            'weeks_array': weeks_array,
            'weeks_next': next_week_int,
            }


def site_data():
    user_agent = UserAgent().random
    headers = urllib3.HTTPHeaderDict()
    headers.add('User-Agent', user_agent)
    response = urllib3.request('GET',
                               'https://timetables.dkit.ie/studentset.php',
                               headers=headers)

    response = response.data.decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')
    for tag in soup():
        try:
            del tag['style']
        except:
            pass
    days = soup.find('select', {'name': 'days'})
    periods = soup.find('select', {'name': 'periods'})
    submit_button = soup.find('input', {'value': 'View Timetable'})
    return {
            'days': days,
            'periods': periods,
            'submit_button': submit_button,
            }


def scrape_javascript():
    user_agent = UserAgent().random
    headers = urllib3.HTTPHeaderDict()
    headers.add('User-Agent', user_agent)
    response = urllib3.request('GET',
                               'https://timetables.dkit.ie/js/filter.min.js',
                               headers=headers)
    courses_array = []
    courses = re.finditer(r'(?<=studsetarray)\[\d+\] \[\d+\] \= (?P<arrayValues>.+?)(?=;)', str(response.data))
    for match in courses:
        courses_array.append(match.group('arrayValues'))
    ceil = len(courses_array)
    # Divide by 2 because the values are overwritten
    # on original data [I don't know why]
    floor = math.ceil(len(courses_array)/2)
    courses_array = courses_array[floor:ceil]

    course_modules_array = []
    course_modules = re.finditer(r'(?<=\bdeptarray)\[\d+\] \[\d+\] \= (?P<arrayValues>.+?)(?=;)', str(response.data))
    for match in course_modules:
        course_modules_array.append(match.group('arrayValues'))

    weeks_data = re.search(r'(?<=AddGenWeeks\().*?(?=\))', str(response.data))
    weeks_data = weeks_data.group(0).split(',')[0:-3]
    weeks_dict = weeks_generator(weeks_data)

    return {
            'courses_array': matrix_generator_2d(math.ceil((len(courses_array)/3)), 3, courses_array),
            'course_modules': matrix_generator_2d(math.ceil((len(course_modules_array)/2)), 2, course_modules_array),
            'weeks_array': weeks_dict['weeks_array'],
            'weeks_next': weeks_dict['weeks_next']
            }
