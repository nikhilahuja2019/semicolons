from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost',27017)

db = client['demo']

collection = db['demoJson']

# post = {"patient_id": 1,
#         "name": "Nikhil Ahuja",
#         "age": 21,
#         "gender": 'M'}

posts = db['demoJson']

@app.route('/saveData', methods=['POST'])
def saveData() :
    data = request.get_json()
    posts = db['demoJson']

    if posts.find_one({'patient_id' : data['patient_id']}):
       return jsonify({'Error': 'Patient Already Exists!'})

    result = posts.insert_one(data)
    if result.acknowledged :
        return jsonify({'result' : 'Success'})
    else :
        return jsonify({'Error': 'Failed'})

@app.route('/updateData', methods=['POST'])
def updateData() :
    data = request.get_json()
    posts = db['demoJson']

    result = posts.update_one({'patient_id' : data['patient_id']}, {"$set" : data})

    if(result.matched_count > 0) :
        return jsonify({'result': 'Details Updated'})
    else :
        return jsonify({'Error': 'No Such Patient Found!'})

@app.route('/getData/<patientId>', methods=['GET'])
def getData(patientId) :
    posts = db['demoJson']
    result = posts.find_one({'patient_id': int(patientId)})
    if result:
        return jsonify({"patient_id" : result['patient_id'], "name" : result['name'], "age" : result['age'], "gender" : result['gender']})
    else :
        return jsonify({'Error': 'No Such Patient Found!'})

if __name__ == '__main__' :
    app.run(debug=True)


# db.collection_names(include_system_collections=False)
