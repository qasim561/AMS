import tkinter as tk
import pandas as pd
import pickle
from PIL import ImageTk, Image

username = ""

# Function to verify login
def login():
    global username
    global root
    username = entry_username.get()
    password = entry_password.get()
    
    df = pd.read_excel('login.xlsx')
    df['username'] = df['username'].astype(str)
    df['password'] = df['password'].astype(str)
    
    user_exists = df[(df['username'] == username) & (df['password'] == password)].shape[0] == 1
    print(f"User exists: {user_exists}")
    
    if user_exists:
        label_result.config(text="Login Successful", fg="green")
        root.destroy()  # destroy the login window
        with open('username.pkl', 'wb') as f:
            pickle.dump(username, f)
        import student  # import your dashboard script
        student.dashboard(username)  # open the dashboard with the logged-in username
    else:
        label_result.config(text="Login Failed", fg="red")



# Function to handle signup
# Function to handle signup
def signup():
    global username
    global root
    username = entry_username.get()
    password = entry_password.get()
    
    # If the fields are empty, return and show an error message
    if username == "" or password == "":
        label_result.config(text="Both fields must be filled.", fg="red")
        return
    
    # Load excel file
    df = pd.read_excel('login.xlsx')

    # Check if username already exists
    if df['username'].str.contains(username).any():
        label_result.config(text="Username already exists.", fg="red")
    else:
        # Add the new username and password to the DataFrame
        new_data = pd.DataFrame({"username": [username], "password": [password]})
        df = pd.concat([df, new_data], ignore_index=True)

        # Save the DataFrame back to Excel
        df.to_excel('login.xlsx', index=False)

        label_result.config(text="Registration Successful. Please Login", fg="green")


def main():
    global root
    global entry_username
    global entry_password
    global label_result

    root = tk.Tk()
    root.title('Student Login')
    root.geometry('925x500+300+200')
    root.config(bg='#fff')
    root.resizable(False,False)

    image = Image.open('login.png')  
    bg_image = ImageTk.PhotoImage(image)

    bg_label = tk.Label(root, image=bg_image, bg='white')
    bg_label.place(x=50, y=50)

    heading = tk.Label(root, text="Student Login",  fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.pack()

    label_username = tk.Label(root, text="Username")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password")
    label_password.pack()
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    label_result = tk.Label(root)
    label_result.pack()

    button_login = tk.Button(root, text="Login", command=login)
    button_login.pack()

    # Signup button
    button_signup = tk.Button(root, text="Signup", command=signup)
    button_signup.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
