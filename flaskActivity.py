from flask import Flask, jsonify, request, abort
from pydantic import BaseModel, ValidationError
from typing import List

app = Flask(__name__)

class Activity(BaseModel):
    name: str
    location: str = None
    duration_minutes: int
    
    
sessionList = []

@app.route('/activities/', methods=['POST'])
def create_activity():
    try:
        activity = Activity(**request.json)
        sessionList.append(activity.model_dump())
        return jsonify(activity.model_dump()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 422
    
    
@app.route('/', methods=['GET'])
def get_activities():
    return jsonify(sessionList)

@app.route('/activities/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    if activity_id < 0 or activity_id >= len(sessionList):
        abort(404, description="Activity not found")
    
    try:
        updated_activity = Activity(**request.json)
        sessionList[activity_id] = updated_activity.model_dump()
        return jsonify(updated_activity.model_dump())
    except ValidationError as e:
        return jsonify(e.errors()), 422
    
@app.route('/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    if activity_id < 0 or activity_id >= len(sessionList):
        abort(404, description="Activity not found")
    
    deleted_activity = sessionList.pop(activity_id)
    return jsonify(deleted_activity)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)