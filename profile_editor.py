import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json

class ProfileEditor:

    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Rule Profile Editor")
        self.window.geometry("500x500")

        self.rules = {}
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.window, columns=("Rule", "Value"), show="headings")
        self.tree.heading("Rule", text="Rule")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Add", command=self.add_rule).pack(side="left")
        tk.Button(btn_frame, text="Delete", command=self.delete_rule).pack(side="left")
        tk.Button(btn_frame, text="Load", command=self.load_profile).pack(side="left")
        tk.Button(btn_frame, text="Save", command=self.save_profile).pack(side="left")

    def add_rule(self):
        rule = simpledialog.askstring("Rule Name", "Enter rule name:")
        value = simpledialog.askfloat("Rule Value", "Enter rule value:")

        if rule and value is not None:
            self.tree.insert("", "end", values=(rule, value))

    def delete_rule(self):
        selected = self.tree.selection()
        for item in selected:
            self.tree.delete(item)

    def load_profile(self):
        file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file:
            return

        with open(file) as f:
            data = json.load(f)

        self.tree.delete(*self.tree.get_children())

        for rule, value in data.items():
            self.tree.insert("", "end", values=(rule, value))

    def save_profile(self):
        file = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json")])
        if not file:
            return

        updated = {}

        for row in self.tree.get_children():
            rule, value = self.tree.item(row)["values"]
            updated[rule] = float(value)

        with open(file, "w") as f:
            json.dump(updated, f, indent=4)

        messagebox.showinfo("Saved", "Profile saved successfully.")