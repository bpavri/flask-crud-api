import os, time, db, json
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image

class Floorplans:

    def __init__(self) -> None:
        pass
        
    def openConnection(self):
        self.connection = db.mysqlInstance()
        self.cursor = self.connection.cursor()
    
    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

    def create(self, pid, theRequest):
        allowed = ('image/jpeg','image/jpg','image/png','image/gif')
        
        try:
            
            # Check for file
            if 'file' not in theRequest.files:
                return jsonify({'message': 'No file found in request. Send it as multipart form data.'}), 400
            
            #Check for file type
            file = theRequest.files['file']
            
            if file.content_type not in allowed:
                return jsonify({'message': 'Only jpeg, jpg, png or gif allowed'}), 400

            timestamp = str(int(time.time()))
            path = os.getcwd() + '/images/' + timestamp + '_' + secure_filename(file.filename)
            theRequest.files['file'].save(path)

            im = Image.open(theRequest.files['file'])
            thumb = im.resize((100, 100))
            large = im.resize((2000, 2000))
            thumbpath = os.getcwd() + '/images/' + timestamp + '_thumb_' +  secure_filename(file.filename)
            largepath = os.getcwd() + '/images/' + timestamp + '_large_' +  secure_filename(file.filename)
            thumb.save(thumbpath)
            large.save(largepath)


            self.openConnection()
            urls = json.dumps([path, thumbpath, largepath])

            self.cursor.execute("INSERT INTO floorplans (pid, name, urls) VALUES (%s, %s, %s)", (pid, secure_filename(file.filename), urls))
            self.connection.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            
            result = self.cursor.fetchall()
            fid = result[0][0]
            self.closeConnection()

            return jsonify({'message' : 'File successfully uploaded', 'fileID' : fid}), 201
        except Exception as e:
            print(e)
            return jsonify({'message' : 'File not uploaded'}), 500

    def patch(self, fid, theRequest):
        allowed = ('image/jpeg','image/jpg','image/png','image/gif')
        
        try:
            
            # Check for file
            if 'file' not in theRequest.files:
                return jsonify({'message': 'No file found in request. Send it as multipart form data.'}), 400
            
            #Check for file type
            file = theRequest.files['file']
            
            if file.content_type not in allowed:
                return jsonify({'message': 'Only jpeg, jpg, png or gif allowed'}), 400

            timestamp = str(int(time.time()))
            path = os.getcwd() + '/images/' + timestamp + '_' + secure_filename(file.filename)
            theRequest.files['file'].save(path)

            im = Image.open(theRequest.files['file'])
            thumb = im.resize((100, 100))
            large = im.resize((2000, 2000))
            thumbpath = os.getcwd() + '/images/' + timestamp + '_thumb_' +  secure_filename(file.filename)
            largepath = os.getcwd() + '/images/' + timestamp + '_large_' +  secure_filename(file.filename)
            thumb.save(thumbpath)
            large.save(largepath)

            #Delete old image file
            self.openConnection()
            self.cursor.execute("select urls from floorplans \
                where fid =  %s", (fid,))
            result = self.cursor.fetchall()

            #Delete the files
            urls = json.loads(result[0][0])
            for url in urls:
                os.remove(url)

            newUrls = json.dumps([path, thumbpath, largepath])
            
            self.cursor.execute("update floorplans set urls = %s where fid = %s", (newUrls,fid))

            self.connection.commit()
            self.closeConnection()

            return jsonify({'message' : 'File successfully updated.'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message' : 'File not updated.'}), 500

    def delete(self, fid):
        try:
            self.openConnection()

            self.cursor.execute("select urls from floorplans \
                where fid =  %s", (fid,))
            result = self.cursor.fetchall()

            #Delete the files
            urls = json.loads(result[0][0])
            for url in urls:
                os.remove(url)

            self.cursor.execute("delete from floorplans where fid = %s", (fid,))
            self.connection.commit()
            self.closeConnection()
            
            return jsonify({"message":"Floorplan deleted succesfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message":"Failed to delete floorplan."}), 500

    def get(self, fid = None, fileType = None):
        self.openConnection()
        
        self.cursor.execute('select urls from floorplans where fid = %s', (fid,))
        result = self.cursor.fetchall()
        self.closeConnection()
        
        urls = json.loads(result[0][0])
        
        if fileType == 'original' or fileType == None:
            return send_file(urls[0])
        elif fileType == 'thumb':
            return send_file(urls[1])
        elif fileType == 'large':
            return send_file(urls[2])
        
        
