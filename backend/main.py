from flask import Flask, render_template, redirect, request, url_for, session, flash

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = "rfwef65657eo234w223fh33HI2UhuhgR7YG"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def LaserTag():
    return render_template("projects.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    if request.method == "POST":
    
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "ben" and password == "B3n1sCool":
            return render_template("system/home.html")
        
        else:
            flash("Invalid username or password")
    
    return render_template("login.html")

if __name__ == '__main__':
    app.run()