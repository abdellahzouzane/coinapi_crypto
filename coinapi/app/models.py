import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
print("Database opened successfully")


# name: name of the alert
# currency: e.g. BTC (You should use CoinApi asset ID) - Base currency
# quote_currency: e.g. USD (You should use CoinApi asset ID) - Quote currency
# anchor_price: The price of the operation
# operation: accepts 2 values "above" and "under"
cur.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        name TEXT,
        currency TEXT,
        quote_currency TEXT,
        anchor_price REAL,
        operation TEXT
    )
''')

conn.commit()

print("Table created successfully")
conn.close()
