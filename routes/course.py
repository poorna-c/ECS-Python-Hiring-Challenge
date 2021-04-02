"""Routes for the course resource.
"""

from run import app
from flask import request, jsonify
from http import HTTPStatus
import data
import datetime


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    found = False
    for i in data.courses:
        if i['id'] == id:
            result = {"data":i}
            found = True
            break
    if not found:
        result = { "messge": "Course "+str(id)+" does not exist" }

    return jsonify(result)


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    filtered_set = []
    try:
        page_size = int(request.args["page-size"])
    except:
        page_size = 5
    try:
        page_number = int(request.args["page-number"])
    except:
        page_number = 1
    try:
        title_words = request.args["title-words"]
        for i in data.courses:
            for j  in title_words.split(','):
                if j in i['title'].lower():
                    filtered_set.append(i)
    except Exception as e:
        print("Error occured at Title Words...",e)
    if filtered_set:
        sets = [filtered_set[i:i+page_size] for i in range(0,len(filtered_set),page_size)]
    else:
        sets = [data.courses[i:i+page_size] for i in range(0,len(data.courses),page_size)]
    result = {
        "data":sets[page_number-1],
        "metadata":{
            "page_count": len(sets),
            "page_number": page_number, 
            "page_size": page_size, 
            "record_count": len(data.courses)
        }
    }
    return jsonify(result)


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    ids_already_have = []
    for i in data.courses:
        ids_already_have.append(i['id'])
    max_id = max(ids_already_have)

    assign_id = max_id + 1
    json_data = request.get_json()
    description = json_data['description']
    discount_price = json_data['discount_price']
    title = json_data['title']
    price = json_data['price']
    image_path = json_data['image_path']
    on_discount = json_data['on_discount']
    new_entry = {
        "date_created": datetime.datetime.now(), 
        "date_updated": datetime.datetime.now(), 
        "description": description, 
        "discount_price": discount_price, 
        "id": assign_id, 
        "image_path": image_path, 
        "on_discount": on_discount, 
        "price": price, 
        "title": title
    }
    data.courses.append(new_entry)
    result = {
        "data": new_entry
    }

    return jsonify(result)


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    data_index = -1
    for i in data.courses:
        if i['id'] == id:
            data_index = data.courses.index(i)
            break

    if data_index == -1:
        result = { "message": "The id does match the payload"}
    else:
        json_data = request.get_json()
        
        description = json_data['description']
        discount_price = json_data['discount_price']
        title = json_data['title']
        price = json_data['price']
        image_path = json_data['image_path']
        on_discount = json_data['on_discount']
        id_ = json_data['id']

        data.courses[data_index]['id'] = id_
        data.courses[data_index]['on_discount'] = on_discount
        data.courses[data_index]['image_path'] = image_path
        data.courses[data_index]['price'] = price
        data.courses[data_index]['title'] = title
        data.courses[data_index]['discount_price'] = discount_price
        data.courses[data_index]['description'] = description
        data.courses[data_index]['date_updated'] = datetime.datetime.now()

        result = {
            "data": {
                "date_updated": data.courses[data_index]['date_updated'], 
                "description": data.courses[data_index]['description'], 
                "discount_price": data.courses[data_index]['discount_price'], 
                "id": data.courses[data_index]['id'], 
                "image_path": data.courses[data_index]['image_path'], 
                "on_discount": data.courses[data_index]['on_discount'], 
                "price": data.courses[data_index]['price'], 
                "title": data.courses[data_index]['title']
            }
        }
    return jsonify(result)


    


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    deleted = False
    for i in data.courses:
        if i['id'] == id:
            print(i,type(i))
            data.courses.remove(i)
            result = { "message": "The specified course was deleted" }
            deleted = True
            break
    if not deleted:
        result = { "messge": "Course "+str(id)+" does not exist" }
    return jsonify(result)
