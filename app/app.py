from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import os


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "../instance/dbgestionbudget.db")
)

app = Flask(__name__)
#app.config.from_object("config.config.Config")
app.secret_key = 'super secret string'

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Ajout de cette ligne pour éviter les avertissements

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_view" 


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    depenses = db.relationship('Depense', backref='user')


class Depense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    libelle = db.Column(db.String(50), nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        default=lambda: current_user.get_id()
                        )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Connexion réussie.')
            return redirect(url_for('depenses_view'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")
    return render_template('login.html')

# Vue pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Essayez d'insérer l'utilisateur dans la base de données
        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('L\'utilisateur existe déjà. Veuillez choisir un autre nom d\'utilisateur ou une autre adresse email.', 'error')
            return redirect('/register')

        # Flash message pour l'inscription réussie
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login_view'))  # Utilisation de url_for pour générer l'URL

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout_view():
    logout_user()
    flash('Connexion Reussie.')
    return redirect(url_for('login_view'))

@app.route("/")
@login_required
def ajouter():
    return render_template("ajouter.html")

@app.route("/supprimer/<int:id>")
@login_required
def supprimer(id):
    depense = Depense.query.filter_by(id=id).first()
    db.session.delete(depense)
    db.session.commit()
    return redirect("/depenses")

@app.route("/modifier", methods=['POST'])
@login_required
def modifier_depense_post():
    depense_id = request.form['id']
    depense = Depense.query.filter_by(id=depense_id).first()
    
    depense.date = request.form['date']
    depense.libelle = request.form['libelle']
    depense.montant = int(request.form['montant'])
    depense.categorie = request.form['categorie']
    
    db.session.commit()
    return redirect("/depenses")

@app.route("/modifier_depense/<int:id>")
@login_required
def modifier_depense(id):
    depense = Depense.query.filter_by(id=id).first()
    return render_template("modifier_depense.html", depense=depense)

@app.route('/depenses')
@login_required
def depenses_view():
    expenses = Depense.query.filter_by(user_id=current_user.id)
    total = 0
    t_alimentation = 0
    t_loisirs = 0
    t_logement = 0
    t_transport = 0
    t_sante = 0
    t_vetements = 0
    t_autres = 0
    #import pdb;
    #pdb.set_trace()
    if expenses :
        for depense in expenses:
            total += depense.montant
            if depense.categorie == 'alimentation':
                t_alimentation += depense.montant
            elif depense.categorie == 'loisirs':
                t_loisirs += depense.montant
            elif depense.categorie == 'logement':
                t_logement += depense.montant
            elif depense.categorie == 'transport':
                t_transport += depense.montant
            elif depense.categorie == 'sante':
                t_sante += depense.montant
            elif depense.categorie == 'vetements':
                t_vetements += depense.montant
            elif depense.categorie == 'autres':
                t_autres += depense.montant
    else:
        expenses = []
    return render_template("depenses.html", depenses=expenses, total=total, t_alimentation=t_alimentation, t_loisirs=t_loisirs, t_logement=t_logement, t_transport=t_transport, t_sante=t_sante, t_vetements=t_vetements, t_autres=t_autres)

@app.route("/ajouterdepense", methods=['POST'])
@login_required
def ajouterdepense():
    date = request.form['date']
    libelle = request.form['libelle']
    montant = request.form['montant']
    categorie = request.form['categorie']
    print(date + ' ' + libelle + ' ' + montant + ' ' + categorie)
    depense = Depense(date=date, libelle=libelle, montant=montant, categorie=categorie)
    db.session.add(depense)
    db.session.commit()
    return redirect("/depenses")

# Convertir les montants en entiers
with app.app_context():
    db.create_all()  # Création des tables
    depenses = Depense.query.all()
    for depense in depenses:
        if depense.montant:  # Vérifier que la valeur n'est pas vide
            depense.montant = int(depense.montant)
        else:
            depense.montant = 0
    db.session.commit()

if __name__ == '__main__':
    app.run(app.run(host="0.0.0.0", port="5010", debug=True))
