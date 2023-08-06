import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

class TeacherApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.root.title("Teacher Dashboard")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text='Attendance Records')
        self.notebook.add(self.frame2, text='Attendance Graph')

        # Load the attendance data
        self.df = pd.read_excel('attendance.xlsx')
        self.df_rows = self.df.index.tolist()  # Convert the DataFrame to a list of dictionaries

        # Create an entry widget for searching
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame1, textvariable=self.search_var)
        self.search_entry.pack(side='top', padx=10, pady=10)
        self.search_var.trace('w', self.search)

        # Create buttons for add, update, delete
        self.button_frame = ttk.Frame(self.frame1)
        self.button_frame.pack(side='top', fill='x')
        self.add_button = ttk.Button(self.button_frame, text='Add', command=self.add)
        self.add_button.pack(side='left')
        self.update_button = ttk.Button(self.button_frame, text='Update', command=self.update)
        self.update_button.pack(side='left')
        self.delete_button = ttk.Button(self.button_frame, text='Delete', command=self.delete)
        self.delete_button.pack(side='left')

        # Create the table
        self.update_table()

        # Bind the event to update the graph when switching to the 'Attendance Graph' tab
        self.notebook.bind('<ButtonRelease-1>', self.on_tab_changed)

    def update_table(self):
        # If the treeview already exists, clear it. Otherwise, create it.
        try:
            self.treeview
        except AttributeError:
            self.treeview = ttk.Treeview(self.frame1)
            self.treeview.pack(fill='both', expand=True)

            self.treeview["column"] = list(self.df.columns)
            self.treeview["show"] = "headings"

            for column in self.treeview["column"]:
                self.treeview.heading(column, text=column)
        else:
            for i in self.treeview.get_children():
                self.treeview.delete(i)

        # Update df_rows and repopulate the treeview
        self.df_rows = self.df.index.tolist()
        for idx in self.df_rows:
            row = self.df.loc[idx]
            self.treeview.insert("", "end", iid=str(idx), values=row.tolist())

    def search(self, *args):
        search_term = self.search_var.get()
        df_filtered = self.df[self.df['username'].str.contains(search_term)]
        self.df_rows = df_filtered.index.tolist()
        self.treeview.delete(*self.treeview.get_children())
        for idx in self.df_rows:
            row = self.df.loc[idx]
            self.treeview.insert("", "end", iid=str(idx), values=row.tolist())

    def add(self):
        new_data = {} 
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Attendance")
        add_window.geometry('300x200')

        for column in self.df.columns:
            label = tk.Label(add_window, text=column)
            label.pack()
            entry = tk.Entry(add_window)
            entry.pack()
            new_data[column] = entry  

        add_button = tk.Button(add_window, text="Add", command=lambda: self.save_new_record(new_data, add_window))
        add_button.pack()

    def save_new_record(self, new_data, add_window):
        values = [entry.get() for entry in new_data.values()]

        if not all(values):
            messagebox.showwarning("Incomplete Entry", "Please fill in all fields.")
            return

        new_record = pd.DataFrame([values], columns=self.df.columns)
        self.df = pd.concat([self.df, new_record], ignore_index=True)
        self.df_rows = self.df.to_dict('records')  # Update df_rows with the new record

        self.update_table()
        self.save_to_file()
        messagebox.showinfo("Success", "Attendance record added successfully.")
        add_window.destroy()

    def update(self):
        # Get the selected item from the treeview
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return

        # Get the values of the selected record
        selected_values = self.treeview.item(selected_item[0], "values")

        # Create a new window with entry fields for each column, pre-filled with the current values
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Attendance")
        update_window.geometry('300x200')

        entry_widgets = {}  # Dictionary to store the entry widgets
        for idx, column in enumerate(self.df.columns):
            label = tk.Label(update_window, text=column)
            label.grid(row=idx, column=0)
            entry = tk.Entry(update_window)
            entry.insert(0, selected_values[idx])  # Pre-fill with current values
            entry.grid(row=idx, column=1)
            entry_widgets[column] = entry  # Store the entry widget in the dictionary

        # Update button to save the changes
        update_button = tk.Button(update_window, text="Update",
                              command=lambda: self.save_changes(entry_widgets, selected_item, update_window))
        update_button.grid(row=len(self.df.columns), column=0, columnspan=2)
                            

        update_window.geometry('300x200')

        entry_widgets = {}  # Dictionary to store the entry widgets
        for idx, column in enumerate(self.df.columns):
            label = tk.Label(update_window, text=column)
            label.grid(row=idx, column=0)
            entry = tk.Entry(update_window)
            entry.insert(0, selected_values[idx])  # Pre-fill with current values
            entry.grid(row=idx, column=1)
            entry_widgets[column] = entry  # Store the entry widget in the dictionary

        # Update button to save the changes
        update_button = tk.Button(update_window, text="Update",
                              command=lambda: self.save_changes(entry_widgets, selected_item, update_window))
        update_button.grid(row=len(self.df.columns), column=0, columnspan=2)

    def save_changes(self, entry_widgets, selected_item, update_window):
        new_values = [entry.get() for entry in entry_widgets.values()]

        if not all(new_values):
            messagebox.showwarning("Incomplete Entry", "Please fill in all fields.")
            return

        selected_index = int(selected_item[0])  # Convert iid to an integer
        self.df.loc[selected_index] = new_values
        self.df_rows = self.df.index.tolist()  # Update df_rows

        self.update_table()
        self.save_to_file()
        messagebox.showinfo("Success", "Attendance record updated successfully.")
        update_window.destroy()

    def delete(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            selected_index = int(selected_item[0])  # Convert iid to an integer
            self.df.drop(selected_index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.df_rows = self.df.index.tolist() 
            self.update_table()
            self.save_to_file()
            messagebox.showinfo("Success", "Attendance record deleted successfully.")

    def save_to_file(self):
        self.df.to_excel('attendance.xlsx', index=False)

    def plot_attendance(self):
        # Clear the frame
        for widget in self.frame2.winfo_children():
            widget.destroy()

        # Create a figure and a set of subplots
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Assuming 'username' is the column with names and 'attendance' is the column with attendance data
        attendance_count = self.df['username'].value_counts()
        attendance_count.plot(kind='bar', ax=ax)

        # Add the plot to the tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_tab_changed(self, event):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 1:  # Attendance Graph tab
            self.plot_attendance()

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Teacher')
    root.geometry('925x500+300+200')
    root.config(bg='#fff')

    heading = tk.Label(root, text="Teacher Dashboard",  fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.pack()

    app = TeacherApp(root)
    root.mainloop()

