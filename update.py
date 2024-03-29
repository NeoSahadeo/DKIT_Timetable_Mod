import math
import re
import urllib3
from fake_useragent import UserAgent


def getCoursesData():
    courses = []
    user_agent = UserAgent().random
    headers = urllib3.HTTPHeaderDict()
    headers.add('User-Agent', user_agent)
    response = urllib3.request('GET',
                               'https://timetables.dkit.ie/js/filter.min.js',
                               headers=headers)

    matches = re.finditer(r'(?<=studsetarray)\[\d+\] \[\d+\] \= (?P<arrayValues>.+?)(?=;)', str(response.data))
    for match in matches:
        courses.append(match.group('arrayValues'))

    ceil = len(courses)
    # Divide by 2 because the values are overwritten
    # on original data [I don't know why]
    floor = math.ceil(len(courses)/2)
    return courses[floor:ceil]


def updateSiteCoursesData():
    # Sort data into a 1x3 matrix
    # Course Name, Course Module, ID
    data: [] = getCoursesData()
    count = 0
    matrix = [0]*math.ceil(len(data)/3)
    for element in data:
        if matrix[count] == 0:
            matrix[count] = []
        matrix[count].append(element)
        if len(matrix[count]) == 3:
            count += 1
    matrix.sort()
    return matrix


def getCourseOverview():
    courses = []
    user_agent = UserAgent().random
    headers = urllib3.HTTPHeaderDict()
    headers.add('User-Agent', user_agent)
    response = urllib3.request('GET',
                               'https://timetables.dkit.ie/js/filter.min.js',
                               headers=headers)
    matches = re.finditer(r'(?<=\bdeptarray)\[\d+\] \[\d+\] \= (?P<arrayValues>.+?)(?=;)', str(response.data))
    for match in matches:
        courses.append(match.group('arrayValues'))

    return courses


def updateSiteCoursesOverview():
    # Sort data into a 1x2 matrix
    # Course Name, Course Module
    data: [] = getCourseOverview()
    count = 0
    print(data)
    matrix = [0]*math.ceil(len(data)/2)
    for element in data:
        if matrix[count] == 0:
            matrix[count] = []
        matrix[count].append(element)
        if len(matrix[count]) == 2:
            count += 1
    matrix.sort()
    return matrix
