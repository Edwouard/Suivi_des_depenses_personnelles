from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def ajouter():
    return render_template("ajouter.html")

@app.route("/ajouterdepense", methods=['POST'])
def ajouterdepense():
    date = request.form['date']
    libelle = request.form['libelle']
    montant = request.form['montant']
    categorie = request.form['categorie']
    print(date  + ' ' + libelle + ' ' + montant + ' ' + categorie)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)