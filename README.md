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


## Getting Started

### Prerequisites
Python 3.x installed (Download Python)


Text editor or IDE of your choice (List of Source Code Editors)


### Installation

Clone the Repository:
```bash
git clone [https://github.com/sharathkumaar/Password-Generator_And_Manager.git]
```

### Setup Database

**Create MySQL Database**
- Access your MySQL server administration tool (e.g., phpMyAdmin, MySQL Workbench).
- Create a new database and name it appropriately (e.g., password_manager).
- Create passwords Table Within the newly created database, execute the following SQL statement to create the passwords table:
```bash
CREATE TABLE IF NOT EXISTS passwords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password_hash BLOB NOT NULL,
    `key` VARCHAR(255) NOT NULL
);
```
**Create Database User**
- Create a new user specifically for the password manager application and grant it the necessary privileges.
Important:
Avoid using the root user for application access.
- Grant privileges on the password_manager database (e.g., SELECT, INSERT, UPDATE, DELETE) to this new user.
- Assign a strong password to the newly created user and store it securely (avoid hardcoding passwords in code).
  
**Connect to Database**
- Connecting to the Database in app.py (Secure Method)
- Replace all the placeholder values in app.py with your actual database credentials. Avoid hardcoding sensitive information directly into the code to enhance security.
```bash
connection = mysql.connector.connect(
    host = "localhost"  # Replace with your database host address
    user = "UserName"  # Replace with your database username
    password = "User_Password"  # Replace with your database password
    database = "Database_Name"  # Replace with your database name
)
```
- Use find and replace method or create a global variable with actual database credentials at the begining of the code.
- Save the changes to app.py.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Script

```bash
python app.py
```

Follow the on-screen instructions to generate passwords, manage your password database, and utilize export functionalities.


**Contributing:**

We welcome contributions! Please feel free to submit pull requests or open issues for any enhancements or bug fixes.

**License:**

This project is licensed under the MIT License. See the LICENSE file for details.
