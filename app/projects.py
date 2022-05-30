import os
from flask import Flask, request, jsonify
import db


class Projects:

    def __init__(self) -> None:
        pass

    def openConnection(self):
        self.connection = db.mysqlInstance()
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

    def create(self, values):
        try:
            self.openConnection()
            self.cursor.execute("INSERT INTO projects (name) VALUES (%s)", (values['name'],))
            self.connection.commit()
            self.cursor.execute("SELECT LAST_INSERT_ID()")
            
            result = self.cursor.fetchall()
            projectId = result[0][0]
            self.closeConnection()
            
            return jsonify({"message":"Project created succesfully.", "projectId":projectId}), 201
        except Exception as e:
            print(e)
            return jsonify({"message":"Failed to create project."}), 500

    def patch(self, pid, values):
        if pid == None:
            return jsonify({"message":"Failed to create project. Missing project ID."}), 400

        try:
            self.openConnection()
            
            query = "update projects set"
            for val in values:
                query += " " + val + " = %s ,"
            query = query[:-1] + "where pid = %s"
            params = tuple(values.values()) + (pid,)
            
            self.cursor.execute(query, params)
            self.connection.commit()
            self.closeConnection()
            
            return jsonify({"message":"Project updated succesfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message":"Failed to update project."}), 500

    def delete(self, pid):
        try:
            self.openConnection()
            self.cursor.execute("delete from projects where pid = %s", (pid,))
            self.connection.commit()
            self.closeConnection()
            
            return jsonify({"message":"Project deleted succesfully."}), 200
        except Exception as e:
            print(e)
            return jsonify({"message":"Failed to delete project."}), 500

    def get(self, pid = None):
        self.openConnection()
        
        if pid == None:
            #Means show all
            self.cursor.execute("select * from projects left join floorplans \
                on projects.pid = floorplans.pid")
            result = self.cursor.fetchall()
            print (result)

        else:
            self.cursor.execute("select * from projects left join floorplans \
                on projects.pid = floorplans.pid where projects.pid = %s", (pid,))
            result = self.cursor.fetchall()

        toReturn = {}
        for row in result:
            toReturn.setdefault(row[0],{'name': row[1], 'floorplans': []})
            toReturn[row[0]]['floorplans'].append((row[2], row[4]))
        # toReturn = jsonify(toReturn)

        self.closeConnection()
        return toReturn
