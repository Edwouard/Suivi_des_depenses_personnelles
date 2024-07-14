from app import app, db, Depense


def init_db():
    with app.app_context():
        db.create_all()
        # Convertir les montants en entiers
        depenses = Depense.query.all()
        for depense in depenses:
            if depense.montant:
                depense.montant = int(depense.montant)
            else:
                depense.montant = 0
        db.session.commit()


if __name__ == "__main__":
    init_db()
