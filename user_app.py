
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import os
import bcrypt
from database import create_db, get_db_connection
import sqlite3

create_db()

def register_user():
    """Register a new user."""
    username = simpledialog.askstring("Register", "Enter username:")
    password = simpledialog.askstring("Register", "Enter password:")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, 'user'))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def login_user():
    """Login a user and open the user dashboard."""
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND role='user'", (username,))
    user = cursor.fetchone()
    
    conn.close()


    if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
        user_dashboard(user[0], username)  
    else:
        messagebox.showerror("Error", "Invalid credentials.")

def user_dashboard(user_id, username):
    """User dashboard to upload resumes."""
    def upload_resume():
        job_title = simpledialog.askstring("Upload Resume", "Enter job title:")
        file_path = filedialog.askopenfilename(title="Select Resume", filetypes=(("PDF files", "*.pdf"), ("Word files", "*.docx")))

        if not job_title or not file_path:
            messagebox.showerror("Error", "Please provide both job title and resume file.")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO resumes (user_id, job_title, file_path) VALUES (?, ?, ?)", (user_id, job_title, file_path))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Resume uploaded successfully!")

    user_window = tk.Toplevel()
    user_window.title(f"User Dashboard - {username}")
    user_window.geometry("400x200")

    frame = ttk.Frame(user_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=f"Welcome {username}!", font=("Arial", 14)).pack(pady=10)
    ttk.Button(frame, text="Upload Resume", command=upload_resume, width=20).pack(pady=15)

    user_window.mainloop()

def main():
    root = tk.Tk()
    root.title("User - Resume Management System")
    root.geometry("400x200")

    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="User - Resume Management System", font=("Arial", 16)).pack(pady=20)
    ttk.Button(frame, text="Register", command=register_user, width=20).pack(pady=10)
    ttk.Button(frame, text="Login as User", command=login_user, width=20).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
