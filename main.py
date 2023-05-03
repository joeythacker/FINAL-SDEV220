import datetime
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
from matplotlib import pyplot as plt


# This class is used to define the name, ID, type, quantity, and expiration date of product.
class Product:
    def __init__(self, id, name, type, quantity, expiration_date):
        self.id = id
        self.name = name
        self.type = type
        self.quantity = quantity
        self.expiration_date = expiration_date


# This class keeps the inventory of the products
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product, expiration_date):
        product.expiration_date = expiration_date
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def filter_products_by_type(self, type):
        filtered_products = []
        for product in self.products:
            if product.type == type:
                filtered_products.append(product)
        return filtered_products

    def check_expired_products(self):
        current_date = datetime.date.today()
        expired_products = []
        for product in self.products:
            if product.expiration_date < current_date:
                expired_products.append(product)
        return expired_products

    def save_inventory(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                for product in self.products:
                    product_data = f"{product.id},{product.name},{product.type},{product.quantity}," \
                                   f"{product.expiration_date.strftime('%Y-%m-%d')}\n"
                    f.write(product_data)
    def load_inventory(self, filename):
        self.products = []
        with open(filename, "r") as f:
            for line in f:
                id, name, type, quantity, expiration_date = line.strip().split(',')
                expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
                product = Product(id, name, type, int(quantity), expiration_date)
                self.add_product(product, expiration_date)


class UI:
    def __init__(self):
        self.inventory = Inventory()
        self.current_user = None

        # Create main window
        self.window = Tk()
        self.window.title("Ivy Food Pantry Inventory System")
        self.window.geometry("800x600")

        # Create login screen
        self.create_login_screen()

        self.window.mainloop()

    def authenticate_user(self, username, password):
        # Check if the username and password are valid
        # For example, you could check if they match entries in a database
        # or if they match hardcoded values
        if username == "admin" and password == "password":
            return True
        else:
            return False

    def create_login_screen(self):
        # Create login screen
        self.clear_window()
        self.login_label = Label(self.window, text="Login", font=("Arial", 20))
        self.login_label.pack(pady=10)

        self.username_label = Label(self.window, text="Username:")
        self.username_label.pack()

        self.username_entry = Entry(self.window)
        self.username_entry.pack()

        self.password_label = Label(self.window, text="Password:")
        self.password_label.pack()

        self.password_entry = Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = Button(self.window, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.authenticate_user(username, password):
            self.current_user = username
            self.create_home_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def create_home_screen(self):
        # Create home screen
        self.clear_window()
        self.home_label = Label(self.window, text="Home", font=("Arial", 20))
        self.home_label.pack(pady=10)

        self.filter_type_label = Label(self.window, text="Filter by Type:")
        self.filter_type_label.pack()

        self.filter_type_entry = Entry(self.window)
        self.filter_type_entry.pack()

        self.filter_type_button = Button(self.window, text="Filter", command=self.filter_by_type)
        self.filter_type_button.pack(pady=10)

        self.display_graph_button = Button(self.window, text="Display Graph", command=self.display_graph)
        self.display_graph_button.pack(pady=10)

        self.item_output_button = Button(self.window, text="Item Output", command=self.item_output)
        self.item_output_button.pack(pady=10)

        self.item_input_button = Button(self.window, text="Item Input", command=self.item_input)
        self.item_input_button.pack(pady=10)

        self.logout_button = Button(self.window, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

        self.expired_products_button = Button(self.window, text="Show Expired Products",
                                              command=self.show_expired_products)
        self.expired_products_button.pack(pady=10)

        self.save_inventory_button = Button(self.window, text="Save Inventory", command=self.save_inventory)
        self.save_inventory_button.pack(pady=10)

        self.load_inventory_button = Button(self.window, text="Load Inventory", command=self.load_inventory)
        self.load_inventory_button.pack(pady=10)

        self.product_listbox = Listbox(self.window, width=80, height=20)
        self.product_listbox.pack(pady=10)

        self.update_product_list()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def filter_by_type(self):
        type = self.filter_type_entry.get()
        filtered_products = self.inventory.filter_products_by_type(type)
        self.update_product_list(filtered_products)

    def display_graph(self):
        product_types = {}
        for product in self.inventory.products:
            product_type = product.type
            if product_type in product_types:
                product_types[product_type] += 1
            else:
                product_types[product_type] = 1

        plt.bar(product_types.keys(), product_types.values())
        plt.title("Product Types")
        plt.xlabel("Type")
        plt.ylabel("Quantity")
        plt.show()

    def item_output(self):
        selected_product = self.product_listbox.curselection()
        if selected_product:
            selected_product = selected_product[0]
            product = self.inventory.products[selected_product]
            if product.quantity > 0:
                product.quantity -= 1
                self.update_product_list()
            else:
                messagebox.showerror("Error", "Product is out of stock.")

    def item_input(self):
        inventory_id = len(self.inventory.products) + 1
        name = simpledialog.askstring("Input", "Product name:", parent=self.window)
        product_type = simpledialog.askstring("Input", "Product type:", parent=self.window)
        quantity = simpledialog.askinteger("Input", "Quantity:", parent=self.window)
        expiration_date_str = simpledialog.askstring("Input", "Expiration date (yyyy-mm-dd):", parent=self.window)

        if name and product_type and quantity and expiration_date_str:
            expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d").date()
            product = Product(inventory_id, name, product_type, quantity, expiration_date)
            self.inventory.add_product(product, expiration_date)
            self.update_product_list()

    def update_product_list(self, products=None):
        self.product_listbox.delete(0, END)
        if not products:
            products = self.inventory.products
        for product in products:
            if product.expiration_date < datetime.date.today():
                item_text = f"{product.name} ({product.type}) - {product.quantity} (Expired)"
            else:
                item_text = f"{product.name} ({product.type}) - {product.quantity}"
            self.product_listbox.insert(END, item_text)

    def show_expired_products(self):
        expired_products = self.inventory.check_expired_products()
        self.update_product_list(expired_products)

    def save_inventory(self):
        self.inventory.save_inventory()

    def load_inventory(self):
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            self.inventory.load_inventory(filename)
            self.update_product_list()




if __name__ == "__main__":
    ui = UI()
