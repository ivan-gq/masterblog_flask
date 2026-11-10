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
            "content": request.form.get('content')
        }
        
        posts.append(new_post)
        save_posts(posts)
        
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Fetch the current list of posts
    posts = get_posts()
    
    # Find the blog post with the given id and remove it from the list
    for post in posts:
        if post.get('id') == post_id:
            posts.remove(post)
            break  # Exit the loop once the post is found and removed
            
    # Save the updated list back to the JSON file
    save_posts(posts)
    
    # Redirect back to the home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)