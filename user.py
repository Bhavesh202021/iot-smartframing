from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://bhavesh:bhau2021@cluster0.1mj5o.mongodb.net/test'

mongo = MongoClient(app.config.get('MONGO_URI'))
db =  mongo['test']
collName = db['users']

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data=request.json
    # users = mongo.test.users
    login_user = collName.find_one({'name' : data['username']})
    # print(login_user['password'])
    if login_user:
        if bcrypt.hashpw(data['pass'].encode('utf-8'), login_user['password']) \
        == login_user['password']:
            session['username'] = data['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    data = request.json
    if request.method == 'POST':
        # users = mongo.test.users
        existing_user = collName.find_one({'name' : data['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt())
            collName.insert_one({'name' : data['username'], 'password' : hashpass})
            session['username'] = data['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)