from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from webapp.auth import login_required
from webapp.db import get_db

bp = Blueprint('opportunities', __name__)


@bp.route('/')
@login_required
def index():
    """Show all opportunities assigned to the current user."""
    db = get_db()
    opportunities = db.execute(
        'SELECT o.id, organization_name, volunteer_title, url, image,'
        ' position_date, description, age_requirement, skill_requirement,'
        ' address_virtual, passion_areas, specific_skills, filters,'
        ' verification_status, assigned_user_id'
        ' FROM opportunity o'
        ' WHERE o.assigned_user_id = ?'
        ' ORDER BY o.created_at DESC',
        (g.user['id'],)
    ).fetchall()
    
    return render_template('opportunities/index.html', opportunities=opportunities)


@bp.route('/all')
@login_required
def all_opportunities():
    """Show all opportunities (for admins or overview)."""
    db = get_db()
    opportunities = db.execute(
        'SELECT o.id, organization_name, volunteer_title, url, image,'
        ' position_date, description, age_requirement, skill_requirement,'
        ' address_virtual, passion_areas, specific_skills, filters,'
        ' verification_status, assigned_user_id, u.username as assigned_to'
        ' FROM opportunity o'
        ' LEFT JOIN user u ON o.assigned_user_id = u.id'
        ' ORDER BY o.created_at DESC'
    ).fetchall()
    
    return render_template('opportunities/all.html', opportunities=opportunities)


@bp.route('/<int:id>/verify', methods=('GET', 'POST'))
@login_required
def verify(id):
    """Verify an opportunity."""
    opportunity = get_opportunity(id)
    
    if request.method == 'POST':
        status = request.form['status']
        notes = request.form.get('notes', '')
        error = None
        
        if status not in ['verified', 'rejected', 'needs_review']:
            error = 'Invalid status.'
        
        if error is None:
            db = get_db()
            db.execute(
                'UPDATE opportunity SET verification_status = ?'
                ' WHERE id = ?',
                (status, id)
            )
            db.execute(
                'INSERT INTO verification (opportunity_id, user_id, status, notes)'
                ' VALUES (?, ?, ?, ?)',
                (id, g.user['id'], status, notes)
            )
            db.commit()
            flash(f'Opportunity {status}!', 'success')
            return redirect(url_for('opportunities.index'))
        
        flash(error, 'error')
    
    return render_template('opportunities/verify.html', opportunity=opportunity)


@bp.route('/<int:id>/detail')
@login_required
def detail(id):
    """Show detailed view of an opportunity."""
    opportunity = get_opportunity(id, check_assigned=False)
    
    db = get_db()
    verifications = db.execute(
        'SELECT v.*, u.username'
        ' FROM verification v'
        ' JOIN user u ON v.user_id = u.id'
        ' WHERE v.opportunity_id = ?'
        ' ORDER BY v.verified_at DESC',
        (id,)
    ).fetchall()
    
    return render_template('opportunities/detail.html', 
                         opportunity=opportunity, 
                         verifications=verifications)


@bp.route('/<int:id>/assign', methods=('POST',))
@login_required
def assign(id):
    """Assign an opportunity to a user."""
    user_id = request.form.get('user_id')
    
    if not user_id:
        flash('User ID is required.', 'error')
        return redirect(url_for('opportunities.all_opportunities'))
    
    db = get_db()
    db.execute(
        'UPDATE opportunity SET assigned_user_id = ?'
        ' WHERE id = ?',
        (user_id, id)
    )
    db.commit()
    flash('Opportunity assigned successfully!', 'success')
    return redirect(url_for('opportunities.all_opportunities'))


@bp.route('/stats')
@login_required
def stats():
    """Show verification statistics."""
    db = get_db()
    
    user_stats = db.execute(
        'SELECT COUNT(*) as total,'
        ' SUM(CASE WHEN verification_status = "verified" THEN 1 ELSE 0 END) as verified,'
        ' SUM(CASE WHEN verification_status = "rejected" THEN 1 ELSE 0 END) as rejected,'
        ' SUM(CASE WHEN verification_status = "pending" THEN 1 ELSE 0 END) as pending,'
        ' SUM(CASE WHEN verification_status = "needs_review" THEN 1 ELSE 0 END) as needs_review'
        ' FROM opportunity'
        ' WHERE assigned_user_id = ?',
        (g.user['id'],)
    ).fetchone()
    
    overall_stats = db.execute(
        'SELECT COUNT(*) as total,'
        ' SUM(CASE WHEN verification_status = "verified" THEN 1 ELSE 0 END) as verified,'
        ' SUM(CASE WHEN verification_status = "rejected" THEN 1 ELSE 0 END) as rejected,'
        ' SUM(CASE WHEN verification_status = "pending" THEN 1 ELSE 0 END) as pending,'
        ' SUM(CASE WHEN verification_status = "needs_review" THEN 1 ELSE 0 END) as needs_review'
        ' FROM opportunity'
    ).fetchone()
    
    return render_template('opportunities/stats.html', 
                         user_stats=user_stats,
                         overall_stats=overall_stats)


def get_opportunity(id, check_assigned=True):
    """Get an opportunity by id, optionally checking if it's assigned to current user."""
    opportunity = get_db().execute(
        'SELECT o.id, organization_name, volunteer_title, url, image,'
        ' position_date, description, age_requirement, skill_requirement,'
        ' address_virtual, passion_areas, specific_skills, filters,'
        ' verification_status, assigned_user_id'
        ' FROM opportunity o'
        ' WHERE o.id = ?',
        (id,)
    ).fetchone()
    
    if opportunity is None:
        abort(404, f"Opportunity id {id} doesn't exist.")
    
    if check_assigned and opportunity['assigned_user_id'] != g.user['id']:
        abort(403, "You don't have permission to verify this opportunity.")
    
    return opportunity
