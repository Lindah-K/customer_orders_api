
# Customer Orders Service with OpenID Connect and SMS Notification

This project implements a simple Python service with Django, allowing users to manage customers and orders. It uses OpenID Connect for authentication and authorization, and sends SMS notifications to customers upon order creation via Africa’s Talking SMS gateway. The project also includes Continuous Integration (CI) and Continuous Deployment (CD) using GitHub Actions, and is deployed on Render.

## Features
- **Customer and Orders API**: Simple REST API to manage customers and their orders.
- **Authentication**: OpenID Connect for user authentication.
- **SMS Notifications**: Sends an SMS to customers when a new order is placed.
- **CI/CD**: Automated testing, build, and deployment using GitHub Actions.
- **Deployment**: Hosted on Render.

## Technologies Used
- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Authentication**: OpenID Connect
- **SMS Gateway**: Africa's Talking
- **CI/CD**: GitHub Actions
- **Hosting**: Render

## Prerequisites
- Python 3.x
- Africa’s Talking Account
- Google OpenID Connect
- Render account

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Lindah-K/customer_orders_api.git
cd customer_orders_api
```

### 2. Set up a virtual environment
```bash
python3 -m venv venv
# On Windows use:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root and add the following environment variables:
```
SECRET_KEY=your_django_secret_key
SMS_API_KEY=your_africas_talking_api_key
OIDC_RP_CLIENT_ID=your_openid_client_id
OIDC_RP_CLIENT_SECRET=your_openid_client_secret
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Run the application
```bash
python manage.py runserver
```

### 7. Running Tests
To run the unit tests, use the following command:
```bash
python manage.py test
```

## Deployment
The project is configured to be deployed on Render using a `Procfile`:

1. **Push to GitHub**: Push your code to a GitHub repository.
2. **Render Setup**: Create a new service on Render, connecting your GitHub repository.
3. **Automatic Deployment**: Render will automatically deploy your application after each push.

## CI/CD Pipeline
GitHub Actions is used for CI/CD to automate the testing and deployment process.

- **Testing**: On each push, the tests will be run to ensure the code is correct.
- **Deployment**: After tests pass, the code is automatically deployed to Render.

## License
This project is licensed under the MIT License.
