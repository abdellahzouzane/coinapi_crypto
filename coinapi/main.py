import requests
import smtplib
from email.mime.text import MIMEText
import mariadb
from time import sleep

# Configuration CoinAPI
COIN_API_KEY = "F0D3DED3-87EA-4E09-8375-2F08BAB6B298"  #clé d'API CoinAPI
BTC_ALERT_THRESHOLD = 5000  # budget d'alerte en USD
BTC_PERCENTAGE_THRESHOLD = 1  # Par exemple, 1% de hausse
ALERT_INTERVAL = 30  # Délai de vérification en secondes

# Configuration SMTP
SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587
SMTP_USERNAME = "Abdellahzouzane@gmail.com" # mail qui permet d'envoyer des mails au clients
SMTP_PASSWORD = ""  # mot de passe d'application mail

# obtenir les e-mails des clients dans la BD
def get_client_emails():
    emails = []
    try:
        conn = mariadb.connect(
            host="localhost",
            user="root",
            password="duck",
            database="alert_crypto"
        )
        cursor = conn.cursor()

        # Récupérer toutes les adresses e-mail des clients
        cursor.execute("SELECT mail FROM client")
        emails = [row[0] for row in cursor.fetchall()]

    except mariadb.Error as err:
        print(f"Erreur lors de la récupération des e-mails des clients: {err}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return emails

# Fonction pour envoyer des e-mails
def send_email(recipient, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = recipient

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Utilisez TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail à {recipient}: {e}")

# Fonction pour obtenir le prix du Bitcoin
def get_btc_price():
    # lien api pour vérifier le prix de la crypto
    url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    headers = {"X-CoinAPI-Key": COIN_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["rate"]
        else:
            raise Exception(f"Erreur HTTP: {response.status_code}")
    except Exception as e:
        raise Exception(f"Impossible de récupérer le prix du BTC: {e}")

# Variable pour suivre le dernier prix
previous_btc_price = None

# Fonction pour vérifier le prix du Bitcoin et envoyer des alertes
def check_btc_price_and_alert():
    global previous_btc_price
    current_btc_price = get_btc_price()

    # Vérifier si le prix est inférieur au budget initail
    if current_btc_price < BTC_ALERT_THRESHOLD:
        emails = get_client_emails()
        for email in emails:
            send_email(email, "Alerte Bitcoin", f"Le prix du Bitcoin est tombé à {current_btc_price} USD.")

    else:
        print(f"Le prix du Bitcoin est de {current_btc_price} USD, aucune alerte nécessaire.")  # Ajout de ce message, si le prix est au-dessus du budget

    # Vérifier la variation en pourcentage
    if previous_btc_price is not None:
        percentage_change = ((current_btc_price - previous_btc_price) / previous_btc_price) * 100
        if percentage_change >= BTC_PERCENTAGE_THRESHOLD:
            emails = get_client_emails()
            for email in emails:
                send_email(email, "Alerte Bitcoin", f"Le prix du Bitcoin a augmenté de {percentage_change:.2f}%.")

    # Mettre à jour le dernier prix
    previous_btc_price = current_btc_price

# Boucle de vérification périodique
while True:
    try:
        check_btc_price_and_alert()  # Vérifier le prix du Bitcoin et envoyer des alertes
    except Exception as e:
        print(f"Erreur lors de la vérification du prix BTC et des alertes: {e}")
    sleep(ALERT_INTERVAL)  # Attendre avant la prochaine vérification
