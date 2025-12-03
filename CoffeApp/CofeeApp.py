import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# === Data Models ===
class Coffee:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class OrderItem:
    def __init__(self, coffee, quantity=1):
        self.coffee = coffee
        self.quantity = quantity

    @property
    def total_price(self):
        return self.coffee.price * self.quantity


class LoyaltySystem:
    def __init__(self):
        self.points = 0

    def earn_points(self, amount):
        earned = int(amount)
        self.points += earned

    def redeem_points(self):
        if self.points >= 10:
            self.points -= 10
            return 1.0
        return 0.0


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, coffee, quantity=1):
        for item in self.items:
            if item.coffee.name == coffee.name:
                item.quantity += quantity
                return
        self.items.append(OrderItem(coffee, quantity))

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def clear(self):
        self.items.clear()

    def total(self):
        return sum(item.total_price for item in self.items)


# === GUI ===
class CoffeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("☕ Coffee Heaven")
        self.root.geometry("850x550")
        self.root.config(bg="#2b2b2b")
        self.root.resizable(False, False)

        self.menu = [
            Coffee("Espresso", 2.5),
            Coffee("Double Espresso", 3.0),
            Coffee("Latte", 3.5),
            Coffee("Cappuccino", 3.0),
            Coffee("Americano", 2.0),
            Coffee("Cold Brew", 4.0)
        ]

        self.order = Order()
        self.loyalty = LoyaltySystem()

        self.create_widgets()
        self.update_order_display()

    # === GUI Setup ===
    def create_widgets(self):
        # --- Title ---
        title = tk.Label(
            self.root,
            text="☕ Welcome to Coffee Heaven ☕",
            font=("Segoe UI", 20, "bold"),
            bg="#2b2b2b",
            fg="#ffcc66"
        )
        title.pack(pady=10)

        # --- Frames ---
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Menu Section
        menu_frame = tk.LabelFrame(
            main_frame, text=" Coffee Menu ", font=("Segoe UI", 13, "bold"),
            bg="#3c3f41", fg="white", labelanchor="n", padx=10, pady=10
        )
        menu_frame.pack(side="left", fill="y", padx=10, pady=5)

        for coffee in self.menu:
            frame = tk.Frame(menu_frame, bg="#3c3f41")
            frame.pack(anchor="w", pady=4)
            label = tk.Label(frame, text=f"{coffee.name} - ${coffee.price:.2f}",
                             bg="#3c3f41", fg="white", font=("Segoe UI", 11))
            label.pack(side="left", padx=5)
            btn = tk.Button(frame, text="Add ☕", font=("Segoe UI", 10, "bold"),
                            bg="#ffcc66", fg="#2b2b2b",
                            activebackground="#ffd966", activeforeground="#2b2b2b",
                            command=lambda c=coffee: self.add_item(c))
            btn.pack(side="right", padx=5)

        # Order Section
        order_frame = tk.LabelFrame(
            main_frame, text=" Your Order ", font=("Segoe UI", 13, "bold"),
            bg="#3c3f41", fg="white", labelanchor="n", padx=10, pady=10
        )
        order_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        self.order_list = tk.Listbox(order_frame, font=("Consolas", 11),
                                     bg="#2b2b2b", fg="white", selectbackground="#ffcc66",
                                     selectforeground="#2b2b2b")
        self.order_list.pack(fill="both", expand=True, padx=10, pady=10)

        # Points Bar
        points_frame = tk.Frame(self.root, bg="#2b2b2b")
        points_frame.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(points_frame, text="🏆 Loyalty Points:", font=("Segoe UI", 11, "bold"),
                 bg="#2b2b2b", fg="#ffcc66").pack(side="left")
        self.points_var = tk.IntVar(value=0)
        self.points_bar = ttk.Progressbar(points_frame, maximum=100, variable=self.points_var, length=300)
        self.points_bar.pack(side="left", padx=10)
        self.points_label = tk.Label(points_frame, text="0 pts", font=("Segoe UI", 10),
                                     bg="#2b2b2b", fg="white")
        self.points_label.pack(side="left")

        # Control Buttons
        button_frame = tk.Frame(self.root, bg="#2b2b2b")
        button_frame.pack(fill="x", pady=5)

        self.create_button(button_frame, "🗑️ Clear Order", "#cc6666", self.clear_order).pack(side="left", padx=10)
        self.create_button(button_frame, "❌ Remove Item", "#f0ad4e", self.remove_item).pack(side="left", padx=10)
        self.create_button(button_frame, "💰 Checkout", "#99cc66", self.checkout).pack(side="right", padx=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Welcome to Coffee Heaven!",
                                     bg="#2b2b2b", fg="#dcdcdc", anchor="w")
        self.status_label.pack(fill="x", pady=5, padx=10)

    # === Button Helper ===
    def create_button(self, parent, text, color, command):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 11, "bold"),
                         bg=color, fg="white", activebackground="#ffd966",
                         relief="flat", padx=10, pady=5, cursor="hand2")

    # === Logic ===
    def update_order_display(self):
        self.order_list.delete(0, tk.END)
        if not self.order.items:
            self.order_list.insert(tk.END, "🛒 Your order is empty.")
        else:
            for item in self.order.items:
                self.order_list.insert(tk.END, f"{item.coffee.name:<15} x{item.quantity:<2} ${item.total_price:.2f}")
            self.order_list.insert(tk.END, "-" * 35)
            self.order_list.insert(tk.END, f"Total: ${self.order.total():.2f}")

        self.points_label.config(text=f"{self.loyalty.points} pts")
        self.points_var.set(min(self.loyalty.points, 100))

    def add_item(self, coffee):
        self.order.add_item(coffee)
        self.update_order_display()
        self.status_label.config(text=f"Added {coffee.name} to your order ☕")

    def remove_item(self):
        selection = self.order_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select an item to remove.")
            return
        index = selection[0]
        if index >= len(self.order.items):
            return
        self.order.remove_item(index)
        self.update_order_display()
        self.status_label.config(text="Item removed ❌")

    def clear_order(self):
        if messagebox.askyesno("Confirm", "Clear your entire order?"):
            self.order.clear()
            self.update_order_display()
            self.status_label.config(text="Order cleared 🗑️")

    def checkout(self):
        if not self.order.items:
            messagebox.showinfo("Empty", "Your order is empty!")
            return

        total = self.order.total()
        discount_code = simpledialog.askstring("Discount", "Enter discount code (COFFEE10/FIRSTBREW):")
        discount = 0

        if discount_code:
            code = discount_code.strip().upper()
            if code == "COFFEE10":
                discount = total * 0.10
            elif code == "FIRSTBREW":
                discount = 2.0
            else:
                messagebox.showwarning("Invalid", "Invalid discount code.")

        # Loyalty redemption
        use_points = False
        if self.loyalty.points >= 10:
            use_points = messagebox.askyesno("Loyalty", "Redeem 10 points for $1 off?")
        if use_points:
            discount += self.loyalty.redeem_points()

        final_total = max(0, total - discount)
        confirm = messagebox.askyesno(
            "Confirm Checkout",
            f"Total: ${total:.2f}\nDiscount: ${discount:.2f}\nFinal: ${final_total:.2f}\nProceed?"
        )

        if confirm:
            self.loyalty.earn_points(final_total)
            self.order.clear()
            self.update_order_display()
            messagebox.showinfo("Success", f"Order confirmed! 🎉\nYou earned points. Total points: {self.loyalty.points}")
            self.status_label.config(text="Order completed successfully ✅")


# === Run the App ===
if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeApp(root)
    root.mainloop()
