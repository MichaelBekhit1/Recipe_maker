import tkinter as tk
from tkinter import simpledialog
import sqlite3

class Dashboard:
    def __init__(self, master):
        self.master = master
        master.title("Dashboard")

        # create buttons
        self.add_recipe_button = tk.Button(master, text="Add Recipe", command=self.add_recipe)
        self.make_recipe_button = tk.Button(master, text="Make Recipe", command=self.make_recipe)
        self.add_ingredient_button = tk.Button(master, text="Add Ingredient", command=self.add_ingredient)
        self.menu_button = tk.Button(master, text="Menu", command=self.menu)

        # arrange buttons in a grid layout
        self.add_recipe_button.grid(row=0, column=0, padx=10, pady=10)
        self.make_recipe_button.grid(row=0, column=1, padx=10, pady=10)
        self.add_ingredient_button.grid(row=1, column=0, padx=10, pady=10)
        self.menu_button.grid(row=1, column=1, padx=10, pady=10)

        # create database connection and table
        self.conn = sqlite3.connect("recipes.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS recipes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            ingredients TEXT
                         )""")
        self.conn.commit()

    def add_recipe(self):
        # get recipe name from user
        recipe_name = simpledialog.askstring("Add Recipe", "Enter recipe name:")

        # get ingredients from user
        ingredients = []
        while True:
            ingredient = simpledialog.askstring("Add Recipe", "Enter ingredient name (leave blank to finish):")
            if not ingredient:
                break
            quantity = simpledialog.askfloat("Add Recipe", f"Enter quantity of {ingredient}:")
            ingredients.append((ingredient, quantity))

        # add recipe to database
        self.c.execute("INSERT INTO recipes (name, ingredients) VALUES (?, ?)", (recipe_name, str(ingredients)))
        self.conn.commit()

        print(f"Recipe '{recipe_name}' added with ingredients: {ingredients}")

    def make_recipe(self):
        print("Make Recipe button pressed")
    
    def add_ingredient(self):
        print("Add Ingredient button pressed")
    
    def menu(self):
        # retrieve recipes from database and display in a messagebox
        self.c.execute("SELECT name, ingredients FROM recipes")
        recipes = self.c.fetchall()
        recipe_text = "\n".join([f"{name}: {ingredients}" for name, ingredients in recipes])
        simpledialog.messagebox.showinfo("Recipes", recipe_text)

    def __del__(self):
        # close database connection when object is deleted
        self.conn.close()

root = tk.Tk()
dashboard = Dashboard(root)
root.mainloop()
