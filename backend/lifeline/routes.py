from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import func, or_, select, text
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .forms import DonorForm, LoginForm, RegisterForm
from .models import Donor, User

main = Blueprint("main", __name__)


def page(name, **context):
    return render_template("site.html", page=name, **context)


@main.get("/")
def home():
    count = db.session.scalar(select(func.count()).select_from(Donor).where(Donor.available.is_(True), Donor.consent.is_(True))) or 0
    return page("home", donor_count=count)


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        username, email = form.username.data.strip().lower(), form.email.data.strip().lower()
        if db.session.scalar(select(User.id).where(User.username == username)):
            flash("That username is already in use. Please choose another.", "error")
        elif db.session.scalar(select(User.id).where(User.email == email)):
            flash("An account with that email address already exists.", "error")
        else:
            user = User(first_name=form.first_name.data.strip(), last_name=form.last_name.data.strip(),
                        username=username, email=email, mobile=form.mobile.data.strip())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Your account is ready. Welcome to LifeLine!", "success")
            return redirect(url_for("main.dashboard"))
    return page("register", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.username == form.username.data.strip().lower()))
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You are signed in.", "success")
            return redirect(url_for("main.dashboard"))
        flash("The username or password is incorrect.", "error")
    return page("login", form=form)


@main.post("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("main.home"))


@main.get("/dashboard")
@login_required
def dashboard():
    count = db.session.scalar(select(func.count()).select_from(Donor).where(Donor.available.is_(True), Donor.consent.is_(True))) or 0
    return page("dashboard", donor_count=count, donor=current_user.donor)


@main.route("/donate", methods=["GET", "POST"])
@login_required
def donor_form():
    donor = current_user.donor
    form = DonorForm(obj=donor)
    if request.method == "GET" and donor is None:
        form.name.data = f"{current_user.first_name} {current_user.last_name}".strip()
        form.email.data, form.mobile.data = current_user.email, current_user.mobile
    if form.validate_on_submit():
        if donor is None:
            donor = Donor(user=current_user)
        donor.name, donor.age = form.name.data.strip(), form.age.data
        donor.email, donor.mobile = form.email.data.strip().lower(), form.mobile.data.strip()
        donor.location, donor.blood_group = form.location.data.strip(), form.blood_group.data
        donor.gender = form.gender.data or "Prefer not to say"
        donor.available, donor.consent = form.available.data, form.consent.data
        db.session.add(donor)
        db.session.commit()
        flash("Your donor profile has been saved.", "success")
        return redirect(url_for("main.dashboard"))
    return page("donor_form", form=form, editing=donor is not None)


@main.get("/donors")
@login_required
def donors():
    blood_group, query = request.args.get("blood_group", "").strip(), request.args.get("q", "").strip()
    stmt = select(Donor).where(Donor.available.is_(True), Donor.consent.is_(True))
    if blood_group:
        stmt = stmt.where(Donor.blood_group == blood_group)
    if query:
        term = f"%{query}%"
        stmt = stmt.where(or_(Donor.name.ilike(term), Donor.location.ilike(term)))
    records = db.session.scalars(stmt.order_by(Donor.created_at.desc()).limit(100)).all()
    return page("donors", donors=records, blood_group=blood_group, query=query)


@main.get("/contact")
def contact():
    return page("contact")


@main.get("/health/")
def health():
    try:
        db.session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify(status="unhealthy", database="unavailable"), 503
    return jsonify(status="ok", database="ok"), 200
