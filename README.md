# CustomersandOrders
This project is a Flask-based web application that allows users to manage customers and orders. It integrates with Africa's Talking API to send SMS alerts for new orders. The project also includes user authentication via Google OAuth and features unit tests with code coverage.

## Features
* Google OAuth Login: Secure login through Google OAuth.
* Customer Management: Add and view customers.
* Order Management: Add and view orders.
* SMS Notifications: Automatically sends SMS alerts via Africa's Talking for new orders.
* RESTful API: Simple API endpoints for managing customers and orders.
* Unit Testing: Tests included with pytest for code coverage.
* CI/CD: Continuous Integration (CI) and Continuous Deployment (CD) set up using GitHub Actions and Render.com.

## Technologies Used
* Flask: Web framework for Python.
* Google OAuth: For user authentication.
* Africa's Talking API: For sending SMS notifications.
* Render.com: For deploying the application.
* GitHub Actions: For Continuous Integration (CI) and Continuous Deployment (CD).
* Pytest: For unit testing and code coverage.

## Project Setup
### Prerequisites
* Python 3.12.4
* A Google OAuth client (with client_id and client_secret)
* Africa's Talking API key
* GitHub Account
* Render.com account

### Cloning the Repository
		git clone https://github.com/chegeveronica/CustomersandOrders.git
  
### Creating a virtual environment and activate it:

	  python -m venv env
    `source env/bin/activate` . On Windows, use `env\Scripts\activate`

### Installing dependencies:

	  pip install -r requirements.txt
   
  
### Set up environment variables:
* Create a .env file in the project root and add the following environment variables:
* FLASK_SECRET_KEY=your_flask_secret_key
* client_id=your_google_oauth_client_id
* client_secret=your_google_oauth_client_secret
* AFRICASTALKING_API_KEY=your_africastalking_api_key
      
### Running the application:

    python app.py
  
### Run unit tests

    pytest
  
### Run tests with coverage

    coverage run -m pytest
    coverage report
  
## API endpoints
* GET /customers: Retrieve all customers.
* POST /customers: Add a new customer.
* GET /orders: Retrieve all orders.
* POST /orders: Create a new order (triggers an SMS notification).
    
## Deployment
To deploy on render.com:
* Push your repository to GitHub.
* Create a new service on Render.com:
  * Log in to Render.com.
  * Create a new Web Service.
  * Connect your GitHub repository.
  * Choose a branch and set up the build command (pip install -r requirements.txt) and start command (python app.py).
* Configure Environment Variables:
  * In the Render dashboard, add the environment variables required by the app (FLASK_SECRET_KEY, client_id, client_secret, AFRICASTALKING_API_KEY).
* Deploy:
  * Render.com will automatically deploy the application after the first push and on every update to the specified branch.
    
  
  
    


