To get started, simply run docker-compose up --build


PROJECTS

GET
curl "http://127.0.0.1:5005/api/v1/projects/1"

curl "http://127.0.0.1:5005/api/v1/projects"

POST (Posting with pid acts as patch. Return success even when the pid is not found as expected from mysql)
curl "http://127.0.0.1:5005/api/v1/projects" \
  -X POST \
  -d "{\"name\": \"test-project-1\"}" \
  -H "Content-Type: application/json" 

PATCH
curl "http://127.0.0.1:5005/api/v1/projects/1" \
  -X PATCH \
  -d "{\"name\": \"test-project-1-new\"}" \
  -H "Content-Type: application/json" 

DELETE (Will fail if any floorpans there as enforcement of foreign key)
curl "http://127.0.0.1:5005/api/v1/projects/1" \
  -X DELETE


FLOORPLANS

GET
curl "http://127.0.0.1:5005/api/v1/floorplans/1"
curl "http://127.0.0.1:5005/api/v1/floorplans/1/large”
curl "http://127.0.0.1:5005/api/v1/floorplans/1/thumb”

POST
curl "http://127.0.0.1:5005/api/v1/floorplans/2" \
  -X POST \
  -H "Content-Type: multipart/form-data" 

Include image with name ‘file’

PATCH
curl "http://127.0.0.1:5005/api/v1/floorplans/1" \
  -X PATCH \
  -H "Content-Type: multipart/form-data" 

Include image with name ‘file’

DELETE
curl "http://127.0.0.1:5005/api/v1/floorplans/1" \
  -X DELETE

Routes
Projects
@app.route('/api/v1/projects', methods=['GET','POST'])
@app.route('/api/v1/projects/<int:pid>', methods=['GET','POST', 'PATCH', 'DELETE'])

Floorplans
@app.route('/api/v1/floorplans/<int:fid>', defaults={'fileType': None}, methods=['GET'])
@app.route('/api/v1/floorplans/<int:fid>/<string:fileType>', methods=['GET'])
@app.route('/api/v1/floorplans/<int:pid>', methods=['POST'])
@app.route('/api/v1/floorplans/<int:fid>', methods=['DELETE', 'PATCH'])
