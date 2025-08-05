"""Populate the database with default roles, permissions and an admin user."""
from audit_tool import create_app, db
from audit_tool.models import Role, Permission, User, RiskTag

app = create_app()

with app.app_context():
    db.create_all()

    # Permissions
    perms = ['view_audit', 'create_audit', 'edit_audit']
    permission_objs = []
    for name in perms:
        p = Permission.query.filter_by(name=name).first()
        if not p:
            p = Permission(name=name)
            db.session.add(p)
        permission_objs.append(p)

    # Roles
    gov = Role.query.filter_by(name='Governance').first()
    if not gov:
        gov = Role(name='Governance', permissions=permission_objs)
        db.session.add(gov)

    # Admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin')
        admin.set_password('admin')
        admin.roles.append(gov)
        db.session.add(admin)

    # Risk categories
    risks = [
        'Risk Contextualization',
        'Intelligent Analytics',
        'High Visibility',
        'Vulnerability Management',
        'Real-Time Reporting',
        'Compliance Management',
        'Vulnerability Validation Automation',
    ]
    for r in risks:
        if not RiskTag.query.filter_by(name=r).first():
            db.session.add(RiskTag(name=r))

    db.session.commit()
    print('Database seeded')
