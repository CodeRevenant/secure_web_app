Secure Microservice-Based Web Application

1. Project Description
This project is a secure web application built using the Django framework, following OWASP-compliant development practices. The application implements a Task Management System with a microservice-inspired 
architecture, focusing on protecting user data against common web vulnerabilities like SQL Injection and Cross-Site Scripting (XSS)

2. Security Features Summary
Aligned with the OWASP Top 10 and the Manual Code Review Checklist, the following security controls are implemented: 

-Authentication & RBAC: Secure login flow with Role-Based Access Control for Admin and Normal users.

-Input Validation: Strict server-side validation using Django Forms and Regex whitelisting to prevent Injection attacks.

-Sensitive Data Protection: All user passwords are encrypted using the bcrypt hashing algorithm.

-CSRF & XSS Protection: Enabled Cross-Site Request Forgery protection and automatic HTML output encoding.

-Audit Logging: A dedicated Admin-only module that logs login attempts and critical system activities.

-Configuration Security: Sensitive keys and database credentials are managed via .env files.

3. Dependencies 
The project relies on the following key libraries (see requirements.txt for the full list):

-Django: Web framework with built-in security features.

-python-dotenv: For managing environment variables.

-bcrypt: For secure password hashing.

-django-auditlog: For maintaining the admin audit trail

4. Installation Steps   
To set up the project locally, follow these steps: 

->Clone the repository: git clone https://github.com/CodeRevenant/secure_web_app.git
->cd secure_web_app
->Create and activate a virtual environment:python -m venv venv
->.\venv\Scripts\activate
->Install dependencies: pip install -r requirements.txt
->Configure Environment Variables: Copy .env.example to a new file named .env ,Generate a unique SECRET_KEY and ensure DEBUG=False for production

6. How to Run the App

Apply Migrations -> python manage.py migrate
Create Admin User -> python manage.py createsuperuser
Start the Development Server -> python manage.py runserver

--The app will be accessible at http://127.0.0.1:8000--
