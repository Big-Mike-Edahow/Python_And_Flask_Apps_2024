# init_db.py

import sqlite3

groceries = [
    "apples",
    "bananas",
    "clemintines",
    "dill",
    "eggs",
    "flour",
    "granola",
    "honey",
    "ice cream",
    "juice",
    "ketchup",
    "lemon",
    "margarine",
    "onion",
    "potatoes",
    "rosmary",
    "salt",
    "thyme",
    "vinegar",
    "watermelon",
    "pears",
    "cucumbers",
    "garlic",
    "carrots",
    "pastries",
    "eggplants",
    "milk",
    "coffee",
    "tea",
    "rice",
    "noodles",
    "lentils",
    "sweet potatoes",
    "strawberries",
    "cranberries",
    "mangos",
    "pappers",
    "zuccinis",
    "lime",
    "broth",
    "mushrooms",
    "chicken",
    "beef",
    "pork",
    "fish",
    "cream",
    "paprika",
    "tumeric",
    "cinamon",
    "pumpkin",
    "basil",
    "tomatoes",
    "bread",
    "cake",
    "chocolate",
    "gum",
    "pinapple",
    "oranges",
    "lettuce",
    "cheese",
    "cilantro",
]

groceries = sorted(groceries)

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

curs.execute("CREATE TABLE groceries (id INTEGER PRIMARY KEY, name TEXT);")
for i in range(len(groceries)):
    curs.execute("INSERT INTO groceries (name) VALUES (?)", [groceries[i]])
    print("added ", groceries[i])

conn.commit()
conn.close()
