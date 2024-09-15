import os
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
        init_collections()

    # Rejestracja blueprintów
    from . import routes
    app.register_blueprint(routes.main_bp)

    # Rejestracja komend CLI
    from .commands import init_data_command
    app.cli.add_command(init_data_command)

    return app

def init_collections():
    from .models import Collection, Card
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_folder):
        print(f"Folder {data_folder} nie istnieje.")
        return

    json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]

    for json_file in json_files:
        file_path = os.path.join(data_folder, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Błąd parsowania pliku {file_path}. Upewnij się, że plik jest poprawnym JSON.")
            continue

        collection_name = data.get('collection_name')
        cards = data.get('cards', [])

        if not collection_name:
            print(f"Plik {json_file} nie zawiera nazwy kolekcji.")
            continue

        collection = Collection.query.filter_by(name=collection_name).first()
        if not collection:
            collection = Collection(name=collection_name)
            db.session.add(collection)
            db.session.commit()

        for card_data in cards:
            identifier = card_data.get('identifier')
            name = card_data.get('name')
            rarity = card_data.get('rarity')

            if not identifier or not name or not rarity:
                print(f"Niekompletne dane karty w pliku {json_file}: {card_data}")
                continue

            existing_card = Card.query.filter_by(identifier=identifier).first()
            if existing_card:
                existing_card.name = name
                existing_card.rarity = rarity
            else:
                card = Card(
                    identifier=identifier,
                    name=name,
                    rarity=rarity,
                    collection_id=collection.id
                )
                db.session.add(card)
        db.session.commit()
