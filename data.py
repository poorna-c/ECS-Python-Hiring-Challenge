"""Routines associated with the application data.
"""
import json
courses = {}

def load_data():
    """Load the data from the json file.
    """
    global courses
    courses = json.load(open('json/course.json','r'))
    return courses

