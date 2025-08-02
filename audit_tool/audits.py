from flask import Blueprint, render_template, redirect, url_for, Response, request, current_app, send_from_directory
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

from .models import Audit, RiskTag, Comment, Attachment, AuditLog, Finding, db
from .rbac import permission_required
import os


class AuditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    severity = SelectField('Severity', choices=['Low', 'Medium', 'High', 'Critical'])
    source = SelectField('Source', choices=['Internal', 'External'])
    assigned_team = StringField('Assigned Team')
    risks = StringField('Risk Tags (comma separated)')
    submit = SubmitField('Create')


class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')


class StatusForm(FlaskForm):
    status = SelectField('Status', choices=['Open', 'Verified', 'Mitigated', 'Closed'])
    submit = SubmitField('Update')


class AttachmentForm(FlaskForm):
    file = FileField('Attachment', validators=[FileAllowed(['pdf', 'txt', 'csv', 'png', 'jpg', 'jpeg'])])
    submit = SubmitField('Upload')


class FindingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    severity = SelectField('Severity', choices=['Low', 'Medium', 'High', 'Critical'])
    status = SelectField('Status', choices=['Open', 'Verified', 'Mitigated', 'Closed'])
    submit = SubmitField('Add Finding')


audit_bp = Blueprint('audit', __name__, url_prefix='/audit', template_folder='templates')


@audit_bp.route('/dashboard')
@login_required
@permission_required('view_audit')
def dashboard():
    severity = request.args.get('severity')
    risk = request.args.get('risk')
    query = Audit.query
    if severity:
        query = query.filter_by(severity=severity)
    if risk:
        query = query.join(Audit.risks).filter(RiskTag.name == risk)
    audits = query.all()
    risks = RiskTag.query.all()
    return render_template('audits/list.html', audits=audits, risks=risks)


@audit_bp.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required('create_audit')
def create():
    form = AuditForm()
    if form.validate_on_submit():
        audit = Audit(
            title=form.title.data,
            description=form.description.data,
            severity=form.severity.data,
            source=form.source.data,
            assigned_team=form.assigned_team.data,
        )
        # handle risk tags
        tag_names = [n.strip() for n in form.risks.data.split(',') if n.strip()]
        for name in tag_names:
            tag = RiskTag.query.filter_by(name=name).first()
            if not tag:
                tag = RiskTag(name=name)
            audit.risks.append(tag)
        db.session.add(audit)
        db.session.commit()
        log = AuditLog(audit=audit, user=current_user, action='Created audit')
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('audit.detail', audit_id=audit.id))
    return render_template('audits/create.html', form=form)


@audit_bp.route('/<int:audit_id>', methods=['GET', 'POST'])
@login_required
@permission_required('view_audit')
def detail(audit_id: int):
    audit = Audit.query.get_or_404(audit_id)
    comment_form = CommentForm(prefix='comment')
    status_form = StatusForm(prefix='status')
    if not status_form.status.data:
        status_form.status.data = audit.status
    attach_form = AttachmentForm(prefix='attach')
    finding_form = FindingForm(prefix='finding')
    can_edit = current_user.has_permission('edit_audit')

    if comment_form.submit.data and can_edit and comment_form.validate_on_submit():
        c = Comment(audit=audit, user=current_user, content=comment_form.content.data)
        db.session.add(c)
        db.session.add(AuditLog(audit=audit, user=current_user, action='Added comment'))
        db.session.commit()
        return redirect(url_for('audit.detail', audit_id=audit_id))

    if status_form.submit.data and can_edit and status_form.validate_on_submit():
        audit.status = status_form.status.data
        db.session.add(AuditLog(audit=audit, user=current_user, action=f'Status changed to {audit.status}'))
        db.session.commit()
        return redirect(url_for('audit.detail', audit_id=audit_id))

    if attach_form.submit.data and can_edit and attach_form.validate_on_submit() and attach_form.file.data:
        file = attach_form.file.data
        filename = file.filename
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        att = Attachment(audit=audit, filename=filename)
        db.session.add(att)
        db.session.add(AuditLog(audit=audit, user=current_user, action=f'Uploaded {filename}'))
        db.session.commit()
        return redirect(url_for('audit.detail', audit_id=audit_id))

    if finding_form.submit.data and can_edit and finding_form.validate_on_submit():
        f = Finding(
            audit=audit,
            title=finding_form.title.data,
            description=finding_form.description.data,
            severity=finding_form.severity.data,
            status=finding_form.status.data,
        )
        db.session.add(f)
        db.session.add(AuditLog(audit=audit, user=current_user, action='Added finding'))
        db.session.commit()
        return redirect(url_for('audit.detail', audit_id=audit_id))

    return render_template(
        'audits/detail.html',
        audit=audit,
        comment_form=comment_form,
        status_form=status_form,
        attach_form=attach_form,
        finding_form=finding_form,
        can_edit=can_edit,
    )


@audit_bp.route('/attachment/<int:attachment_id>')
@login_required
@permission_required('view_audit')
def attachment(attachment_id: int):
    att = Attachment.query.get_or_404(attachment_id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], att.filename, as_attachment=True)


@audit_bp.route('/export/csv')
@login_required
@permission_required('view_audit')
def export_csv():
    """Export all audits to a CSV file."""
    import csv
    from io import StringIO

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['id', 'title', 'severity', 'status'])
    for a in Audit.query.all():
        writer.writerow([a.id, a.title, a.severity, a.status])
    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=audits.csv'})


@audit_bp.route('/export/pdf')
@login_required
@permission_required('view_audit')
def export_pdf():
    """Export all audits to a simple PDF report."""
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    text = p.beginText(40, 750)
    text.textLine('Audit Report')
    text.textLine('')
    for a in Audit.query.all():
        text.textLine(f"{a.id}: {a.title} - {a.severity} - {a.status}")
    p.drawText(text)
    p.showPage()
    p.save()
    buffer.seek(0)
    return Response(
        buffer.read(),
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment;filename=audits.pdf'},
    )
