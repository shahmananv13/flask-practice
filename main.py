from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json

app = Flask(__name__)

with open('templates/config.json', 'rb') as f:
	params = json.load(f)
print(params['params'])
if params['params']['local_server']:
	app.config['SQLALCHEMY_DATABASE_URI'] =  params['params']['local_uri']
else:
	app.config['SQLALCHEMY_DATABASE_URI'] =  params['params']['prod_uri']

db = SQLAlchemy(app)

class Contact(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(50), nullable=False)
	phone_num = db.Column(db.String(20), nullable=False)
	mes = db.Column(db.String(50), nullable=False)
	date = db.Column(db.String(50), nullable = True)

class Posts(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50), nullable=False)
	slug = db.Column(db.String(25), nullable=False)
	content = db.Column(db.String(50), nullable=False)
	image_url = db.Column(db.String(50), nullable=False)
	date = db.Column(db.String(50), nullable = True)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = params['params']['gmail-user'],
    MAIL_PASSWORD = params['params']['gmail-password']
)

mail = Mail(app)

@app.route("/")
def home():
    return render_template('index.html', params = params)

@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
	print(post_slug, flush = True)
	post = Posts.query.filter_by(slug=post_slug).first()
	return render_template('post.html', params=params, post=post)

# @app.route("/post")
# def post():
#     return render_template('post.html', params = params)


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
		### uncomment this when you want the email service
		# mail.send_message(	
		# 			subject = f'New Message From {name}',
		# 			sender = email,
		# 			body = f'{msg} \n {phone} \n {email}',
		# 			recipients = [params['params']['gmail-user']]			
		# 		)
	return render_template('contact.html', params = params)

app.run(debug=True)