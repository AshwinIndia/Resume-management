import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from tkinter import ttk
import PyPDF2
import docx
import bcrypt
from database import create_db, get_db_connection
import sqlite3

create_db()

def register_admin():
    username = simpledialog.askstring("Register Admin", "Enter admin username:")
    password = simpledialog.askstring("Register Admin", "Enter admin password:")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, 'admin'))
        conn.commit()
        messagebox.showinfo("Success", "Admin registration successful!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    finally:
        conn.close()

def login_admin():
    username = simpledialog.askstring("Login", "Enter admin username:")
    password = simpledialog.askstring("Login", "Enter admin password:")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND role='admin'", (username,))
    admin = cursor.fetchone()
    
    conn.close()

    if admin and bcrypt.checkpw(password.encode('utf-8'), admin[2]):
        admin_dashboard()
    else:
        messagebox.showerror("Error", "Invalid admin credentials.")

def admin_dashboard():
    def search_resumes():
        keyword = simpledialog.askstring("Search Resumes", "Enter keyword to search in resumes:")
        
        if not keyword:
            messagebox.showwarning("Warning", "Please enter a keyword.")
            return

        search_results.delete(*search_results.get_children())

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT r.id, u.username, r.file_path FROM resumes r JOIN users u ON r.user_id = u.id")
        resumes = cursor.fetchall()
        
        for resume_id, username, file_path in resumes:
            content = extract_text(file_path)
            if keyword.lower() in content.lower():
                search_results.insert("", "end", values=(username, file_path))
        
        conn.close()

    def extract_text(file_path):
        content = ""
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    content = ''.join(page.extract_text() for page in reader.pages if page.extract_text())
            elif file_path.endswith('.docx'):
                doc = docx.Document(file_path)
                content = ''.join(para.text for para in doc.paragraphs)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
        return content

    admin_window = Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    
    frame = ttk.Frame(admin_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
    ttk.Button(frame, text="Search Resumes by Keyword", command=search_resumes).pack(pady=10)

    global search_results
    search_results = ttk.Treeview(frame, columns=("Username", "File Path"), show="headings")
    search_results.heading("Username", text="Username")
    search_results.heading("File Path", text="File Path")
    
    search_results.column("Username", width=150)
    search_results.column("File Path", width=400)
    
    search_results.pack(fill="both", expand=True)

    admin_window.mainloop()

def main():
    root = tk.Tk()
    root.title("Admin - Resume Management System")
    root.geometry("400x200")

    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Admin - Resume Management System", font=("Arial", 16)).pack(pady=20)
    ttk.Button(frame, text="Register as Admin", command=register_admin, width=20).pack(pady=10)
    ttk.Button(frame, text="Login as Admin", command=login_admin, width=20).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
