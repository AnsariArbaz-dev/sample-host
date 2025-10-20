from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
from bson import ObjectId

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://arbazubairy:Imran%40123@charminar.gdqxafh.mongodb.net/?retryWrites=true&w=majority&appName=charMinar")
client = MongoClient(MONGO_URI)
db = client['flask_blog']
blogs_col = db['blogs']

# Dummy admin login
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

# --- Routes ---

@app.route('/')
def index():
    blogs = list(blogs_col.find().sort("date", -1))
    return render_template('index.html', blogs=blogs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('add_blog'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']

        filename = None
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        blog = {
            'title': title,
            'content': content,
            'image': filename,
            'date': datetime.now(),
            'likes': 0,
            'comments': []
        }
        blogs_col.insert_one(blog)
        return redirect(url_for('index'))

    return render_template('add_blog.html')

@app.route('/blog/<id>', methods=['GET', 'POST'])
def view_blog(id):
    blog = blogs_col.find_one({'_id': ObjectId(id)})  # ✅ Correct
    if request.method == 'POST':
        comment = request.form['comment']
        blogs_col.update_one({'_id': ObjectId(id)}, {'$push': {'comments': comment}})
        return redirect(url_for('view_blog', id=id))
    return render_template('blog.html', blog=blog)
    return render_template('blog.html', blog=blog)

@app.route('/like/<id>')
def like_blog(id):
    blogs_col.update_one({'_id': ObjectId(id)}, {'$inc': {'likes': 1}})
    return redirect(url_for('view_blog', id=id))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
