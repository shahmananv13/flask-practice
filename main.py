from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('templates/config.json', 'rb') as f:
	params = json.load(f)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  params['params']
db = SQLAlchemy(app)

class Contact(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	phone_num = db.Column(db.String(20), nullable=False)
	mes = db.Column(db.String(50), nullable=False)
	date = db.Column(db.String(50), nullable = True)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/post")
def post():
    return render_template('post.html')


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
	if request.method == 'POST':
		email = request.form.get('email')
		name = request.form.get('name')
		msg = request.form.get('msg')
		phone = request.form.get('phone')
		entry = Contact(name = name, mes = msg, date = datetime.now(), phone_num = phone, email = email)
		db.session.add(entry)
		db.session.commit()
	return render_template('contact.html')

app.run(debug=True)