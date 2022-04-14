from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import re
from pymongo import MongoClient
import datetime,json
from db import insertNewRecord
msValue = -1

app = Flask(__name__)
import bcrypt

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://bhavesh:bhau2021@cluster0.1mj5o.mongodb.net/test'
mongo = MongoClient(app.config.get('MONGO_URI'))
db =  mongo['test'] 
collName = db['users']



@app.route('/login/dashboard/',methods=['GET', 'POST'])
def dashboard():
    print("-----------------")
    return render_template('overview.html')

    
@app.route('/')
def welcome():
    return render_template('register.html')

@app.route('/login/home')
def login_home():
    return render_template('info.html')


# http://localhost:5000/login/ - the following will be our login page, which will use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        
        account = collName.find_one({'name' : username})
        
        # Fetch one record and return result
        # If account exists in accounts table in out database
        if account and bcrypt.hashpw(password.encode('utf-8'), account['password']) == account['password']:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            # session['id'] = account['_id']
            session['username'] = account['name']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('login_home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))




# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/login/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
         # Check if account exists using MySQL
        account = collName.find_one({'name' : username,'email' : email})
        
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            collName.insert_one({'name' : username ,'password' : hashpass,'email':email})
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#email = request.form['email']





#http://localhost:5000/login/profile - this will be the profile page, only accessible for loggedin users
@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        mongo = MongoClient(app.config.get('MONGO_URI'))
        db =  mongo['test']
        collName = db['users']
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = collName.find_one({'name' : username})
        account = collName.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



##API 
# @app.route("/user",methods = ['GET'])
# def user_get():
#     return ("http://127.0.0.1:2000/user")

# @app.route("/moisturevalue",methods = ['POST'])
# def setmoisture_get():
#     if msValue > 1 :
#         return msValue
#     return -1
    



@app.route("/setMoisture",methods = ['POST'])
def setMoisture():
    msValue = request.form['moisturealue']  
    print(msValue,type(msValue))
    if msValue > 1:
        return msValue
    return -1
        # try:
        #     # moistureLevel = msValue
        #     return msValue    
        # except Exception as e:
        #     # return {'status_code':300 , 'message':f'Generic error:{str(e)}'}
        #     return -1
    
    
    # return ("http://127.0.0.1:2000/setsoilMoisture")

# @app.route("/test" , methods=['GET', 'POST'])
# def test():
#     select = request.form.get('comp_select')
#     print(str(select))
#     return(str(select)) # just to see what select is


@app.route("/user" , methods = ['POST'])
def user_post():
    data = request.json
    try:
        temperature = data['temperature']
        humidity = data['humidity']
        light = data['light']
        moistureLevel = data['moistureLevel']
                     
        obj = {
            'temperature': temperature,
            'humidity':humidity,
            'light':light,
            'moistureLevel':moistureLevel
        }
        #post = open(f'./data/bhavesh.json','w')
        print(obj)
        #post.write(json.dumps(obj))
        #post.close()
        l = insertNewRecord(obj)
        return {'status_code':200,'message':'Post created successful'}
        
    except Exception as e:
        return {'status_code':300 , 'message':f'Generic error:{str(e)}'}
    
if __name__ == "__main__":
    app.run(debug = True,port=2000)

