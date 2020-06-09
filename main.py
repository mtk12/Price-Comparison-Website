from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from bson.objectid import ObjectId
from functools import wraps
import pymongo as pym
import daraz
#import shophive
import yayvo
import ishopping
import mega
import itshop
import rocket
import symbios
import hummart
import goto
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import smtplib
import os, signal

#GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
#CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
##chrome_options = webdriver.ChromeOptions()
##chrome_options.add_argument('--disable-gpu')
##chrome_options.add_argument('--no-sandbox')
##chrome_options.binary_location = GOOGLE_CHROME_PATH
##driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
#
#chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#chrome_options.add_argument("headless")
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)

ans = {}

app = Flask(__name__)
app.secret_key='secret123'

connection = pym.MongoClient('mongodb+srv://mtk12:audionic1234@cluster0-1msja.mongodb.net/test?retryWrites=true&w=majority')
db = connection.get_database('test')

User_details = pym.collection.Collection(db, 'User_details')
User_Products = pym.collection.Collection(db, 'User_Products')
Products = pym.collection.Collection(db, 'Products')


#def sendMail():
#    server = smtplib.SMTP('smtp.gmail.com',587)
#    server.ehlo()
#    server.starttls()
#    server.ehlo()
#    
#    server.login('khantaha4210@gmail.com','pjgnnbetxhxamaml')
#    
#    products = User_Products
#    
#    p = products.find()
#    
#    email = {}
#    doc = {}
#    for i in p:
#        doc = i
#        text = doc["product_name"] + "\n" + "Price: " + doc["price"] + "\nClick to buy: " + doc["product_link"] + "\n\n"
#        try:
#            email[doc["email"]].append(text)
#        except:
#            key = doc["email"]
#            email.setdefault(key,[])
#            email[key].append(text)
#            
#    subject = "Price Update"
#    for i in email:
#        body = ""
#        for j in email[i]:
#            body = body + j
#        
#        msg = f"Subject:{subject}\n\n{body}"
#        server.sendmail(
#                'khantaha4210@gmail.com',
#                i,
#                msg
#                )
#    print("Sent Mail")
#
#sched = BackgroundScheduler(daemon=True)
#sched.add_job(sendMail,'interval',seconds=5)
#sched.start()

@app.route('/')
def index():
    return render_template('Home.html')

#@app.route('/stopServer', methods=['GET'])
#def stopServer():
#    os.kill(os.getpid(), signal.SIGINT)
#    return print("Server Shutdown")
#

@app.route('/query', methods=['POST'])
def upload():
    global ans
    
    products = User_Products

    if request.method == 'POST':
        if request.form.get('Do_something'):
            pro = request.form.get('Do_something')
            pro = pro.split("  ")
            for i in pro:
                print(i)
            
            user_id = products.insert_one(
            {   "email" : session["username"],
                "product_name" : pro[0],
                "price" : pro[1],
                "product_link" : pro[2],
                "img_link" : pro[3],
                "web_img" : pro[4]
            })
            if user_id:
                print("Inserted")
            flash('Product added to track', 'success')
            return render_template('Result.html',dictionary=ans)
        else:
            query = request.form['query']
            category = request.form['category']
            print(query)
            print(category)
            query = query.lower()
            check_product = check_pro(query,category)
            
            if check_product:
                products = Products
                pid = products.find({"query":query,"category":category})
                
                answer = {}
                y = {}
                for doc in pid:
                    y = doc
                    key = y["title"]
                    answer.setdefault(key,[])
                    answer[key].append(y["price"])
                    answer[key].append(y["link"])
                    answer[key].append(y["image"])
                    answer[key].append(y["shop_image"])
                           
            else:
                if(category == "Grocery"):
                    df1 = daraz.daraz(query)
                    answer = dict(df1)
                    answer.update(yayvo.yayvo(query))
                    answer.update(hummart.hummart(query))
                    #print(answer)
                elif(category == "Mobile and Tablets" or category == "Laptop and Desktop"):
                    df1 = daraz.daraz(query)
                    answer = dict(df1)
                    answer.update(yayvo.yayvo(query))
                    answer.update(goto.goto(query))
                    #answer.update(ishopping.ishopping(driver,query))
                    answer.update(mega.mega(query))
                    answer.update(rocket.rocket(query))
                    answer.update(itshop.itshop(query))
                    answer.update(symbios.symbios(query))
                else:
                    #answer.update(shophive.shophive(driver,query))
                    df1 = daraz.daraz(query)
                    answer = dict(df1)
                    answer.update(rocket.rocket(query))
                    answer.update(yayvo.yayvo(query))
                    answer.update(goto.goto(query))
                    #answer.update(ishopping.ishopping(driver,query))
                
                
            ans = answer
            ans = sorted(ans.items(), key=lambda e: e[1][0])
            ans = dict(ans)
            store_product(ans,query,category)
            return render_template('Result.html',dictionary=ans)

def check_pro(query,category):
    products = Products
    pid = products.find({"query":query})
    if len(list(pid)) > 0:
        return True
    else:
        return False
    
    
def store_product(products,query,category):
    store = Products
    x = len(products)/2
    
    for i in products:
        if x < 0:
            break
        x = x - 1
        uid =  store.insert_one({
                "query" : query,
                "category" : category,
                "title" : i,
                "price" : products[i][0],
                "link" : products[i][1],
                "image" : products[i][2],
                "shop_image" : products[i][3]
                })
        
        
    
    
    
# Register Form Class
class RegisterForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=50)])
    name = StringField('Name', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    users = User_details
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        myid = users.insert_one(
            {   "name" : name,
                "email" : email,
                "password" : password
            })
        flash('You are now registered and can log in', 'success')

        redirect(url_for('login'))
        #return render_template('Login.html') 
    return render_template('Register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User_details
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['username']
        password_candidate = request.form['password']
        
        response = user.find_one({'email': email})
        

        if response:
            password = response['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = email

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('Login.html', error=error)
        else:
            error = 'Email not found'
            return render_template('Login.html', error=error)

    return render_template('Login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    products = User_Products
    email = session['username']
     
    if request.method == 'POST':
        z = products.delete_one({'_id': ObjectId(request.form.get('Do_something'))})
        email = session['username']
    
        x = products.find({"email" : email}) 
        if z:
            data = {}
            y = {}
            for doc in x:
                y = doc
                print(doc)
                key = y["product_name"]
                data.setdefault(key,[])
                data[key].append(y["price"])
                data[key].append(y["product_link"])
                data[key].append(y["img_link"])
                data[key].append(y["web_img"])
                data[key].append(y["_id"])
            
        return render_template('Dashboard.html', dictionary=data)
    
    x = products.find({"email" : email}) 
    if x:
        data = {}
        y = {}
        for doc in x:
            y = doc
            key = y["product_name"]
            data.setdefault(key,[])
            data[key].append(y["price"])
            data[key].append(y["product_link"])
            data[key].append(y["img_link"])
            data[key].append(y["web_img"])
            data[key].append(y["_id"])
            
        return render_template('Dashboard.html', dictionary=data)
    else:
        msg = 'No Articles Found'
        return render_template('Dashboard.html', msg=msg)

#
#def handle_exit():
#    sched.shutdown()
#
#atexit.register(handle_exit)

if __name__ == '__main__':
    
    app.run()
    