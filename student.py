import tkinter as tk
import pandas as pd
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import login
import pickle
from PIL import ImageTk, Image

def mark_attendance():
    global username

    with open('username.pkl', 'rb') as f:
        username = pickle.load(f)
    df = pd.read_excel('attendance.xlsx')
    if df['date'].dtype == 'object':
        df['date'] = pd.to_datetime(df['date']).dt.date
    today = datetime.now().date()
    new_record = pd.DataFrame({"username": [username], "date": [today], "attendance": ['P']})
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_excel('attendance.xlsx', index=False)
    messagebox.showinfo("Success", "Attendance marked successfully")

def view_attendance():
    global username
    global right_frame
    df = pd.read_excel('attendance.xlsx')
    df = df[df["username"] == username]
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    attendance_counts = df['date'].value_counts().sort_index()
    figure = plt.Figure(figsize=(6,5), dpi=100)
    ax = figure.add_subplot(111)
    chart_type = FigureCanvasTkAgg(figure, right_frame)
    chart_type.get_tk_widget().pack()
    attendance_counts.plot(kind='bar', legend=True, ax=ax)
    ax.set_title('Attendance Dates')

def dashboard(username):
    global root
    global right_frame

    root = tk.Tk()
    root.geometry('800x600')
    root.title('Student Dashboard')
    heading = tk.Label(root, text="Student Dashboard",  fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.pack()

    image = Image.open('login.png')  
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image, bg='white')
    bg_label.place(x=50, y=50)

    frame1 = tk.Frame(root,bg='skyblue',padx=50,pady=50)
    frame1.pack(side=tk.LEFT, padx=10, anchor='w')

    label_attendance = tk.Label(frame1, text="Mark Your Attendance", fg='darkblue')
    label_attendance.pack()
    button_mark_attendance = tk.Button(frame1, text="Mark Attendance", command=mark_attendance)
    button_mark_attendance.pack()

    right_frame = tk.Frame(root,bg='skyblue',padx=50,pady=50)
    right_frame.pack(side=tk.RIGHT, padx=10, anchor='e')

    label_view_attendance = tk.Label(right_frame, text="View Your Attendance",fg='darkblue')
    label_view_attendance.pack()
    button_view_attendance = tk.Button(right_frame, text="View Attendance", command=view_attendance)
    button_view_attendance.pack()

    # Logout button
    logout_button = tk.Button(root, text="Logout", command=lambda: logout(root))
    logout_button.pack()

    root.mainloop()

def logout(root):
    root.destroy()  # This will close the student.py window
    login.main()  # And then run the login.py main function again

if __name__ == "__main__":
    username = "Your_username"  # Replace with your logic of obtaining username
    dashboard(username)
