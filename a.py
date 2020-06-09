from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import atexit
import smtplib
import os, signal
import pymongo as pym


connection = pym.MongoClient()
db = connection.test
User_details = db["User_details"]
User_Products = db["User_Products"]
Products = db["Products"]

def sendMail():
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('khantaha4210@gmail.com','pjgnnbetxhxamaml')
    
    products = User_Products
    
    p = products.find()
    
    email = {}
    doc = {}
    for i in p:
        doc = i
        text = doc["product_name"] + "\n" + "Price: " + doc["price"] + "\nClick to buy: " + doc["product_link"] + "\n\n"
        try:
            email[doc["email"]].append(text)
        except:
            key = doc["email"]
            email.setdefault(key,[])
            email[key].append(text)
            
    subject = "Price Update"
    for i in email:
        body = ""
        for j in email[i]:
            body = body + j
        
        msg = f"Subject:{subject}\n\n{body}"
        server.sendmail(
                'khantaha4210@gmail.com',
                i,
                msg
                )
    print("Sent Mail")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sendMail,'interval',seconds=3)
sched.start()

app = Flask(__name__)

@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"
 
@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return print("Server Shutdown")

def handle_exit():
    sched.shutdown()

atexit.register(handle_exit)

#atexit.register(shutdown)

if __name__ == "__main__":
    app.run()