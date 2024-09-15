import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegistrationForm, LoginForm, AddCollectionForm, EmptyForm, RemoveCollectionForm
from .models import User, UserProfile, Collection, Card, UserCard
from . import db, bcrypt

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Zostałeś zalogowany!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło', 'danger')
    return render_template('login.html', form=form)


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Tworzenie UserProfile
        profile = UserProfile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

        flash('Twoje konto zostało utworzone! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany.', 'info')
    return redirect(url_for('main.login'))


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@main_bp.route('/add_collection', methods=['GET', 'POST'])
@login_required
def add_collection():
    form = AddCollectionForm()
    collections = Collection.query.all()
    form.collection.choices = [(c.id, c.name) for c in collections]

    if form.validate_on_submit():
        collection_id = form.collection.data
        collection = Collection.query.get(collection_id)
        if collection not in current_user.profile.collections:
            current_user.profile.collections.append(collection)
            db.session.commit()
            flash('Kolekcja została dodana do Twojego profilu.', 'success')
        else:
            flash('Ta kolekcja jest już dodana do Twojego profilu.', 'info')
        return redirect(url_for('main.profile'))
    return render_template('add_collection.html', form=form)


@main_bp.route('/collection/<int:collection_id>', methods=['GET', 'POST'])
@login_required
def view_collection(collection_id):
    form = EmptyForm()
    remove_form = RemoveCollectionForm()
    collection = Collection.query.get_or_404(collection_id)
    user_cards = {uc.card_id: uc for uc in current_user.profile.user_cards}

    # Pobieramy karty z kolekcji
    cards = collection.cards

    # Funkcja pomocnicza do sortowania identyfikatorów alfanumerycznych
    def sort_key(card):
        match = re.match(r'(\D+)(\d+)', card.identifier)
        if match:
            prefix, number = match.groups()
            return (prefix, int(number))
        else:
            return (card.identifier, 0)

    # Sortujemy karty
    cards = sorted(cards, key=sort_key)

    if form.validate_on_submit():
        for card in cards:
            quantity = request.form.get(f'quantity_{card.id}', type=int)
            if quantity is not None:
                if quantity < 0:
                    quantity = 0
                if card.id in user_cards:
                    user_cards[card.id].quantity = quantity
                else:
                    new_user_card = UserCard(
                        profile_id=current_user.profile.id,
                        card_id=card.id,
                        quantity=quantity
                    )
                    db.session.add(new_user_card)
        db.session.commit()
        flash('Zmiany zostały zapisane.', 'success')
        return redirect(url_for('main.view_collection', collection_id=collection.id))

    return render_template('collection.html', collection=collection, user_cards=user_cards,
                           cards=cards, form=form, remove_form=remove_form)


@main_bp.route('/remove_collection/<int:collection_id>', methods=['POST'])
@login_required
def remove_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    remove_form = RemoveCollectionForm()
    if remove_form.validate_on_submit():
        if collection in current_user.profile.collections:
            # Pobieramy identyfikatory kart w kolekcji
            card_subquery = db.session.query(Card.id).filter(Card.collection_id == collection.id).subquery()
            # Usuwamy powiązane UserCard
            UserCard.query.filter(
                UserCard.profile_id == current_user.profile.id,
                UserCard.card_id.in_(card_subquery)
            ).delete(synchronize_session=False)
            # Usuwamy kolekcję z profilu użytkownika
            current_user.profile.collections.remove(collection)
            db.session.commit()
            flash('Kolekcja została usunięta z Twojego profilu.', 'success')
        else:
            flash('Nie posiadasz tej kolekcji w swoim profilu.', 'warning')
    else:
        flash('Nie udało się usunąć kolekcji. Spróbuj ponownie.', 'danger')
    return redirect(url_for('main.profile'))
