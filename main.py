from flask import Flask,url_for,request,render_template,session,redirect
import sqllite3
import smtplib
from Crypto.Cipher import AES

app=Flask(__name__)

@app.route('/')
@app.route('/<user_name>')
def main(name=None):
	return render_template('home.html',session=session,text=name)

	




































global _id