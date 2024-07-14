from src import create_app, db
from src.models import Depense


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        depenses = Depense.query.all()
        for depense in depenses:
            if depense.montant:
                depense.montant = int(depense.montant)
            else:
                depense.montant = 0
        db.session.commit()


if __name__ == "__main__":
    init_db()
