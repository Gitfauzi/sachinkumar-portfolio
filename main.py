from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "a_really_secret_key_mxcode_123" 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"

db = SQLAlchemy(app)

class User(db.Model):
    sno  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(200), nullable = False)
    message = db.Column(db.String(255), nullable = False)
    datetime = db.Column(db.DateTime, default = datetime.utcnow)

with app.app_context(): # here a user.db file will be made which i can see in sqlite viewer online
    db.create_all()


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/contact", methods = ["GET", "POST"])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']

        # Create new user object
        new_entry = User(email=email, message=message)

        # Save to DB
        db.session.add(new_entry)
        db.session.commit()
        flash("Thank you for contacting me. I'll get back to you soon!", "success")

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

