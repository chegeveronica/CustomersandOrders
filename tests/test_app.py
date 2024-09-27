import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_authenticated(client):
    """Test the index route with a logged-in user."""
    with client.session_transaction() as sess:
        sess['google_id'] = 'mock_google_id'
        sess['profile'] = {'name': 'Test User'}
    
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Hello, you are logged in as Test User' in rv.data

def test_home_page_unauthorized(client):
    """Test the index route without login."""
    rv = client.get('/')
    assert rv.status_code == 401
    assert b'Unauthorized access' in rv.data


def test_customers(client):
    """Test fetching customers."""
    rv = client.get('/customers')
    assert rv.status_code == 200
    assert b'Veronica' in rv.data

def test_create_customer(client):
    """Test creating a new customer."""
    rv = client.post('/customers', json={
        'name': 'John Doe',
        'code': '003',
        'phone number': '0705869123'
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'new_customer_added' in data
    assert data['new_customer_added']['name'] == 'John Doe'

def test_get_orders(client):
    """Test fetching all orders."""
    rv = client.get('/orders')
    assert rv.status_code == 200
    assert b'Milk' in rv.data 

def test_create_order(client):
    """Test creating a new order."""
    rv = client.post('/orders', json={
        'customer_id': '1',
        'item': 'Milk',
        'amount': '100'
    })
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'new_order_added' in data
    assert data['new_order_added']['item'] == 'Milk'
    assert data['new_order_added']['amount'] == '100'
