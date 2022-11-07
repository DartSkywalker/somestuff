import sqlite3
import random
import string
import datetime

# Global variables
db_name = 'passwords.db'
db_table = 'passwords'
db_columns = ['id', 'description', 'password', 'date']


# Functions
def create_db():
    """Create the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS ' + db_table + '(id INTEGER PRIMARY KEY, description TEXT, password TEXT, '
                                                   'date TEXT)')
    conn.commit()
    conn.close()


def add_password(description, password):
    """Add a password to the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ' + db_table + ' (description, password, date) VALUES (?, ?, ?)',
                   (description, password, datetime.datetime.now()))
    conn.commit()
    conn.close()


def get_passwords():
    """Get all passwords from the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + db_table)
    passwords = cursor.fetchall()
    conn.close()
    return passwords


def get_password(id):
    """Get a password from the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ' + db_table + ' WHERE id = ?', (id,))
    password = cursor.fetchone()
    conn.close()
    return password


def delete_password(id):
    """Delete a password from the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ' + db_table + ' WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def update_password(id, description, password):
    """Update a password in the database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('UPDATE ' + db_table + ' SET description = ?, password = ?, date = ? WHERE id = ?',
                   (description, password, datetime.datetime.now(), id))
    conn.commit()
    conn.close()


def generate_password(length):
    """Generate a random password"""
    password = ''
    for i in range(length):
        password += random.choice(string.ascii_letters + string.digits + string.punctuation)
    return password


def main():
    """Main function"""
    # Create the database
    create_db()

    # Show the interactive menu
    while True:
        print('''

        Syntax: 
        1. Generate a new password: gen <length> <description>
        2. Show all passwords: show
        3. Update a password: update <id> <password> <description>
        4. Delete a password: delete <id>
        5. Exit: exit
        
        ''')

        # Get user input
        user_input = input('[PyPass] >> ').split(' ')

        # Option 1: Generate a random password
        if user_input[0] == 'gen':
            # Check all arguments
            if len(user_input) < 3:
                print('Error: check your syntax')
                continue

            # Get the password length
            try:
                length = int(user_input[1])
            except ValueError:
                print('Error: the password length must be an integer')
                continue

            # Get the password description
            description = ' '.join(user_input[2:])

            # Generate a random password
            password = generate_password(length)

            # Add the password to the database
            add_password(description, password)

            # Show the password
            print('[PyPass] Password: ' + password)

        # Option 2: Show all passwords
        elif user_input[0] == 'show':
            # Get all passwords
            passwords = get_passwords()

            # Show all passwords
            for password in passwords:
                print(f'''
                {'-'*10}
                ID: {password[0]}
                Description: {password[1]}
                Password: {password[2]}
                Date: {password[3]}
                ''')

        # Option 3: Update a password
        elif user_input[0] == 'update':
            # Check all arguments
            if len(user_input) < 4:
                print('Error: check your syntax')
                continue

            # Get the password ID
            try:
                pass_id = int(user_input[1])
            except ValueError:
                print('Error: the password ID must be an integer')
                continue

            # Get the password description
            description = ' '.join(user_input[3:])

            # Get the password
            password = user_input[2]

            # Update the password in the database
            update_password(pass_id, description, password)

            # Show the password
            print(f'[PyPass] Password {pass_id} Updated: ' + password)

        # Option 4: Delete a password
        elif user_input[0] == 'delete':
            # Check all arguments
            if len(user_input) < 2:
                print('[PyPass] Error: check your syntax')
                continue

            # Get the password ID
            try:
                pass_id = int(user_input[1])
            except ValueError:
                print('[PyPass] Error: the password ID must be an integer')
                continue

            # Delete the password from the database
            delete_password(pass_id)

            # Show the password
            print(f'[PyPass] Password {pass_id} Deleted')

        # Option 5: Exit
        elif user_input[0] == 'exit':
            break


if __name__ == '__main__':
    main()
