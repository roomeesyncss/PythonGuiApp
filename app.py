import tkinter as tk
from tkinter import ttk
import pyodbc
from datastructure import  *

class RecipeAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe App")

        # Set a hex color for the background
        self.root.configure(bg="#2E4053")

        # Create and set the geometry of the window
        self.root.geometry("800x600")

        # Create a label for the title
        title_label = tk.Label(self.root, text="Recipe App", font=("Helvetica", 25, "bold"), fg="#E74C3C", bg="#2E4053")
        title_label.pack(pady=20)

        # Create a main frame as a container
        main_frame = tk.Frame(self.root, bg="#34495E")
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create tabs for different functionalities
        tab_control = ttk.Notebook(main_frame)

        login_tab = ttk.Frame(tab_control)
        signup_tab = ttk.Frame(tab_control)

        tab_control.add(login_tab, text='Login')
        tab_control.add(signup_tab, text='Signup')

        tab_control.pack(expand=1, fill="both", pady=20)

        # Login Tab
        self.create_login_tab(login_tab)

        # Signup Tab
        self.create_signup_tab(signup_tab)
        self.connection = self.create_database_connection()

    def create_database_connection(self):
        # Implement your database connection logic here
        server_name = 'localhost\\SQLEXPRESS01'
        database_name = 'master'
        trusted_connection = 'yes'
        connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
        connection = pyodbc.connect(connection_string)
        return connection

    def create_login_tab(self, login_tab):
        login_tab.configure(style='TabStyle.TFrame')

        login_label = tk.Label(login_tab, text="Login", font=("Helvetica", 18, "bold"), fg="#3498DB", bg="#34495E")
        login_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create login form elements
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        username_label = tk.Label(login_tab, text="Username", font=("Helvetica", 12), fg="#ECF0F1", bg="#34495E")
        password_label = tk.Label(login_tab, text="Password", font=("Helvetica", 12), fg="#ECF0F1", bg="#34495E")

        username_entry = tk.Entry(login_tab, textvariable=self.username_var, font=("Helvetica", 12))
        password_entry = tk.Entry(login_tab, textvariable=self.password_var, show="*", font=("Helvetica", 12))

        login_button = tk.Button(login_tab, text="Login", command=self.login_action, font=("Helvetica", 12), bg="#3498DB", fg="#ECF0F1")

        # Arrange login form elements using grid
        username_label.grid(row=1, column=0, padx=20, pady=10, sticky=tk.W)
        username_entry.grid(row=1, column=1, padx=20, pady=10)

        password_label.grid(row=2, column=0, padx=20, pady=10, sticky=tk.W)
        password_entry.grid(row=2, column=1, padx=20, pady=10)

        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_signup_tab(self, signup_tab):
        signup_tab.configure(style='TabStyle.TFrame')  # Set the style for the frame

        signup_label = tk.Label(signup_tab, text="Signup", font=("Helvetica", 18, "bold"), fg="#27AE60", bg="#34495E")
        signup_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create signup form elements
        self.new_username_var = tk.StringVar()
        self.new_email_var = tk.StringVar()
        self.new_password_var = tk.StringVar()

        new_username_label = tk.Label(signup_tab, text="New Username", font=("Helvetica", 12), fg="#ECF0F1", bg="#34495E")
        new_email_label = tk.Label(signup_tab, text="Email", font=("Helvetica", 12), fg="#ECF0F1", bg="#34495E")
        new_password_label = tk.Label(signup_tab, text="New Password", font=("Helvetica", 12), fg="#ECF0F1", bg="#34495E")

        new_username_entry = tk.Entry(signup_tab, textvariable=self.new_username_var, font=("Helvetica", 12))
        new_email_entry = tk.Entry(signup_tab, textvariable=self.new_email_var, font=("Helvetica", 12))
        new_password_entry = tk.Entry(signup_tab, textvariable=self.new_password_var, show="*", font=("Helvetica", 12))

        signup_button = tk.Button(signup_tab, text="Signup", command=self.signup_action, font=("Helvetica", 12), bg="#27AE60", fg="#ECF0F1")

        # Arrange signup form elements using grid
        new_username_label.grid(row=1, column=0, padx=20, pady=10, sticky=tk.W)
        new_username_entry.grid(row=1, column=1, padx=20, pady=10)

        new_email_label.grid(row=2, column=0, padx=20, pady=10, sticky=tk.W)
        new_email_entry.grid(row=2, column=1, padx=20, pady=10)

        new_password_label.grid(row=3, column=0, padx=20, pady=10, sticky=tk.W)
        new_password_entry.grid(row=3, column=1, padx=20, pady=10)

        signup_button.grid(row=4, column=0, columnspan=2, pady=10)

    def login_action(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if self.does_user_exist(username, password):
            print("Login successful!")
            self.on_login()
        else:
            print("Login failed. User not found.")

    def signup_action(self):
        new_username = self.new_username_var.get()
        new_email = self.new_email_var.get()
        new_password = self.new_password_var.get()

        self.create_user(new_username, new_email, new_password)
        print("Signup successful!")
        self.on_login()

    def on_login(self):
        # Add actions to perform after a successful login
        # In this case, creating the recipe tree frame

        # Check if the recipe tree frame exists before destroying it
        if hasattr(self, 'tree_frame'):
            self.tree_frame.destroy()

        self.create_recipe_tree_frame()

    def create_recipe_tree_frame(self):
        recipe_tree = build_recipe_tree(self.connection)

        # Check if the tree frame exists before destroying it
        if hasattr(self, 'tree_frame'):
            self.tree_frame.destroy()

        # Create the recipe tree frame
        self.tree_frame = tk.Frame(self.root, padx=20, pady=20)
        self.tree_frame.pack(expand=True, fill="both")

        # Recipe tree widgets
        label_recipe_tree = tk.Label(self.tree_frame, text="Recipe Tree", font=("Helvetica", 16, "bold"))
        label_recipe_tree.pack(pady=10)

        text_recipe_tree = tk.Text(self.tree_frame, wrap="none", height=15, width=70)
        text_recipe_tree.pack(pady=10)

        # Populate the recipe tree text widget (you may format it as needed)
        self.populate_recipe_tree_text(text_recipe_tree, recipe_tree.root)

    def populate_recipe_tree_text(self, text_widget, node, depth=0):
        text_widget.insert(tk.END, f"{depth * '    '}+ {node.recipe['MealType']} - {node.recipe['RecipeName']}\n")
        for child in node.children:
            self.populate_recipe_tree_text(text_widget, child, depth + 1)

    def does_user_exist(self, username, password):
        # Implement database query to check if the user exists
        # Replace the following connection details with your actual values
        server_name = 'localhost\\SQLEXPRESS01'
        database_name = 'master'
        trusted_connection = 'yes'

        connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        hashed_password = self.hash_password(password)
        check_user_query = f"SELECT * FROM Users WHERE Name = '{username}' AND Password = '{hashed_password}'"

        try:
            cursor.execute(check_user_query)
            return cursor.fetchone() is not None
        except pyodbc.Error as e:
            print(f"Error fetching user data: {e}")
            exit(-1)

    def create_user(self, username, email, password):
        # Implement database query to create a new user
        # Replace the following connection details with your actual values
        server_name = 'localhost\\SQLEXPRESS01'
        database_name = 'master'
        trusted_connection = 'yes'

        connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection={trusted_connection};'
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        user_id_query = "SELECT ISNULL(MAX(UserID), 0) + 1 FROM Users"
        cursor.execute(user_id_query)
        user_id = cursor.fetchone()[0]

        hashed_password = self.hash_password(password)

        insert_user_query = f"INSERT INTO Users (UserID, Name, Email, Password) VALUES ({user_id}, '{username}', '{email}', '{hashed_password}')"

        self.execute_sql_query(cursor, insert_user_query)

    def execute_sql_query(self, cursor, query):
        try:
            cursor.execute(query)
            cursor.commit()
        except pyodbc.Error as e:
            print(f"Error executing SQL query: {e}")
            exit(-1)

    def hash_password(self, password):
        hash_value = 5381
        for char in password:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        return str(hash_value)

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeAppGUI(root)

    root.mainloop()
