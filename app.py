from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client['login_system']
users_collection = db['users']

# Signup Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
        return jsonify({'message': 'User already exists'}), 400

    users_collection.insert_one({'username': username, 'email': email, 'password': password})
    return jsonify({'message': 'User registered successfully'}), 201

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data['usernameOrEmail']
    password = data['password']

    user = users_collection.find_one({
        '$or': [{'username': username_or_email}, {'email': username_or_email}],
        'password': password
    })

    if user:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 400

if __name__ == '__main__':
    app.run(debug=True)
