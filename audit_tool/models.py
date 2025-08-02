from __future__ import annotations
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship

from . import db, login_manager

# Association tables
roles_permissions = Table(
    'roles_permissions',
    db.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('permission_id', Integer, ForeignKey('permission.id')),
)

user_roles = Table(
    'user_roles',
    db.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id')),
)

audit_risks = Table(
    'audit_risks',
    db.metadata,
    Column('audit_id', Integer, ForeignKey('audit.id')),
    Column('risk_id', Integer, ForeignKey('risk_tag.id')),
)


class Permission(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Role(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)
    permissions = relationship('Permission', secondary=roles_permissions, backref='roles')


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    roles = relationship('Role', secondary=user_roles, backref='users')

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def has_permission(self, name: str) -> bool:
        return any(name == p.name for r in self.roles for p in r.permissions)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return User.query.get(int(user_id))


class Audit(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(Text)
    severity = Column(String(32))
    source = Column(String(32))
    assigned_team = Column(String(64))
    status = Column(String(32), default='Open')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    risks = relationship('RiskTag', secondary=audit_risks, backref='audits')
    comments = relationship('Comment', backref='audit', cascade='all,delete')
    findings = relationship('Finding', backref='audit', cascade='all,delete')
    attachments = relationship('Attachment', backref='audit', cascade='all,delete')
    logs = relationship('AuditLog', backref='audit', cascade='all,delete')


class RiskTag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    audit_id = Column(Integer, ForeignKey('audit.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User')


class Attachment(db.Model):
    id = Column(Integer, primary_key=True)
    audit_id = Column(Integer, ForeignKey('audit.id'), nullable=False)
    filename = Column(String(256), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(db.Model):
    id = Column(Integer, primary_key=True)
    audit_id = Column(Integer, ForeignKey('audit.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    action = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User')


class Finding(db.Model):
    id = Column(Integer, primary_key=True)
    audit_id = Column(Integer, ForeignKey('audit.id'), nullable=False)
    title = Column(String(128), nullable=False)
    description = Column(Text)
    severity = Column(String(32))
    status = Column(String(32), default='Open')
    created_at = Column(DateTime, default=datetime.utcnow)
