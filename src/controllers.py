from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from src.models import User, Depense
from src import db, login_manager

views_bp = Blueprint("views", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@views_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash("Connexion réussie.")
            return redirect(url_for("views.depenses_view"))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")
    return render_template("login.html")


@views_bp.route("/register", methods=["GET", "POST"])
def register_view():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(
                "L'utilisateur existe déjà. Veuillez choisir un autre nom d'utilisateur ou une autre adresse email.",
                "error",
            )
            return redirect("/register")

        flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for("views.login_view"))

    return render_template("register.html")


@views_bp.route("/logout")
@login_required
def logout_view():
    logout_user()
    flash("Déconnexion réussie.")
    return redirect(url_for("views.login_view"))


@views_bp.route("/")
@login_required
def ajouter():
    return render_template("ajouter.html")


@views_bp.route("/supprimer/<int:id>")
@login_required
def supprimer(id):
    depense = Depense.query.filter_by(id=id).first()
    db.session.delete(depense)
    db.session.commit()
    return redirect("/depenses")


@views_bp.route("/modifier", methods=["POST"])
@login_required
def modifier_depense_post():
    depense_id = request.form["id"]
    depense = Depense.query.filter_by(id=depense_id).first()

    depense.date = request.form["date"]
    depense.libelle = request.form["libelle"]
    depense.montant = int(request.form["montant"])
    depense.categorie = request.form["categorie"]

    db.session.commit()
    return redirect("/depenses")


@views_bp.route("/modifier_depense/<int:id>")
@login_required
def modifier_depense(id):
    depense = Depense.query.filter_by(id=id).first()
    return render_template("modifier_depense.html", depense=depense)


@views_bp.route("/depenses")
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

    if expenses:
        for depense in expenses:
            total += depense.montant
            if depense.categorie == "alimentation":
                t_alimentation += depense.montant
            elif depense.categorie == "loisirs":
                t_loisirs += depense.montant
            elif depense.categorie == "logement":
                t_logement += depense.montant
            elif depense.categorie == "transport":
                t_transport += depense.montant
            elif depense.categorie == "sante":
                t_sante += depense.montant
            elif depense.categorie == "vetements":
                t_vetements += depense.montant
            elif depense.categorie == "autres":
                t_autres += depense.montant
    else:
        expenses = []

    return render_template(
        "depenses.html",
        depenses=expenses,
        total=total,
        t_alimentation=t_alimentation,
        t_loisirs=t_loisirs,
        t_logement=t_logement,
        t_transport=t_transport,
        t_sante=t_sante,
        t_vetements=t_vetements,
        t_autres=t_autres,
    )


@views_bp.route("/ajouterdepense", methods=["POST"])
@login_required
def ajouterdepense():
    date = request.form["date"]
    libelle = request.form["libelle"]
    montant = request.form["montant"]
    categorie = request.form["categorie"]
    print(date + " " + libelle + " " + montant + " " + categorie)
    depense = Depense(date=date, libelle=libelle, montant=montant, categorie=categorie)
    db.session.add(depense)
    db.session.commit()
    return redirect("/depenses")
