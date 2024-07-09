from flask import Flask, render_template, request, redirect
from  flask_sqlalchemy import SQLAlchemy
import os
project_dir= os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir,"db/mydatabase.db")
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Ajout de cette ligne pour éviter les avertissements

db = SQLAlchemy(app)

class Depense(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    date= db.Column(db.String(50), nullable= False)
    libelle= db.Column(db.String(50), nullable= False )
    montant= db.Column(db.Integer, nullable= False)
    categorie= db.Column(db.String(50), nullable= False)

@app.route("/")
def ajouter():
    return render_template("ajouter.html")

@app.route('/depenses')
def depenses():
    expenses= Depense.query.all()
    return render_template("depenses.html", depenses= expenses)

@app.route("/ajouterdepense", methods=['POST'])
def ajouterdepense():
    date = request.form['date']
    libelle = request.form['libelle']
    montant = request.form['montant']
    categorie = request.form['categorie']
    print(date  + ' ' + libelle + ' ' + montant + ' ' + categorie)
    depense= Depense(date=date,libelle=libelle, montant=montant, categorie=categorie )
    db.session.add(depense)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

