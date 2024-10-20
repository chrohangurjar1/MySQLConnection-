import tkinter as tk
from tkinter import messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error


class MySQLConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def create_connection(self):
        """Create a database connection."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.connection.is_connected()
        except Error as e:
            print(f"The error '{e}' occurred")
            return False

    def close_connection(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query):
        """Execute a single query."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            return "Query executed successfully"
        except Error as e:
            return f"The error '{e}' occurred"

    def fetch_query(self, query):
        """Fetch data from the database."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            return f"The error '{e}' occurred"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("MySQL Database Interface")
        self.root.geometry("600x400")

        # Create UI components
        self.create_ui()

        # Initialize the database connection
        self.db_connection = None

    def create_ui(self):
        """Create the user interface."""
        tk.Label(self.root, text="Host:").pack(pady=5)
        self.host_entry = tk.Entry(self.root)
        self.host_entry.pack(pady=5)

        tk.Label(self.root, text="Database:").pack(pady=5)
        self.db_entry = tk.Entry(self.root)
        self.db_entry.pack(pady=5)

        tk.Label(self.root, text="User:").pack(pady=5)
        self.user_entry = tk.Entry(self.root)
        self.user_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Connect", command=self.connect_to_db).pack(pady=10)

        tk.Label(self.root, text="SQL Query:").pack(pady=5)
        self.query_entry = tk.Entry(self.root, width=70)
        self.query_entry.pack(pady=5)

        tk.Button(self.root, text="Execute", command=self.execute_query).pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self.root, width=70, height=10)
        self.result_text.pack(pady=10)

    def connect_to_db(self):
        """Connect to the database."""
        host = self.host_entry.get()
        database = self.db_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        self.db_connection = MySQLConnection(host, database, user, password)
        if self.db_connection.create_connection():
            messagebox.showinfo("Connection", "Connected to MySQL DB successfully!")
            self.result_text.insert(tk.END, "Connected to MySQL DB successfully!\n")
        else:
            messagebox.showerror("Connection", "Failed to connect to MySQL DB.")

    def execute_query(self):
        """Execute the provided SQL query."""
        if not self.db_connection or not self.db_connection.connection:
            messagebox.showerror("Error", "Please connect to the database first.")
            return

        query = self.query_entry.get()
        if not query.strip():
            messagebox.showerror("Error", "Please enter a query.")
            return

        result = self.db_connection.execute_query(query)

        if "successfully" in result:
            self.result_text.insert(tk.END, result + "\n")
        else:
            self.result_text.insert(tk.END, result + "\n")

        self.query_entry.delete(0, tk.END)

    def close_app(self):
        """Close the application."""
        if self.db_connection:  # Check if db_connection is not None
            self.db_connection.close_connection()
        self.root.destroy()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)  # Handle window closing
    root.mainloop()
