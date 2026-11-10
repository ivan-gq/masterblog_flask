from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'blog_posts.json'

def get_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_posts(posts):
    with open(DATA_FILE, 'w') as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = get_posts()
    
    for post in posts:
        if post.get('id') == post_id:
            posts.remove(post)
            break
            
    save_posts(posts)
    
    return redirect(url_for('index'))

def fetch_post_by_id(post_id):
    posts = get_posts()
    for post in posts:
        if post.get('id') == post_id:
            return post
    return None

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = get_posts()
    
    post = None
    for p in posts:
        if p.get('id') == post_id:
            post = p
            break
            
    if post is None:
        
        return "Post not found", 404
    
    if request.method == 'POST':
        
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        
        save_posts(posts)
        
        return redirect(url_for('index'))

    # Else, it's a GET request, display the update page
    return render_template('update.html', post=post)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = get_posts()        
        
        new_id = 1
        if posts:
            new_id = max(post.get('id', 0) for post in posts) + 1            
        
        new_post = {
            "id": new_id,
            "author": request.form.get('author'),
            "title": request.form.get('title'),
            "content": request.form.get('content'),
            "likes": 0
        }        
        
        posts.append(new_post)
        save_posts(posts)
        
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/like/<int:id>')
def like(id):
    posts = get_posts()
    
    for post in posts:
        if post.get('id') == id:
            current_likes = post.get('likes', 0)
            post['likes'] = current_likes + 1
            break
            
    save_posts(posts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)