import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os


class ExpenseTracker:
    def __init__(self, filename):
        self.filename = filename
        self.expenses = self.load_expenses(self.filename)

    def add_expense(self, category, description, amount, date, location, payment_method):
        amount = float(amount)
        self.expenses.append({
            "category": category,
            "description": description,
            "amount": amount,
            "date": date,
            "location": location,
            "payment_method": payment_method
        })

    def view_expenses(self):
        if not self.expenses:
            return "No expenses recorded yet."
        else:
            expense_list = []
            for i, expense in enumerate(self.expenses, 1):
                amount = float(expense['amount'])
                amount_with_rupee = "₹{:.2f}".format(amount)
                date = expense.get('date', 'N/A')
                location = expense.get('location', 'N/A')
                payment_method = expense.get('payment_method', 'N/A')
                if amount < 50:
                    category_color = 'darkgreen'
                    category_text = 'Safe Expenses'
                elif 50 <= amount <= 300:
                    category_color = 'skyblue'
                    category_text = 'Average Zone'
                else:
                    category_color = 'red'
                    category_text = 'High Expenses'
                expense_info = f"{i}. Date: {date}, Category: {expense['category']}, Description: {expense['description']}, Amount: {amount_with_rupee}, Location: {location}, Payment Method: {payment_method}, Category: {category_text}"
                expenses_list.insert(tk.END, expense_info)
                if i <= expenses_list.size():
                    expenses_list.itemconfig(i - 1, {'bg': category_color, 'fg': 'white'})
                expense_list.append(expense_info)
            return "\n".join(expense_list)

    def calculate_total_expenses(self):
        total = sum(float(expense["amount"]) for expense in self.expenses)
        return total

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            return "Expense deleted successfully."
        else:
            return "Invalid expense index."

    def load_expenses(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                return [dict(row) for row in reader]
        except FileNotFoundError:
            return []

    def save_expenses(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ['category', 'description', 'amount', 'date', 'location', 'payment_method']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)
        messagebox.showinfo("Expense Tracker", "Expenses saved successfully!")


def create_gui(username):
    root = tk.Tk()
    root.title(f"SpendWise™ - {username}'s Expense Tracker")

    def on_closing():
        tracker.save_expenses()
        root.destroy()

    def update_expenses_list():
        for i in expenses_tree.get_children():
            expenses_tree.delete(i)
        for i, expense in enumerate(tracker.expenses, 1):
            amount = float(expense['amount'])
            amount_with_rupee = "₹{:.2f}".format(amount)
            date = expense.get('date', 'N/A')
            location = expense.get('location', 'N/A')
            payment_method = expense.get('payment_method', 'N/A')
            if amount < 50:
                category_color = 'darkgreen'
                category_text = 'Safe Expenses'
            elif 50 <= amount <= 300:
                category_color = 'skyblue'
                category_text = 'Average Zone'
            else:
                category_color = 'red'
                category_text = 'High Expenses'
            expenses_tree.insert('', 'end', values=(
            i, date, expense['category'], expense['description'], amount_with_rupee, location, payment_method,
            category_text), tags=(category_color,))

    def update_total_expenses():
        total_label.config(text=f"Total Expenses: ₹{tracker.calculate_total_expenses():.2f}")

    def add_expense():
        category = category_entry.get()
        description = description_entry.get()
        amount = amount_entry.get()
        date = date_entry.get()
        location = location_entry.get()
        payment_method = payment_method_entry.get()
        if category and description and date and location and payment_method:
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("Expense Tracker", "Please enter a valid amount.")
                return
            try:
                datetime.strptime(date, "%d/%m/%Y")
                tracker.add_expense(category, description, amount, date, location, payment_method)
                update_expenses_list()
                update_total_expenses()
                messagebox.showinfo("Expense Tracker", "Expense added successfully!")
            except ValueError:
                messagebox.showerror("Expense Tracker", "Please enter a valid date in DD/MM/YYYY format.")
        else:
            messagebox.showerror("Expense Tracker", "Please fill in all fields.")

    def delete_selected_expense():
        selected_item = expenses_tree.selection()
        if selected_item:
            index = expenses_tree.index(selected_item[0])  # Get the index of the selected item
            result = tracker.delete_expense(index)
            if result == "Expense deleted successfully.":
                update_expenses_list()
                update_total_expenses()
                messagebox.showinfo("Expense Tracker", result)
            else:
                messagebox.showerror("Expense Tracker", result)
        else:
            messagebox.showerror("Expense Tracker", "Please select an expense to delete.")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(root, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    category_entry = ttk.Combobox(root, values=["Food", "Transportation", "Rent/Mortgage", "Utilities", "Entertainment",
                                                "Health", "Education", "Miscellaneous"])
    category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    description_entry = tk.Entry(root)
    description_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Date (DD/MM/YYYY):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    date_entry = tk.Entry(root)
    date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    location_entry = tk.Entry(root)
    location_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(root, text="Payment Method:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    payment_method_entry = ttk.Combobox(root,
                                        values=["Cash", "UPI", "Credit Card", "Debit Card", "Bank Transfer", "Cheque"])
    payment_method_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    add_button = tk.Button(root, text="Add Expense", command=add_expense)
    add_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

    delete_selected_button = tk.Button(root, text="Delete Selected Expense", command=delete_selected_expense)
    delete_selected_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")

    save_button = tk.Button(root, text="Save Expenses", command=tracker.save_expenses)
    save_button.grid(row=5, column=2, padx=10, pady=5, sticky="w")

    total_label = tk.Label(root, text="")
    total_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")

    expenses_tree = ttk.Treeview(root, columns=(
    "Index", "Date", "Category", "Description", "Amount", "Location", "Payment Method", "Category Type"))
    expenses_tree.heading("#1", text="Index")
    expenses_tree.heading("#2", text="Date")
    expenses_tree.heading("#3", text="Category")
    expenses_tree.heading("#4", text="Description")
    expenses_tree.heading("#5", text="Amount")
    expenses_tree.heading("#6", text="Location")
    expenses_tree.heading("#7", text="Payment Method")
    expenses_tree.heading("#8", text="Category Type")
    expenses_tree["show"] = "headings"

    expenses_tree.column("#1", width=50)
    expenses_tree.column("#2", width=100)
    expenses_tree.column("#3", width=100)
    expenses_tree.column("#4", width=200)
    expenses_tree.column("#5", width=100)
    expenses_tree.column("#6", width=100)
    expenses_tree.column("#7", width=150)
    expenses_tree.column("#8", width=100)

    expenses_tree.tag_configure('darkgreen', background='darkgreen', foreground='white')
    expenses_tree.tag_configure('skyblue', background='skyblue')
    expenses_tree.tag_configure('red', background='red', foreground='white')

    expenses_tree.grid(row=6, columnspan=3, padx=10, pady=5, sticky="w")

    bottom_label = tk.Label(root, text="Thank you for using SpendWise™!\n~ Safeer T.S", justify="left")
    bottom_label.grid(row=8, columnspan=3, padx=10, pady=5, sticky="w")

    update_expenses_list()
    update_total_expenses()
    root.geometry("1000x700")
    root.mainloop()


def get_username():
    username_dialog = tk.Tk()
    username_dialog.title("Enter Username")

    def submit_username():
        global username
        username = username_entry.get()
        if username:
            username_dialog.destroy()
            csv_filename = f'{username}_expenses.csv'
            global tracker
            tracker = ExpenseTracker(csv_filename)
            create_gui(username)
        else:
            messagebox.showerror("Expense Tracker", "Username is required.")

    tk.Label(username_dialog, text="Enter your username:").pack()
    username_entry = tk.Entry(username_dialog)
    username_entry.pack()
    submit_button = tk.Button(username_dialog, text="Submit", command=submit_username)
    submit_button.pack()

    username_dialog.mainloop()


if __name__ == "__main__":
    username = None  # Initialize username as None
    get_username()
