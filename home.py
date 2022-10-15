import json
from pymongo import MongoClient
import urllib.parse
from flask import Flask
from flask import request
import flask
username = urllib.parse.quote_plus('<username>')
password = urllib.parse.quote_plus("<password>")

url = "mongodb+srv://{}:{}@firstapplication.sin0ygt.mongodb.net/?retryWrites=true&w=majority".format(username, password)
cluster = MongoClient(url)
db = cluster['selva']
collection = db['api']


app = Flask(__name__)

@app.route('/obj_list', methods=["GET"])
def get_objects_fromDb():
   ret = {}
   c = 0
   for data in collection.find():
      del data["_id"]
      ret["obj_"+str(c)] = data
      c = int(c)
      c+=1
   return ret


@app.route("/upload_db", methods=["POST"])
def upload_objectInDb():
   data = json.loads(request.stream.read())
   collection.insert_one(data)
   return {
      "upload":"success",
      "status code":"200"
   }
@app.route("/update_db", methods=["PUT"])
def update_one():
   data = json.loads(request.stream.read())
   #del data["update"]
   update = list(collection.find(data["find"]))
   if len(update)>=1:
      collection.find_one_and_update(data["find"], {"$set":data["update"]})
      return "update successfully"
   return "no record found"
@app.route("/delete_record", methods=["DELETE"])
def delete_record():
   data = json.loads(request.stream.read())
   collection.delete_one(data)
   return "success"
if __name__ == '__main__':
   app.run(debug=True)
