from flask import Flask, render_template, request
import mariadb


HOST = "localhost"
USER = "root"
PASSWORD = "duck"
DATABASE = "alert_crypto"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inscription():
    if request.method == "GET":
        return render_template("inscription.html")  
    else:  
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]

        try:
            conn = mariadb.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            cursor = conn.cursor()

            # insérer les informations du client (nom, prénom et mail) dans la table client
            cursor.execute("INSERT INTO client (nom, prenom, mail) VALUES (?, ?, ?)", (nom, prenom, email))
            conn.commit()

            
            return render_template("inscription_reussie.html")  

        except mariadb.Error as err:
            print(f"Error: {err}")
            
            message = "Une erreur est survenue. Veuillez réessayer."
            return render_template("inscription.html")  

        finally:
            if conn:
                conn.cursor().close()
                conn.close()

if __name__ == "__main__":
    app.run(debug=True)  