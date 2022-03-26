from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime,json
from db import insertNewRecord
app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bhavesh@tcet'
app.config['MYSQL_DB'] = 'login'

# Intialize MySQL   
mysql = MySQL(app)

@app.route('/device_dashboard')
def device_dashboard():
    return render_template('device_dashboard.html')

@app.route('/login/home/')
def home():
    return render_template('home.html')

@app.route('/')
def welcome():
    return render_template('register.html')

@app.route('/login/home/info')
def info():
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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
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
        
        
         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
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
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#email = request.form['email']





# http://localhost:5000/login/profile - this will be the profile page, only accessible for loggedin users
@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



##API 
# @app.route("/user" ,methods = ['GET'])
# def user_get():
#     return ("http://127.0.0.1:2000/user")

@app.route("/user" ,methods = ['POST'])
def user_post():
    data = request.json
    try:
        temperature = data['temperature']
        humidity = data['humidity']
        light = data['light']
        moistureLevel = data["moistureLevel"]
        #post = open(f'./data/bhavesh.json','w')
        
        obj = {
            'temperature': temperature,
            'humidity':humidity,
            'light':light,
            'moistureLevel':moistureLevel  
        }
        print(obj)
        #post.write(json.dumps(obj))
        #post.close()
        l = insertNewRecord(obj)
        return {'status_code':200,'message':'Post created successful'}
        
    except Exception as e:
        return {'status_code':300 , 'message':f'Generic error:{str(e)}'}
    
    # try:
    #     username = request.args.get('username' , '')
    #     try:
    #         userfile = open(f'./data/{username}.json','r')
    #         userjson = json.loads(userfile.read())
    #         userfile.close()            
    #         return userjson
        
    #     except:
    #         return {'status_code':301 ,'Message':'User not found!'}
             
        
    # except:
    #     return {'status_code' :300 ,'Message':'Bad request! send ona username'}

# @app.route("/makepost" ,methods = ['POST'])
# def makepost():
#     request.get_json(force =True)
#     data = request.json
    
#     timestamp = datetime.datetime.now()
#     timestamp = str(timestamp).replace(' ','').replace(':',' ')
#     print(timestamp)
    
    
#     try:
#         title = data['title']
#         body = data['body']
#         user = data['username']
#         post = open(f'./data/{user}_{timestamp}.json','w')
        
#         obj = {
#             'timestamp':timestamp,
#             'username': user,
#             'title':title,
#             'body':body
            
#         }
#         post.write(json.dumps(obj))
#         post.close
#         return {'status_code':200,'message':'Post created successful'}
        
#     except Exception as e:
#         return {'status_code':300 , 'message':f'Generic error:{str(e)}'}
#     print(timestamp)    
    
#     return {}

        

@app.route("/senseordata" ,methods = ['POST'])
def sensordata():
    #Pull out the username from the request
    
    """
    
    {
        'username' : 'vikind_dev'
    }
    
    """
    request.get_json(force=True)
    data = request.json
    try:
        username = data['username']     
        try:
            user_file =  open(f'./data/{username}.json','r')
            json_data = json.loads(user_file.read())
            user_file.close()
            
            return json_data
        except:
            return {'status_code':301, 'message':'User not found!'}   
    except:
         return {'status_code':300 , 'message':'Malformed request, send on username'}
        
    #open the filr with user's information in it
    
    #send our response

## FRONTED/RENDER SECTION ##
@app.route('/login/home/userRender', methods =['GET'])
def user_render():
    username = request.args.get('username')
    try:
        userfile = open(f'./data/{username}.json', 'r')
        userjson = json.loads(userfile.read())
        userfile.close()
        creation_date = userjson['creation_date']
        posts = userjson['posts']
        return render_template('hellouser.html', username = username, creation_date = creation_date, posts = posts)
    except Exception as e:
        return render_template('error.html',exception=str(e))
    
        
   

if __name__ == "__main__":
    app.run(debug = True)

