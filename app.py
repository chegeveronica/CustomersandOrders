
from flask import Flask, redirect, url_for, session, abort, jsonify, request
import uuid
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta, datetime
import africastalking
import logging

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Session config
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo', 
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route('/')
@login_is_required
def index():
    name = session['profile'].get('name', 'No details found')
    return f'Hello, you are logged in as {name}!.<br/> <a href="/logout">logout</a>'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session['google_id'] = user_info['id']  # Store google_id in the session
    session['name'] = user_info['name'] 
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.errorhandler(401)
def unauthorized(e):
    return "Unauthorized access. Please <a href='/login'>login</a> to continue.", 401

#database
customers = [
    {
        'customer_id': '1',
        'name': 'Veronica',
        'code': '001',
        'phone number': '0743861475'
    },
    {
        'customer_id': '2',
        'name': 'Alice',
        'code': '002',
        'phone number': '0743861475'
        
    }
]

orders = [
    {
        'order_id': uuid.uuid4().hex,
        'customer_id': '2',
        'item': 'Milk',
        'amount': '50'
    },
    {
        'order_id': uuid.uuid4().hex,
        'customer_id': '2',
        'item': 'Sugar',
        'amount': '100'
    },
    {
        'order_id': uuid.uuid4().hex,
        'customer_id': '2',
        'item': 'Margarine',
        'amount': '150'
    },
    {
        'order_id': uuid.uuid4().hex,
        'customer_id': '1',
        'item': 'Eggs',
        'amount': '20'
    },
    {
        'order_id': uuid.uuid4().hex,
        'customer_id': '1',
        'item': 'Bread',
        'amount': '100'
    }

]

#get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify({'customers': customers})

#add customer
@app.route('/customers', methods=['POST'])
def create_customer():
    new_customer = {
        'customer_id': len(customers)+1,
        'name': request.json['name'],
        'code': request.json['code'],
        'phone number': request.json['phone number']
    }
    customers.append(new_customer)
    return jsonify({'new_customer_added': new_customer})

#get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify({'orders': orders})

#add order
@app.route('/orders', methods=['POST'])
def create_order():
    new_order = {
        'order_id': uuid.uuid4().hex,
        'customer_id': request.json['customer_id'],
        'item': request.json['item'],
        'amount': request.json['amount'],
        'timestamp': datetime.now().isoformat()
        
    }
    orders.append(new_order)

    # get customer details then send SMS alert for the order
    customer = next((cus for cus in customers if cus['customer_id'] == new_order['customer_id']), None)
    if customer:
        message = f"Dear {customer['name']}, your order for {new_order['item']} worth {new_order['amount']} has been received!"
        send_sms_alert(customer['phone number'], message)

    return jsonify({'new_order_added': new_order})


# Initialize Africa's Talking
username = "sandbox"
api_key = "atsk_7864da2ab580802cd3ab166930b25c637d3b8b97757a672f4331264ac8193777a1eef269" 
# Initialize the SDK
africastalking.initialize(username, api_key)

# Get the SMS service
sms = africastalking.SMS

def send_sms_alert(phone, message):
    try:
        print(f"Sending SMS to {phone}: {message}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)