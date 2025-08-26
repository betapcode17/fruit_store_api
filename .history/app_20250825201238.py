from flask import Flask, redirect, url_for,request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1> Hello Flask! <h2>"


# Truyen bien
@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
        
    return f"<h1> Hello {name} </h1>"


@app.route('blog/<int:blog_id>')
def blog(blog_id):
    return f"<h1> Blog {blog_id}! </h1>"


# Chuyển hướng trang
@app.route('/admin')
def hello_admin():
    return f"<h1> Hello Admin </h1>"

if __name__ == "__main__":
    app.run(debug=True)
