 📌 Overview

This is a simple Flask-based backend server that:
- Allows user registration and login
- Lets logged-in users create posts with images
- Stores data in MongoDB
- Serves uploaded images via URL
- Supports CORS (so it can connect with a frontend like React or Next.js)

---

 🧱 Tech Stack
- Flask – Python web framework
- MongoDB – NoSQL database
- PyMongo – MongoDB client for Python
- Flask-CORS – For enabling cross-origin requests
- HTML Form Handling – For image uploads

---

 📂 Project Structure
```
project-root/
│
├── app.py                   Main Flask app
├── uploads/                 Folder where uploaded images are stored
```

---

 ⚙️ Setup Instructions

1. Install dependencies:
```bash
pip install flask flask-cors pymongo
```

2. Start MongoDB:
Make sure MongoDB is running on your system at:
```
mongodb://localhost:27017/
```

3. Run the server:
```bash
python app.py
```

Server will start at: `http://localhost:5000`

---

 🚀 API Endpoints

---

 1. `POST /register` — User Registration

Registers a new user using `username`, `email`, and `password`.

Request Body:
```json
{
  "username": "sukhdeep",
  "email": "sukh@xyz.com",
  "password": "mypassword"
}
```

Responses:
- ✅ `201`: User registered successfully
- ❌ `400`: User already exists

---

 2. `POST /login` — User Login

Logs in a user using either username or email + password.

Request Body:
```json
{
  "usernameOrEmail": "sukh@xyz.com",
  "password": "mypassword"
}
```

Responses:
- ✅ `200`: Login successful (returns user's email)
- ❌ `400`: Invalid credentials

---

 3. `POST /get_user` — Fetch User Info by Email

Fetches the username of a user based on their email.

Request Body:
```json
{
  "email": "sukh@xyz.com"
}
```

Responses:
- ✅ `200`: `{ "username": "sukhdeep" }`
- ❌ `404`: User not found

---

 4. `POST /create_post` — Create a Post (with Image)

Creates a post with title, paragraph, and image upload.

Form Data (not JSON! Use `multipart/form-data`):
```
title:      My First Post
paragraph:  This is a cool post with an image!
image:      (Choose a file)
```

Responses:
- ✅ `201`: Post created successfully
- ❌ `400`: All fields required

Note: Images are saved in the `uploads/` folder and served via `/uploads/<filename>`

---

 5. `GET /get_posts` — Fetch All Posts

Returns all posts (title, paragraph, image path).

Response Example:
```json
[
  {
    "title": "My First Post",
    "paragraph": "This is a cool post!",
    "image_path": "/uploads/image1.jpg"
  }
]
```

---

 6. `GET /uploads/<filename>` — Serve Uploaded Images

You can access uploaded images like this:

```
http://localhost:5000/uploads/image1.jpg
```

---

 💾 MongoDB Collections Used

- `users` – Stores user documents with:
  ```json
  {
    "username": "sukhdeep",
    "email": "sukh@xyz.com",
    "password": "mypassword"
  }
  ```

- `posts` – Stores posts with:
  ```json
  {
    "title": "My Post",
    "paragraph": "Content here...",
    "image_path": "/uploads/image1.jpg"
  }
  ```

---

 🔐 CORS Enabled

Using:
```python
from flask_cors import CORS
CORS(app, supports_credentials=True)
```

This ensures the frontend (even on a different port like `localhost:3000`) can interact with this backend.

---

 📁 File Upload Setup

- Uploads go to `uploads/` folder.
- Folder is auto-created using:
```python
os.makedirs('uploads', exist_ok=True)
```

---

 🛠 Run the App

```bash
python app.py
```

Then, test API using Postman, cURL, or your frontend.

---
