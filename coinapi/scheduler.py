import time
import requests
import sqlite3


def check_alerts():
    while True:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM alerts")
        alerts = cur.fetchall()

        for alert in alerts:
            currency = alert[2]
            quote_currency = alert[3]
            anchor_price = alert[4]
            operation = alert[5]

            url = f"https://rest.coinapi.io/v1/exchangerate/{currency}/{quote_currency}"
            headers = {
                "X-CoinAPI-Key": "F0D3DED3-87EA-4E09-8375-2F08BAB6B298"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                current_price = data['rate']

                if operation == 'above' and current_price > anchor_price:
                    print(f"Alert! {currency} is above {quote_currency}: {current_price}")
                elif operation == 'under' and current_price < anchor_price:
                    print(f"Alert! {currency} is under {quote_currency}: {current_price}")
            else:
                print("Error fetching exchange rate.")

        conn.close()

        time.sleep(1)


if __name__ == "__main__":
    check_alerts()
