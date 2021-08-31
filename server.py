from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from tinydb import TinyDB, Query
import uuid
from config import CONFIG, CROSSORIGIN_LOCALHOST

app = Flask(__name__)
CORS(app, resources={r"/api/*": {'origins': CONFIG['ORIGINS']}}, supports_credentials=True)

db = TinyDB('todos.json')

Todos = Query()

@app.route('/api/todos/', methods=['GET', 'POST'])
@cross_origin(origin=CROSSORIGIN_LOCALHOST)
def todos():
    response = ''
    status_code = 200
    
    if request.method == "GET":
        response = db.all()
    if request.method == "POST":
        data = request.json
        new_uuid = str(uuid.uuid1())
        new_todo = {
            "uuid": new_uuid,
            "title": data.get("title"),
            "project": data.get("project"),
            "done": False
        }
        added = db.insert(new_todo)

        if added:
            response = new_todo
            status_code = 201
        else:
            response = "An error occured. Please check your input."
            status_code = 400

    return make_response(jsonify(response), status_code)

@app.route('/api/todos/<todo_uuid>/', methods=['PUT', 'DELETE'])
@cross_origin(origin=CROSSORIGIN_LOCALHOST)
def todo(todo_uuid):
    response = ''
    updated = []
    status_code = 200
    if request.method == "PUT":
        data = request.json
        updated_data = {
            "title": data.get("title"),
            "project": data.get("project"),
            "done": data.get("done")
        }
        updated = db.update(updated_data, Todos.uuid == todo_uuid)
        updated_data["uuid"] = todo_uuid
        response = updated_data

    if request.method == "DELETE":
        updated = db.remove(Todos.uuid == todo_uuid)

    if not updated:
        response = "Todo not found"
        status_code = 404

    return make_response(jsonify(response), status_code)

@app.route('/api/todos/remove-completed/', methods=['POST'])
@cross_origin(origin=CROSSORIGIN_LOCALHOST)
def remove_completed_todos():
    status_code = 200
    data = request.json

    db.remove((Todos.uuid.one_of(data)) & (Todos.done == True))

    return make_response('', status_code)

@app.route('/api/todos/reverse-all/', methods=['POST'])
@cross_origin(origin=CROSSORIGIN_LOCALHOST)
def reverse_all_todos():
    status_code = 200
    data = request.json

    updated_data = {
        "done": data.get("done")
    }

    uuids_to_update = data.get("uuids")

    updated = db.update(updated_data, Todos.uuid.one_of(uuids_to_update))
    
    response = "Done"

    return make_response(response, status_code)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': error.description}), 405)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)