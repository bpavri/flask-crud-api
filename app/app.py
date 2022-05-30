# from unicodedata import name
import os
from flask import Flask, request, jsonify
from projects import Projects
from floorplans import Floorplans

app = Flask(__name__)

@app.route('/welcome/', methods=['GET'])
def welcome():
    return "Welcome to CRUD"

#API call for projects
@app.route('/api/v1/projects', methods=['GET','POST'])
@app.route('/api/v1/projects/<int:pid>', methods=['GET','POST', 'PATCH', 'DELETE'])
def projects(pid = None):
    myProject = Projects()
    
    if request.method == 'GET':
        return jsonify(myProject.get(pid))

    if request.method == 'POST':
        if pid == None:
            #MEans create a new one
            return myProject.create(request.json)
        else:
            #Work it like patch
            return myProject.patch(pid, request.json)

    if request.method == 'PATCH':        
        return myProject.patch(pid, request.json)

    if request.method == 'DELETE':        
        return myProject.delete(pid)


@app.route('/api/v1/floorplans/<int:fid>', defaults={'fileType': None}, methods=['GET'])
@app.route('/api/v1/floorplans/<int:fid>/<string:fileType>', methods=['GET'])
@app.route('/api/v1/floorplans/<int:pid>', methods=['POST'])
@app.route('/api/v1/floorplans/<int:fid>', methods=['DELETE', 'PATCH'])
def floorplans(pid = None, fid = None, fileType = 'original'):
    myFloorplan = Floorplans()

    if request.method == 'POST':
        return myFloorplan.create(pid, request)

    if request.method == 'DELETE':
        return myFloorplan.delete(fid)

    if request.method == 'GET':
        return myFloorplan.get(fid, fileType)

    if request.method == 'PATCH':
        return myFloorplan.patch(fid, request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)