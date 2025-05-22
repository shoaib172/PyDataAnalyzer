import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class SingarCorner:
    def __init__(self, root):
        self.root = root
        self.root.title("Singar Corner")
        self.db = sqlite3.connect('singar_corner.db')
        self.cursor = self.db.cursor()
        self.create_tables()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.product_frame = tk.Frame(self.notebook)
        self.sales_frame = tk.Frame(self.notebook)
        self.purchase_frame = tk.Frame(self.notebook)
        self.stock_frame = tk.Frame(self.notebook)

        self.notebook.add(self.product_frame, text="Products")
        self.notebook.add(self.sales_frame, text="Sales")
        self.notebook.add(self.purchase_frame, text="Purchases")
        self.notebook.add(self.stock_frame, text="Stock")

        self.product_widgets()
        self.sales_widgets()
        self.purchase_widgets()
        self.stock_widgets()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL
            );
        ''')
        self.db.commit()

    def product_widgets(self):
        tk.Label(self.product_frame, text="Product Name:").pack()
        self.product_name_entry = tk.Entry(self.product_frame)
        self.product_name_entry.pack()

        tk.Label(self.product_frame, text="Product Price:").pack()
        self.product_price_entry = tk.Entry(self.product_frame)
        self.product_price_entry.pack()

        tk.Label(self.product_frame, text="Product Quantity:").pack()
        self.product_quantity_entry = tk.Entry(self.product_frame)
        self.product_quantity_entry.pack()

        tk.Button(self.product_frame, text="Add Product", command=self.add_product).pack()

    def sales_widgets(self):
        tk.Label(self.sales_frame, text="Product ID:").pack()
        self.sales_product_id_entry = tk.Entry(self.sales_frame)
        self.sales_product_id_entry.pack()

        tk.Label(self.sales_frame, text="Quantity:").pack()
        self.sales_quantity_entry = tk.Entry(self.sales_frame)
        self.sales_quantity_entry.pack()

        tk.Button(self.sales_frame, text="Make Sale", command=self.make_sale).pack()

    def purchase_widgets(self):
        tk.Label(self.purchase_frame, text="Product ID:").pack()
        self.purchase_product_id_entry = tk.Entry(self.purchase_frame)
        self.purchase_product_id_entry.pack()

        tk.Label(self.purchase_frame, text="Quantity:").pack()
        self.purchase_quantity_entry = tk.Entry(self.purchase_frame)
        self.purchase_quantity_entry.pack()

        tk.Button(self.purchase_frame, text="Make Purchase", command=self.make_purchase).pack()

    def stock_widgets(self):
        tk.Button(self.stock_frame, text="Check Stock", command=self.check_stock).pack()

    def add_product(self):
        try:
            name = self.product_name_entry.get()
            price = float(self.product_price_entry.get())
            quantity = int(self.product_quantity_entry.get())
            self.cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
            self.db.commit()
            messagebox.showinfo("Success", "Product added successfully!")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid price and quantity.")

    def make_sale(self):
        try:
            product_id = int(self.sales_product_id_entry.get())
            quantity = int(self.sales_quantity_entry.get())

            self.cursor.execute('SELECT price, quantity FROM products WHERE id = ?', (product_id,))
            product = self.cursor.fetchone()

            if not product:
                messagebox.showerror("Error", "Product ID does not exist.")
                return

            price, current_stock = product

            if quantity > current_stock:
                messagebox.showerror("Error", "Not enough stock available.")
                return

            total = price * quantity
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute('INSERT INTO sales (product_id, quantity, total, date) VALUES (?, ?, ?, ?)',
                                (product_id, quantity, total, date))
            self.cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (current_stock - quantity, product_id))

            self.db.commit()
            messagebox.showinfo("Sale Completed", f"Sale recorded. Total: ₹{total:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Product ID and Quantity.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def make_purchase(self):
        try:
            product_id = int(self.purchase_product_id_entry.get())
            quantity = int(self.purchase_quantity_entry.get())

            self.cursor.execute('SELECT price, quantity FROM products WHERE id = ?', (product_id,))
            product = self.cursor.fetchone()

            if not product:
                messagebox.showerror("Error", "Product ID does not exist.")
                return

            price, current_stock = product
            total = price * quantity
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.cursor.execute('INSERT INTO purchases (product_id, quantity, total, date) VALUES (?, ?, ?, ?)',
                                (product_id, quantity, total, date))
            self.cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (current_stock + quantity, product_id))

            self.db.commit()
            messagebox.showinfo("Purchase Completed", f"Purchase recorded. Total: ₹{total:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Product ID and Quantity.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    def check_stock(self):
        self.cursor.execute('SELECT id, name, quantity FROM products')
        products = self.cursor.fetchall()
        stock_info = "\n".join([f"ID: {pid}, Name: {name}, Stock: {qty}" for pid, name, qty in products])
        messagebox.showinfo("Stock Info", stock_info if stock_info else "No products found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SingarCorner(root)
    root.mainloop()
