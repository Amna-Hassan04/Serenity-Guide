import tkinter as tk
from tkinter import messagebox
from flask import Flask, request, jsonify
import re

def validate_email(email):
 # Regular expression for validating an Email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regex
    return re.match(email_regex, email) is not None

def check_email():
    email = email_entry.get()
    
    if validate_email(email):
        messagebox.showinfo("Success", "Email is valid!")
    else:
        messagebox.showerror("Error", "Invalid email entered.")

root = tk.Tk()
root.title("Email Validator")

email_label = tk.Label(root, text="Enter your email:")
email_label.pack()

email_entry = tk.Entry(root, width=50)
email_entry.pack()

check_button = tk.Button(root, text="Check Email", command=check_email)
check_button.pack()

root.mainloop()


app = Flask(__name__)

def validate_email(email):
    # Regular expression for validating an Email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regex
    return re.match(email_regex, email) is not None

@app.route('/validate-email', methods=['POST'])
def validate_email_api():
    email = request.json['email']
    
    if validate_email(email):
        return jsonify({'result': 'valid'})
    else:
        return jsonify({'result': 'invalid'})

if __name__ == '__main__':
    app.run(debug=True)