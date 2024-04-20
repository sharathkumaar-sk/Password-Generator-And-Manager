# Password-Generator-And-Manager

## Overview

This script serves as a password manager application that allows users to generate, manage, and export passwords securely. It utilizes encryption techniques to store passwords in a database, ensuring confidentiality and security. Users can perform various operations such as generating passwords, viewing, editing, deleting, searching for passwords, and exporting password data in different formats like CSV, PDF, and SQLite database.


## Key Features

- Password Generation: Users can generate strong, random passwords based on specified criteria such as length and character set.
- Password Encryption: Generated passwords are encrypted using the Fernet encryption scheme before storing them in the database, ensuring data security.
- Password Management: Users can manage their passwords by viewing, editing, and deleting existing passwords for different applications.
- Search Functionality: Users can search for passwords by specifying the application name, making it easy to retrieve specific password entries.
- Export Functionality: Users can export password data in various formats such as CSV, PDF, and SQLite database for backup or external use.
- User-Friendly Interface: The script provides a simple and intuitive command-line interface, guiding users through the password management process with clear menu options.
- Error Handling: The script includes robust error handling mechanisms to catch and display errors, ensuring smooth operation and user-friendly experience.
- Secure Database Storage: Passwords are stored securely in a MySQL database, safeguarding sensitive information against unauthorized access.
- Modular Design: The script is organized into functions and modules, promoting code reusability, readability, and maintainability.
- Main Menu Navigation: Users can easily navigate between different functionalities using the main menu, providing a seamless user experience.
Getting Started
Prerequisites
Python 3.x installed (Download Python)
Text editor or IDE of your choice (List of Source Code Editors)
Installation
Clone the Repository:
bash
Copy code
git clone https://github.com/your-username/password-manager.git
Install Dependencies:Navigate to the project directory and install the required libraries using pip:
bash
Copy code
cd password-manager
pip install -r requirements.txt
Usage
Run the application:

bash
Copy code
python password_manager.py
Follow the on-screen instructions to generate passwords, manage your password database, and utilize export functionalities.

Contributing
We welcome your contributions! If you'd like to enhance this project, follow these steps:

Fork the Repository: Create a copy of the repository on your GitHub account.
Make Changes: Implement your desired improvements and modifications.
Submit a Pull Request: Share your code changes with the project maintainers for review and potential integration.
License
This project is distributed under the permissive MIT License. Refer to the LICENSE file for the full terms and conditions.

Database Setup (External to app.py)
Create MySQL Database
Access your MySQL server administration tool (e.g., phpMyAdmin, MySQL Workbench).
Create a new database and name it appropriately (e.g., password_manager).
Create passwords Table
Within the newly created database, execute the following SQL statement to create the passwords table:

sql
Copy code
CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password_hash BLOB NOT NULL,  -- Use a secure hashing algorithm for password storage
    `key` VARCHAR(255) NOT NULL
);
Explanation:

id: Auto-incrementing integer for unique identification (primary key).
app_name: Stores the name of the application the credentials belong to (e.g., "Gmail", "Social Media Platform").
username: Username associated with the application.
password_hash: Stores the securely hashed password using a strong hashing algorithm like bcrypt (never store passwords in plain text).
key: An optional field that can be used to store additional security information (e.g., encryption key for password decryption).
Create Database User
Create a new user specifically for the password manager application and grant it the necessary privileges.
Important:

Avoid using the root user for application access.
Grant privileges on the password_manager database (e.g., SELECT, INSERT, UPDATE, DELETE) to this new user.
Assign a strong password to the newly created user and store it securely (avoid hardcoding passwords in code).
Connecting to the Database in app.py (Secure Method)
Environment Variables:

Highly recommended: Store database credentials (username, password) as environment variables to improve security and avoid hardcoding them in your code.

Use a tool like dotenv to manage environment variables.

Here's an example structure for app.py:

python
Copy code
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

host = os.getenv("DB_HOST", "localhost")  # Optional default value
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
Secure Connection:

Import the necessary libraries (e.g., mysql.connector) for connecting to MySQL.
Use a prepared statement approach to prevent SQL injection vulnerabilities.
Here's an improved version assuming you're using mysql.connector:

python
Copy code
import mysql.connector

def connect_to_database():
    try:
        cnx = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return cnx
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return None

# Example usage:
cnx = connect_to_database()
# ... your database interaction code ...
cnx.close()  # Close the connection after use
Find-and-Replace Approach (Less Secure, Use with Caution)

Warning: This approach is less secure than environment variables and should only be used if absolutely necessary (e.g., local development). Exposing database credentials in code could lead to security breaches.

Create a Configuration File (config.py):

Store the database credentials in a separate file.

python
Copy code
host = "localhost"
user = "your_username"
password = "your_password"
database = "password_manager"
Find-and-Replace in app.py:

Use string manipulation (e.g., replace) to update the connection parameters.

python
Copy code
# config.py (assumed to be in the same directory)
from config import host, user, password, database
