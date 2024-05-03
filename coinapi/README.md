
# Crypto Alert Project
API for managing cryptocurrency alerts

## Features
- Create cryptocurrency alerts
- Get cryptocurrency alerts
- Update cryptocurrency alerts
- Delete cryptocurrency alerts


## Available endpoints
Here are the entry points available for the API with a brief explanation of each:

-POST /alerts: Creates a new cryptocurrency alert. The alert data must be sent in the request body in JSON format with the following keys:
name: Alert name
currency: Base currency
quote_currency: Quotation currency
anchor_price: Anchor price
operation: Either “above” or “under”.

-GET /alerts: Get a list of all alerts. Returns a message indicating that alerts are retrieved.

-POST /alerts/<currency_id>: Update a cryptocurrency alert based on its identifier. Returns an update message.

-DELETE /alerts/<currency_id> : Delete a cryptocurrency alert by its identifier. Returns a message indicating that the alert has been deleted.

# Request examples
'{"name": "Bitcoin Alert", "currency": "BTC", "quote_currency": "USD", "anchor_price": 40000, "operation": "above"}'

## Database structure
The API uses a SQLite database to store cryptocurrency alerts. The alert table is created with the following fields:

- **name** : Alert name.
- currency**: Base currency (e.g. BTC). Use the CoinAPI asset ID.
- quote_currency**: Quote currency (e.g. USD). Use CoinAPI asset ID.
- **anchor_price**: Anchor price of the operation.
- **operation**: Can take 2 values: “above” and “under”.

The following code creates the `alerts` table in the SQLite database:

python
import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
print(“Database opened successfully”)

# Create alert table
conn.execute('CREATE TABLE alerts (name TEXT, currency TEXT, anchor_price REAL, operation TEXT)')
print(“Table created successfully”)

## Installation
To install the API, you first need to install Python and Flask. Then you can set up a virtual environment to isolate your project's dependencies.

```bash

# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate # For Linux/macOS
env\Scripts\activate # For Windows

# Install Flask
pip install flask
