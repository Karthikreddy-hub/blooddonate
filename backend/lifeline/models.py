from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    mobile = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    donor = db.relationship("Donor", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Donor(db.Model):
    __tablename__ = "donors"
    __table_args__ = (
        db.UniqueConstraint("user_id", name="uq_donors_user_id"),
        db.CheckConstraint("age >= 1 AND age <= 120", name="ck_donors_age_range"),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(160), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(254), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(160), nullable=False, index=True)
    gender = db.Column(db.String(32), nullable=False, default="Prefer not to say")
    blood_group = db.Column(db.String(3), nullable=False, index=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    consent = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    user = db.relationship("User", back_populates="donor")
