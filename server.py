from flask import Flask, render_template, request, redirect, flash
import re
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'emailvalidation')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html') 

# Displaying Results
@app.route('/result', methods=['POST'])
def takeResults():
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(request.form['email']) < 1:
        message = flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        message = flash("Invalid Email Address!")
        return redirect('/')
    else:
        flash("Success!")
        # return redirect('/success')
        # we want to insert into our query.
        query = "INSERT INTO users (email) VALUES (:email)"
        # We'll then create a dictionary of data from the POST data received.
        data = {
                'email': request.form['email'],
            }
        # Run query, with dictionary values injected into the query.
        mysql.query_db(query, data)
        return redirect('/success')
   


@app.route('/success')
def success():
    query = "SELECT * FROM users"                           # define your query
    email = mysql.query_db(query) 
    return render_template("entered.html", all_email=email)

app.run(debug=True)