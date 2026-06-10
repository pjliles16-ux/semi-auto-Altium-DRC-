import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

from version import get_full_version
from core.parser import parse_altium_rules
from core.validator import validate_rules
from core.report import export_pdf
from core.session import save_session


class PCBValidatorGUI:

    def __init__(self, root):
        self.root = root
        self.root.title(get_full_version())
        self.root.geometry("1150x700")

        self.board_file = None
        self.required_rules = {}

        self.setup_dark_mode()
        self.create_tabs()

    # ------------------- UI -------------------

    def setup_dark_mode(self):
        self.root.configure(bg="#1e1e1e")
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        fieldbackground="#2b2b2b")

        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="white")

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.validation_tab = tk.Frame(self.notebook, bg="#1e1e1e")
        self.rules_tab = tk.Frame(self.notebook, bg="#1e1e1e")

        self.notebook.add(self.validation_tab, text="Validation")
        self.notebook.add(self.rules_tab, text="DRC Requirements")

        self.create_validation_tab()
        self.create_rules_tab()

    # ------------------- Validation Tab -------------------

    def create_validation_tab(self):
        toolbar = tk.Frame(self.validation_tab, bg="#1e1e1e")
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Load Board", command=self.load_board).pack(side="left")
        tk.Button(toolbar, text="Validate", command=self.validate).pack(side="left")
        tk.Button(toolbar, text="Export PDF", command=self.export).pack(side="left")
        tk.Button(toolbar, text="Save Session", command=self.save_session_file).pack(side="left")

        columns = ("Rule", "Required", "Actual", "Status")
        self.validation_tree = ttk.Treeview(self.validation_tab, columns=columns, show="headings")

        for col in columns:
            self.validation_tree.heading(col, text=col)
            self.validation_tree.column(col, width=220)

        self.validation_tree.pack(fill="both", expand=True)

    # ------------------- Rules Tab -------------------

    def create_rules_tab(self):
        toolbar = tk.Frame(self.rules_tab, bg="#1e1e1e")
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Add Rule", command=self.add_rule).pack(side="left")
        tk.Button(toolbar, text="Edit Rule", command=self.edit_rule).pack(side="left")
        tk.Button(toolbar, text="Delete Rule", command=self.delete_rule).pack(side="left")
        tk.Button(toolbar, text="Save Requirements", command=self.save_profile).pack(side="left")
        tk.Button(toolbar, text="Load Requirements", command=self.load_profile).pack(side="left")

        columns = ("Rule", "Required Value")
        self.rules_tree = ttk.Treeview(self.rules_tab, columns=columns, show="headings")

        for col in columns:
            self.rules_tree.heading(col, text=col)
            self.rules_tree.column(col, width=300)

        self.rules_tree.pack(fill="both", expand=True)

    # ------------------- Rule Management -------------------

    def add_rule(self):
        rule = simpledialog.askstring("Rule Name", "Enter rule name:")
        value = simpledialog.askfloat("Required Value", "Enter required value:")

        if rule and value is not None:
            self.required_rules[rule] = value
            self.refresh_rules_table()

    def edit_rule(self):
        selected = self.rules_tree.selection()
        if not selected:
            return

        item = selected[0]
        rule, value = self.rules_tree.item(item)["values"]

        new_value = simpledialog.askfloat("Edit Rule",
                                          f"Enter new value for {rule}:",
                                          initialvalue=float(value))

        if new_value is not None:
            self.required_rules[rule] = new_value
            self.refresh_rules_table()

    def delete_rule(self):
        selected = self.rules_tree.selection()
        for item in selected:
            rule = self.rules_tree.item(item)["values"][0]
            if rule in self.required_rules:
                del self.required_rules[rule]

        self.refresh_rules_table()

    def refresh_rules_table(self):
        self.rules_tree.delete(*self.rules_tree.get_children())
        for rule, value in self.required_rules.items():
            self.rules_tree.insert("", "end", values=(rule, value))

    # ------------------- Profile Save/Load -------------------

    def save_profile(self):
        file = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON Files", "*.json")])
        if not file:
            return

        with open(file, "w") as f:
            json.dump(self.required_rules, f, indent=4)

        messagebox.showinfo("Saved", "Requirements saved.")

    def load_profile(self):
        file = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file:
            return

        with open(file) as f:
            self.required_rules = json.load(f)

        self.refresh_rules_table()
        messagebox.showinfo("Loaded", "Requirements loaded.")

    # ------------------- Validation Logic -------------------

    def load_board(self):
        self.board_file = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        messagebox.showinfo("Board Loaded", self.board_file)

    def validate(self):
        if not self.board_file:
            messagebox.showerror("Error", "Load a board first.")
            return

        if not self.required_rules:
            messagebox.showerror("Error", "Add DRC requirements first.")
            return

        actual = parse_altium_rules(self.board_file)
        results = validate_rules(self.required_rules, actual)

        self.display_results(results)

    def display_results(self, results):
        self.validation_tree.delete(*self.validation_tree.get_children())

        for r in results:
            tag = "fail" if r["status"] == "FAIL" else "pass"

            self.validation_tree.insert("", "end",
                                        values=(r["rule"],
                                                r["required"],
                                                r["actual"],
                                                r["status"]),
                                        tags=(tag,))

        self.validation_tree.tag_configure("fail", background="#5c1f1f")
        self.validation_tree.tag_configure("pass", background="#1f3d1f")

    # ------------------- Export & Session -------------------

    def export(self):
        export_pdf(self.validation_tree)

    def save_session_file(self):
        filename = save_session(self.validation_tree)
        messagebox.showinfo("Session Saved", filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = PCBValidatorGUI(root)
    root.mainloop()