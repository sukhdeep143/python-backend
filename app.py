from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
# client = MongoClient("mongodb://localhost:27017/")
db = client['login_system']
users_collection = db['users']
posts_collection = db['posts']

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)   
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data['usernameOrEmail']
    password = data['password']

    user = users_collection.find_one({
        '$or': [{'username': username_or_email}, {'email': username_or_email}],
        'password': password
    }, {'_id': 0, 'username': 1, 'email': 1})

    if user:
        return jsonify({'message': 'Login successful', 'email': user['email']}), 200
    return jsonify({'message': 'Invalid credentials'}), 400

@app.route('/get_user', methods=['POST'])
def get_user():
    data = request.get_json()
    email = data.get('email')

    user = users_collection.find_one({'email': email}, {'_id': 0, 'username': 1})
    if user:
        return jsonify({'username': user['username']}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    paragraph = request.form.get('paragraph')
    image = request.files.get('image')

    if not title or not paragraph or not image:
        return jsonify({'message': 'All fields are required'}), 400

    image_filename = image.filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)

    post_data = {
        'title': title,
        'paragraph': paragraph,
        'image_path': f"/uploads/{image_filename}"
    }
    posts_collection.insert_one(post_data)

    return jsonify({'message': 'Post created successfully'}), 201

@app.route('/get_posts', methods=['GET'])
def get_posts():
    posts = list(posts_collection.find({}, {'_id': 0}))
    return jsonify(posts), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
