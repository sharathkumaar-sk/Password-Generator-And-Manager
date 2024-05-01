import random
import string
import mysql.connector
import csv
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from prettytable import PrettyTable
from cryptography.fernet import Fernet
import os
import stdiomask

localhost=""
User_Name=""
User_Password=""
Database_Name=""
authenticated = False

def authenticate_user():
    global User_Name, User_Password
    print("\n\t\t\t\t\t\tWelcome To Password Genrator And Manager\n")
    User_Name = input("Enter your database username: ")
    User_Password = stdiomask.getpass("Enter your database password: ", mask='*')

    try:
        # Establish database connection for authentication
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )
        authenticated = connection.is_connected()
        return authenticated
    except mysql.connector.Error as e:
        clear_screen()
        print(f"Authentication failed: {e}")
        authenticated=False
        return False

def authenticate_user2():
    global User_Name, User_Password
    print("\n\t\t\t\t\t\tEXPORT PASSWORD\n")
    User_Name = input("Enter your database username: ")
    User_Password = stdiomask.getpass("Enter your database password: ", mask='*')

    try:
        # Establish database connection for authentication
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )
        authenticated = connection.is_connected()
        return authenticated
    except mysql.connector.Error as e:
        clear_screen()
        print(f"Authentication failed: {e}")
        authenticated=False
        return False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_encryption_key():
    return Fernet.generate_key()

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def generate_password(length, characters):
    if characters == '1':
        characters_set = string.digits
    elif characters == '2':
        characters_set = string.ascii_letters
    elif characters == '3':
        characters_set = string.ascii_letters + string.digits
    elif characters == '4':
        characters_set = string.ascii_letters + string.digits + string.punctuation
    else:
        print("Invalid character type. Using default set (letters, digits, punctuation).")
        characters_set = string.ascii_letters + string.digits + string.punctuation

    if characters in ['3', '4']:
        # Ensure at least one lowercase, one uppercase, and one digit character
        password = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase) + random.choice(string.digits)
        remaining_length = length - 3
        password += ''.join(random.choice(characters_set) for _ in range(remaining_length))
        password = ''.join(random.sample(password, len(password)))  # Shuffle the password
    else:
        password = ''.join(random.choice(characters_set) for _ in range(length))

    return password

def select(length=None, characters=None):
    while True:
        try:
            if length is None:
                length = int(input("\nEnter the number of characters for the password: "))
                if length <= 0:
                    print("Length must be a positive integer.")
                    continue
            if characters is None:
                print("""\nCharacter Sets:
        1. Only numbers
        2. Only letters (lowercase and uppercase)
        3. Letters and digits
        4. Letters, digits, and special characters""")
                characters = input("\nChoose a character set (1/2/3/4):")
                if characters not in ['1', '2', '3', '4']:
                    print("Invalid character set choice.\n")
                    continue
            password = generate_password(length, characters)
            return password, length, characters
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def dis_password():
    connection = None
    cursor = None
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query to select all passwords
            sql = "SELECT app_name, username, password_eny, `key` FROM passwords"
            cursor.execute(sql)

            # Fetch all the rows
            passwords = cursor.fetchall()

            if passwords:
                table = PrettyTable(["App Name", "Username", "Password"])
                for row in passwords:
                    app_name = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    key = row[3]
                    # Decrypt the password using retrieved key
                    decrypted_password = decrypt_password(encrypted_password, key)
                    table.add_row([app_name, username, decrypted_password])
                print(table)
            else:
                print("No passwords found.")
        else:
            print("Connection is not established.")

    except mysql.connector.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()



def retry_password(length, characters):
    password, _, _ = select(length, characters)
    return password

def save_password(app_name, username, password):
    connection = None  # Initialize the connection variable
    try:
        # Generate encryption key
        key = generate_encryption_key()

        # Encrypt the password
        encrypted_password = encrypt_password(password, key)

        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )
        
        cursor = connection.cursor()
        
        # Check if the same password already exists
        select_sql = "SELECT password_eny, `key` FROM passwords"
        cursor.execute(select_sql)
        existing_passwords = cursor.fetchall()
        
        for existing_password, existing_key in existing_passwords:
            decrypted_existing_password = decrypt_password(existing_password, existing_key)
            if decrypted_existing_password == password:
                print("Password already exists.")
                return
        
        # Insert new password
        insert_sql = "INSERT INTO passwords (app_name, username, password_eny, `key`) VALUES (%s, %s, %s, %s)"
        insert_val = (app_name, username, encrypted_password, key)
        cursor.execute(insert_sql, insert_val)
        
        connection.commit()
        print("Password saved successfully.")
        
    except mysql.connector.Error as e:
        print(f"An error occurred while saving password: {e}")
        
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def exit_generate_password():
    response = input("Do you want to return to the main menu? (Y/N): ").lower()
    if response == "y":
        clear_screen()
        main_menu()
    elif response == "n":
        generate_password_menu()
    else:
        print("Invalid option.")

def view_passwords():
    clear_screen()
    print("\n\t\t\t\t\t\tVIEW PASSWORDS\n")
    dis_password()
    input("\nPress Enter to return to the Manage Passwords menu...")

def edit_password():
    clear_screen()
    print("\n\t\t\t\t\t\tEDIT PASSWORDS\n")
    dis_password()
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )

        cursor = connection.cursor()

        # Prompt the user to enter the application name
        app_name = input("Enter the name of the application to edit the password: ")

        # Query to select password by app name
        sql = "SELECT app_name, username, password_eny, `key` FROM passwords WHERE app_name = %s"
        val = (app_name,)
        cursor.execute(sql, val)

        # Fetch the row
        password = cursor.fetchone()

        if password:
            # Retrieve existing password details
            old_username = password[1]
            encrypted_password = password[2]
            key = password[3]

            # Decrypt the password using retrieved key
            decrypted_password = decrypt_password(encrypted_password, key)
            old_password = decrypted_password

            # Prompt the user to enter new username and password
            new_username = input(f"Enter new username for {app_name} (leave empty to keep current): ")
            new_password = input(f"Enter new password for {app_name} (leave empty to keep current): ")

            # Update username and/or password if provided
            if new_username.strip():
                old_username = new_username
            if new_password.strip():
                old_password = new_password

            # Encrypt the new password
            new_encrypted_password = encrypt_password(old_password, key)

            # Query to update password details
            update_sql = "UPDATE passwords SET username = %s, password_eny = %s WHERE app_name = %s"
            update_val = (old_username, new_encrypted_password, app_name)
            cursor.execute(update_sql, update_val)

            # Commit changes
            connection.commit()

            print("Password updated successfully.")
            dis_password()
        else:
            print("No password found for the specified application name.")

    except mysql.connector.Error as e:
        print(f"An error occurred while editing password: {e}")

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("\nConnection closed.")
    input("\nPress Enter to return to the Manage Passwords menu...")

def delete_password():
    clear_screen()
    print("\n\t\t\t\t\t\tDELETE PASSWORDS\n")
    dis_password()
    try:
        app_name = input("\nEnter the application name to delete: ")
        conf = input(f"Do you want to delete the password for {app_name}? (Y/N): ").lower()
        if conf == "y":
            # Establish database connection
            connection = mysql.connector.connect(
                host=localhost,
                user=User_Name,
                password=User_Password,
                database=Database_Name
            )

            cursor = connection.cursor()

            # Query to delete password by app name
            sql = "DELETE FROM passwords WHERE app_name = %s"
            val = (app_name,)
            cursor.execute(sql, val)

            # Commit changes
            connection.commit()
        
            # Check if any rows were affected
            if cursor.rowcount > 0:
                print("\nPassword deleted successfully.")
                dis_password()
            else:
                print("No password found for the specified application name.")
        else:
            print("Password deletion canceled.")
            while True:
                user_input = input("\nPress Enter to return to the Manage Passwords menu...")
                if user_input == "":
                    manage_passwords_menu()
                else:
                    print("Invalid input. Please press Enter to continue.")

    except mysql.connector.Error as e:
        print(f"An error occurred while deleting password: {e}")

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("\nConnection closed.")
    input("\nPress Enter to return to the Manage Passwords menu...")

def search_password():
    clear_screen()
    print("\n\t\t\t\t\t\tSEARCH PASSWORDS\n")
    try:
        app_name = input("Enter the application name to search for: ")
        
        # Establish database connection
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )

        cursor = connection.cursor()

        # Query to select password by app name
        sql = "SELECT app_name, username, password_eny, `key` FROM passwords WHERE app_name = %s"
        val = (app_name,)
        cursor.execute(sql, val)

        # Fetch the row
        password = cursor.fetchone()

        if password:
            table = PrettyTable(["App Name", "Username", "Password"])
            app_name = password[0]
            username = password[1]
            encrypted_password = password[2]
            key = password[3]
            
            # Decrypt the password using retrieved key
            decrypted_password = decrypt_password(encrypted_password, key)
            table.add_row([app_name, username, decrypted_password])
            print("Password found:")
            print(table)
        else:
            print("No password found for the specified application name.")

    except mysql.connector.Error as e:
        print(f"An error occurred while searching password: {e}")

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("\nConnection closed.")
    input("\nPress Enter to return to the Manage Passwords menu...")

def export_passwords():
    clear_screen()
    authenticated = False
    while not authenticated:
        authenticated = authenticate_user2()
    clear_screen()
    print("\n\t\t\t\t\tEXPORT PASSWORDS\n")
    try:
        filename = input("Enter a file name to export as (Example.txt, Example.csv, Example.pdf, Example.db): ")
        
        # Extract the file extension
        file_extension = filename.split(".")[-1].lower()
        # Establish database connection
        connection = mysql.connector.connect(
            host=localhost,
            user=User_Name,
            password=User_Password,
            database=Database_Name
        )

        cursor = connection.cursor()

        # Query to select all passwords
        sql = "SELECT app_name, username, password_eny, `key` FROM passwords"
        cursor.execute(sql)

        # Fetch all the rows
        passwords = cursor.fetchall()

        if passwords:
            if file_extension == "csv":
                # Export as CSV
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    # Write title in the middle of the CSV
                    writer.writerow([" " * 2 + "PASSWORD MANAGER"])
                    writer.writerow([])
                    writer.writerow(["App Name", "Username", "Decrypted Password"])
                    for row in passwords:
                        app_name = row[0]
                        username = row[1]
                        encrypted_password = row[2]
                        key = row[3]
                        
                        # Decrypt the password using retrieved key
                        decrypted_password = decrypt_password(encrypted_password, key)
                        writer.writerow([app_name, username, decrypted_password])
                print(f"Passwords exported to {filename} successfully.")
            elif file_extension == "pdf":
                # Export as PDF
                content = []
                title = "PASSWORD MANAGER"
                title_style = ParagraphStyle(
                    name='Title',
                    fontName='Helvetica-Bold',
                    fontSize=20,
                    alignment=1
                )
                title_paragraph = Paragraph(title, title_style)
                content.append(title_paragraph)
                content.append(Spacer(1, 20))  # Add some space after title

                # Create table data
                data = [["App Name", "Username", "Decrypted Password"]]
                for row in passwords:
                    app_name = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    key = row[3]
                    
                    # Decrypt the password using retrieved key
                    decrypted_password = decrypt_password(encrypted_password, key)
                    data.append([app_name, username, decrypted_password])

                # Create the table
                table = Table(data)

                # Add style to the table
                style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

                table.setStyle(style)
                content.append(table)
                # Create PDF document
                doc = SimpleDocTemplate(filename, pagesize=letter)
                doc.build(content)
                print(f"Passwords exported to {filename} successfully.")

            elif file_extension == "db":
                # Export as SQLite database
                conn = sqlite3.connect(filename)
                c = conn.cursor()
                c.execute('''CREATE TABLE IF NOT EXISTS passwords
                             (app_name TEXT, username TEXT, decrypted_password TEXT)''')
                
                # Insert title into the database
                title = "PASSWORD MANAGER"
                c.execute("INSERT INTO passwords (app_name) VALUES (?)", (title,))
                
                # Insert data into the database
                for row in passwords:
                    app_name = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    key = row[3]
                    
                    # Decrypt the password using retrieved key
                    decrypted_password = decrypt_password(encrypted_password, key)
                    
                    # Insert decrypted password into the database
                    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (app_name, username, decrypted_password))
                
                conn.commit()
                conn.close()
                print(f"Passwords exported to {filename} successfully.")
            else:
                # Export as plain text (default)
                table = PrettyTable(["App Name", "Username", "Decrypted Password"])
                for row in passwords:
                    app_name = row[0]
                    username = row[1]
                    encrypted_password = row[2]
                    key = row[3]
                    
                    # Decrypt the password using retrieved key
                    decrypted_password = decrypt_password(encrypted_password, key)
                    table.add_row([app_name, username, decrypted_password])

                with open(filename, 'w') as file:
                    title = "PASSWORD MANAGER"
                    padding = (80 - len(title)) // 2  # Assuming 80 characters width
                    # Add centered title to the file
                    file.write(" " * padding + title + "\n\n")
                    file.write(str(table))
                
                print(f"Passwords exported to {filename} successfully.")
        else:
            print("No passwords found.")

    except mysql.connector.Error as e:
        print(f"An error occurred while exporting passwords: {e}")

    finally:
        # Close cursor and connection
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
            print("\nConnection closed.")
    input("\nPress Enter to return to the Manage Passwords menu...")
    
def main_menu():
    global authenticated
    while not authenticated:
        authenticated = authenticate_user()
    while True:
        clear_screen()
        print("\n\t\t\t\t\t\tMAIN MENU\n")
        print("1. Generate Password")
        print("2. Manage Passwords")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            generate_password_menu()
        elif choice == "2":
            manage_passwords_menu()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def generate_password_menu():
    clear_screen()
    while True:
        print("\n\t\t\t\t\t\tGENERATE PASSWORD MENU\n")
        try:
            app_name = input("Enter the name of the application: ")
            username = input(f"Enter your username for the {app_name}: ")
            ue = input("Do you have a password (Y/N)? ").lower()
            if ue == "y":
                password = input("Enter your password: ")
            else:
                password, length, characters = select()

            while True:
                print("\nGenerated Password:", password)
                print("\n1. Retry")
                print("2. Save")
                print("3. Exit")
                option = input("Choose an option (1/2/3): ").lower()

                if option == "1":
                    if ue != "y":
                        password = retry_password(length, characters)
                        if password is None:
                            break
                    else:
                        password = input("Enter your password: ")
                elif option == "2":
                    save_password(app_name, username, password)
                    break
                elif option == "3":
                    if exit_generate_password():
                        break
                    else:
                        continue
                else:
                    print("Invalid option. Please choose from 1, 2, or 3.")

            if not exit_generate_password():
                break  # Exit the generate_password_menu loop and return to the main menu

        except Exception as e:
            print("An error occurred:", e)

def manage_passwords_menu():
    while True:
        clear_screen()
        print("\n\t\t\t\t\t\tMANAGE PASSWORDS MENU\n")
        print("1. View Passwords")
        print("2. Edit Password")
        print("3. Delete Password")
        print("4. Search Password")
        print("5. Export Passwords")
        print("6. Main Menu")
        choice = input("Choose an option (1/2/3/4/5/6): ")

        if choice == "1":
            view_passwords()
        elif choice == "2":
            edit_password()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            search_password()
        elif choice == "5":
            export_passwords()
        elif choice == "6":
            cc=input("Do you want to return to the main menu? (Y/N): ").lower()
            if cc == "y":
                main_menu()
            else:
                manage_passwords_menu()
        else:
            print("Invalid choice. Please enter a valid option.")

def main():
    main_menu()

if __name__ == "__main__":
    main()
