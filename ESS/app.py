from flask import Flask,render_template,redirect,flash,session,url_for,request,jsonify
import mysql.connector
import os
import time
from werkzeug.utils import secure_filename
from datetime import datetime

#----------------database connections----
conn=mysql.connector.connect(host="localhost",user="root",password="")
mydatabase="ericappdb"
try:
	cursor=conn.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS ericappdb")
	conn.commit()
except:
	conn.rollback()
conn=mysql.connector.connect(host="localhost",user="root",password="",database=str(mydatabase))
#conn=mysql.connector.connect(host="ericgichuri.mysql.pythonanywhere-services.com",user="ericgichuri",password="@2605Eric",database="ericgichuri$ericappdb")
#----------create table projects---------
try:
	sql="""CREATE TABLE IF NOT EXISTS projects(
		projectid int NOT NULL AUTO_INCREMENT,
		projecttitle varchar(30) NOT NULL,
		briefinfo varchar(100) NOT NULL,
		projectdescription varchar(600) NOT NULL,
		datecreated date NOT NULL,
		projectimg1 varchar(50) NOT NULL,
		projectimg2 varchar(50) NOT NULL,
		projectlink varchar(100) NOT NULL,
		projectstatus int NOT NULL,
		postby varchar(30) NOT NULL,
		PRIMARY KEY(projectid)
	)"""
	cursor=conn.cursor()
	cursor.execute(sql)
	conn.commit()
except:
	conn.rollback()

#-------------create table admin---------
try:
	sql1="""CREATE TABLE IF NOT EXISTS users(
		userid int NOT NULL AUTO_INCREMENT,
		fname varchar(20) NOT NULL,
		lname varchar(20) NOT NULL,
		sname varchar(20) NOT NULL,
		email varchar(50) NOT NULL,
		phoneno varchar(20) NOT NULL, 
		occupation varchar(20) NOT NULL,
		role varchar(20) NOT NULL,
		username varchar(20) NOT NULL,
		password varchar(70) NOT NULL,
		profile varchar(30) NOT NULL,
		joindate date NOT NULL,
		PRIMARY KEY(userid),
		UNIQUE KEY(email),
		UNIQUE KEY(phoneno),
		UNIQUE KEY(username)
	)"""
	cursor=conn.cursor()
	cursor.execute(sql1)
	conn.commit()
except:
	conn.rollback()
#----------------create table blog-----
try:
	sql2="""CREATE TABLE IF NOT EXISTS blog(
		blogid int NOT NULL AUTO_INCREMENT,
		blogtopic varchar(50) NOT NULL,
		category varchar(30) NOT NULL,
		subcategory varchar(30) NOT NULL,
		blogcontent varchar(1000) NOT NULL,
		bloggrade varchar(20) NOT NULL,
		blogimage varchar(30) NOT NULL,
		dateposted date NOT NULL,
		timeposted time NOT NULL,
		postedby varchar(20) NOT NULL,
		PRIMARY KEY(blogid),
		UNIQUE KEY(blogtopic)
	)"""
	cursor=conn.cursor()
	cursor.execute(sql2)
	conn.commit()
except:
	conn.rollback()
#---------defined variable--------------
userfullname=""
profile=""

#---------------decorator----------------
app=Flask(__name__)
app.config['SECRET_KEY']="random string"
#app.config['UPLOAD_FOLDER']="/static/images/uploads/"
app.config['UPLOAD_FOLDER']="/"
ALLOWED_EXTENSIONS={'png','jpg','gif','jpeg'}
def check_file(file):
	return "." in file and file.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

#--------------index page----------------
@app.route("/")
def index():
	#------------get projects from database---
	projectdetails=""
	try:
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM projects WHERE projectstatus=1")
		projectdetails=cursor.fetchall()
		if projectdetails:
			return render_template('index.html',projectdetails=projectdetails)
	except:
		return render_template('index.html',projectdetails=projectdetails)

	

#--------------projects page-------------
@app.route("/Projects")
def projects():
	#-------get all projects from databse----
	projectcontent=""
	try:
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM projects")
		projectcontent=cursor.fetchall()
	except:
		pass
	return render_template("projects.html",projectcontent=projectcontent)



#-------------contact page--------------
@app.route("/Contact")
def contact():
	return render_template("contact.html")

#--------------services page--------------
@app.route("/Service")
def service():
	return render_template("services.html")

#-----------------admin page--------------
@app.route("/admin")
def admin():
	global userfullname
	if 'adminid' in session:
		if userfullname=="":
			return redirect(url_for('adminlogin'))
		else:	
			adminid=session['adminid']
			return render_template('admin.html',adminid=adminid,userfullname=userfullname)
	else:
		return redirect(url_for('adminlogin'))

#-------------admin login page-------------
@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
	global userfullname,profile
	if request.method=="POST":
		username=request.form['username']
		password=request.form['password']
		if username=="":
			flash("Username is empty")
		elif password=="":
			flash("Password is empty")
		else:
			try:
				cursor=conn.cursor()
				cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role='Admin'",(username,password))
				userdetails=cursor.fetchall()
				if userdetails:
					session['adminid']=userdetails[0][0]
					session['username']=username
					userfullname=userdetails[0][1]+" "+userdetails[0][2]+" "+userdetails[0][3]
					#profile=userdetails[0][10]
					return redirect(url_for('admin'))
				else:
					flash("Username or Password incorrect. Try Again")
			except:
				flash("Username or Password incorrect")
	return render_template("adminlogin.html")
#-------------admin logout--------------
@app.route("/logout")
def logout():
	if 'adminid' in session:
		session.pop("adminid",None)
		session.pop("username",None)
		return redirect(url_for('adminlogin'))
	else:
		return redirect(url_for('adminlogin'))

#------------admin add project-----------
@app.route("/addproject")
def addproject():
	return render_template("addproject.html")



@app.route("/uploadproject",methods=['GET','POST'])
def uploadprojects():
	if request.method=="POST":
		if 'adminid' in session:
			adminid=session['adminid']
			username=session['username']
			projecttitle=request.form['projecttitle']
			projectinfo=request.form['briefinfo']
			projectdescription=request.form['projectdescription']
			projectlink=request.form['projectlink']
			
			
			if projecttitle=="":
				return jsonify({"message": "! project title empty"})
			elif projectinfo=="":
				return jsonify({"message": "! project briefinfo empty"})
			elif projectdescription=="":
				return jsonify({"message": "! Project description empty"})
			elif projectlink=="":
				return jsonify({"message": "! project link empty"})
			else:
				today=time.strftime("%Y/%m/%d")
				curtime=time.strftime("%Y%m%d%H%M%S")
				if 'img1' not in request.files:
					return jsonify({"message":"image 1 not selected"})

				if 'img2' not in request.files:
					return jsonify({"message":"image 2 not selected"})					
				file=request.files['img1']
				filename=file.filename
				file1=request.files['img2']
				filename1=file1.filename
				if filename=="":
					return jsonify({"message":"File empty"})

				if filename1=="":
					return jsonify({"message":"File empty"})

				if check_file(filename)==False:
					return jsonify({"message":"File not allowed"})

				if check_file(filename1)==False:
					return jsonify({"message":"File not allowed"})
				try:
					fileonename=curtime+".png"
					time.sleep(3)
					filetwoname=curtime+".jpg"
					file.save("static/images/uploads/"+fileonename)#filename
					file1.save("static/images/uploads/"+filetwoname)#filename1
					cursor=conn.cursor()
					cursor.execute("INSERT INTO projects(projecttitle,briefinfo,projectdescription,datecreated,projectimg1,projectimg2,projectlink,projectstatus,postby) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(projecttitle,projectinfo,projectdescription,today,fileonename,filetwoname,projectlink,1,username))
					conn.commit()
					return jsonify({"message":1})
				except:
					return jsonify({"message":"File not saved"})
		else:
			return redirect(url_for('adminlogin'))

@app.route("/viewprojects")
def viewprojects():
	try:
		conn=mysql.connector.connect(host="localhost",user="root",password="",database=str(mydatabase))
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM projects")
		projects=cursor.fetchall()
		conn.commit()
		if projects:
			return render_template("viewprojects.html",projects=projects)
	except:
		pass
@app.route("/Projects/<projectid>")
def userviewproject(projectid):
	projectid=projectid
	global projectd
	try:
		conn=mysql.connector.connect(host="localhost",user="root",password="",database=str(mydatabase))
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM projects WHERE projectid=%s"%(projectid))
		projectd=cursor.fetchall()
		conn.commit()
		if projectd:
			return redirect(url_for('projectview'))
		else:
			return "no project found"
	except:
		return "no project found"+projectid
		pass

@app.route("/Project/")
def projectview():
	global projectd
	return render_template("userviewproject.html",project=projectd)

@app.route("/addblog",methods=['POST','GET'])
def addblog():
	if 'adminid' in session:
		adminid=session['adminid']
		username=session['username']
	else:
		return redirect(url_for('adminlogin'))
	if request.method=="POST":
		bgtopic=request.form['blogtopic']
		bgcategory=request.form['blogcategory']
		bgsubcategory=request.form['blogsubcategory']
		bgcontent=request.form['blogcontent']
		bggrade=request.form['bloggrade']
		if bgtopic=="":
			return jsonify({"message":"Topic is empty"})
		elif bgcategory=="":
			return jsonify({"message":"select category"})
		elif bgsubcategory=="":
			return jsonify({"message":"select sub category"})
		elif bgcontent=="":
			return jsonify({"message":"content is empty"})
		elif bggrade=="":
			return jsonify({"message":"select grading"})
		else:
			today=time.strftime("%Y/%m/%d")
			mytime=time.strftime("%H:%M:%S")
			curtime=time.strftime("%Y%m%d%H%M%S")
			file=request.files['blogimg1']
			filename=file.filename
			if filename=="":
				return jsonify({"message":"image not selected"})

			if check_file(filename)==False:
				return jsonify({"message":"This file is not an image"})

			myblogimage=curtime+".png"
			try:	
				cursor=conn.cursor()
				cursor.execute("INSERT INTO blog(blogtopic,category,subcategory,blogcontent,bloggrade,blogimage,dateposted,timeposted,postedby) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bgtopic,bgcategory,bgsubcategory,bgcontent,bggrade,myblogimage,today,mytime,username))
				conn.commit()
				file.save("static/images/bloguploads/"+myblogimage)
				return jsonify({"message":1})
			except:
				conn.rollback()
				return jsonify({"message":"Unable to upload try Again"})

	return render_template('addblog.html',username=username,adminid=adminid)

#--------------blog page-----------------
@app.route("/Blog")
def blog():
	try:
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog ORDER BY blogid DESC LIMIT 3")
		mylatestblog=cursor.fetchall()
		if mylatestblog:
			mylatestblog=mylatestblog

		
		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE bloggrade='Recommended' ORDER BY blogid DESC LIMIT 3")
		myrecommendedblog=cursor.fetchall()
		if myrecommendedblog:
			myrecommendedblog=myrecommendedblog


		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE bloggrade='Trending' ORDER BY blogid DESC LIMIT 3")
		mytrendingblog=cursor.fetchall()
		if mytrendingblog:
			mytrendingblog=mytrendingblog

		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE category='Programming' ORDER BY blogid DESC LIMIT 5")
		myprogrammingblog=cursor.fetchall()
		if myprogrammingblog:
			myprogrammingblog=myprogrammingblog

		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE category='Softwares' ORDER BY blogid DESC LIMIT 5")
		mysoftwaresblog=cursor.fetchall()
		if mysoftwaresblog:
			mysoftwaresblog=mysoftwaresblog

		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE category='Computers' ORDER BY blogid DESC LIMIT 5")
		mycomputersblog=cursor.fetchall()
		if mycomputersblog:
			mycomputersblog=mycomputersblog

		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE category='Phone' ORDER BY blogid DESC LIMIT 5")
		myphoneblog=cursor.fetchall()
		if myphoneblog:
			myphoneblog=myphoneblog

		cursor=conn.cursor()
		cursor.execute("SELECT * FROM blog WHERE category='Motivations' ORDER BY blogid DESC LIMIT 5")
		mymotivationblog=cursor.fetchall()
		if mymotivationblog:
			mymotivationblog=mymotivationblog

		return render_template("Blog.html",mylatestblog=mylatestblog,myrecommendedblog=myrecommendedblog,mytrendingblog=mytrendingblog,myprogrammingblog=myprogrammingblog,mysoftwaresblog=mysoftwaresblog,mycomputersblog=mycomputersblog,myphoneblog=myphoneblog,mymotivationblog=mymotivationblog)
	except:
		return render_template("Blog.html",mylatestblog=mylatestblog,myrecommendedblog=myrecommendedblog,mytrendingblog=mytrendingblog,myprogrammingblog=myprogrammingblog,mysoftwaresblog=mysoftwaresblog,mycomputersblog=mycomputersblog,myphoneblog=myphoneblog,mymotivationblog=mymotivationblog)


	



if __name__=="__main__":
	app.run(debug=True)
	