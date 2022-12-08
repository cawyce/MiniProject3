#dns is https://myapp.mini-project-3.dynv6.net/

from flask import Flask,render_template,request
import sqlite3
import pandas as pd
import os
#creats sqlite database only if it doesn't already exist
def database():
    with sqlite3.connect("data.db") as con:
        with open("init.sql") as f:
            con.executescript(f.read())

app=Flask(__name__,template_folder='templates')

#makes sure the database is only created once
if not os.path.exists('data.db'):
    database()

#route for homepage
@app.route('/')
def homepage():
    return render_template("homepage.html");

#route for missing info
@app.route('/missing',methods=['POST'])
def missinginfo():
    return render_template("missinginfo.html")

#loads the webpage to add products to the system
@app.route('/add',methods=['GET'])
def add():
    return render_template("add.html",title="Enter Product Details")

#saves the data from the /add page onto the database
@app.route('/savedetails',methods=['POST'])
def saveDetails():
    #using try method so it grabs the correct variables and there are other paths if something else runs
    try:
        category=request.form.get("category")
        description=request.form.get("description")
        price=request.form.get("price")
        code=request.form.get("code")
        
        #creats the second argument for executemany
        insert_todb=[(category, description, price, code)]
        
        with sqlite3.connect("data.db") as con:
            con.executemany("INSERT INTO data VALUES (?,?,?,?)", insert_todb)
#if any info is missing this reroutes to the webpage for the error message
    except:
        return missinginfo()

    return render_template("homepage.html")

#route for getting the datat for the specific data retrieval
@app.route('/fetch',methods=['GET'])
def getdata():
    return render_template("fetch.html",title="Inventory Retrieval")

@app.route('/view',methods=['POST'])
def view():
    userinput=request.form.get("category").strip()

    #connect to the database and then displays the speciifc row called
    with sqlite3.connect("data.db") as con:
        if userinput != "":
            df=pd.read_sql("SELECT * FROM data WHERE category=?",con,params=(userinput,))
        else:
            df=pd.read_sql("SELECT * FROM product", con)
    
    return render_template("view.html",df=df,title="Retrieval Successful")


#app.run(debug=True,port=8080)
