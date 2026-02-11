"""
Database migration script to update existing databases to the new schema.
This handles the case where databases were created with the old schema.
"""

import sqlite3
import click
from flask import current_app
from webapp.db import get_db


def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table."""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns


@click.command('migrate-db')
def migrate_db_command():
    """Migrate existing database to new schema."""
    db = get_db()
    cursor = db.cursor()
    
    click.echo('Checking database schema...')
    
    # Check if opportunity table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='opportunity'")
    if not cursor.fetchone():
        click.echo('No opportunity table found. Run "flask init-db" first.')
        return
    
    migrations_applied = []
    
    # Migration 1: Rename assigned_user to assigned_user_id if needed
    if check_column_exists(cursor, 'opportunity', 'assigned_user'):
        click.echo('Migrating: assigned_user -> assigned_user_id')
        cursor.execute("""
            CREATE TABLE opportunity_new (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              organization_name TEXT NOT NULL,
              volunteer_title TEXT NOT NULL,
              url TEXT NOT NULL,
              image TEXT,
              position_date TEXT NOT NULL,
              description TEXT NOT NULL,
              age_requirement TEXT,
              skill_requirement TEXT,
              address_virtual TEXT,
              passion_areas TEXT,
              specific_skills TEXT,
              filters TEXT,
              assigned_user_id INTEGER,
              verification_status TEXT DEFAULT 'pending',
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (assigned_user_id) REFERENCES user (id)
            )
        """)
        
        cursor.execute("""
            INSERT INTO opportunity_new 
            SELECT id, organization_name, volunteer_title, url, image, position_date,
                   description, age_requirement, skill_requirement, address_virtual,
                   passion_areas, specific_skills, filters, assigned_user,
                   verification_status, created_at
            FROM opportunity
        """)
        
        cursor.execute("DROP TABLE opportunity")
        cursor.execute("ALTER TABLE opportunity_new RENAME TO opportunity")
        migrations_applied.append('Renamed assigned_user to assigned_user_id')
    
    # Migration 2: Add missing columns if needed
    if not check_column_exists(cursor, 'opportunity', 'assigned_user_id'):
        click.echo('Adding assigned_user_id column...')
        cursor.execute('ALTER TABLE opportunity ADD COLUMN assigned_user_id INTEGER')
        migrations_applied.append('Added assigned_user_id column')
    
    if not check_column_exists(cursor, 'opportunity', 'verification_status'):
        click.echo('Adding verification_status column...')
        cursor.execute("ALTER TABLE opportunity ADD COLUMN verification_status TEXT DEFAULT 'pending'")
        cursor.execute("UPDATE opportunity SET verification_status = 'pending' WHERE verification_status IS NULL")
        migrations_applied.append('Added verification_status column')
    
    if not check_column_exists(cursor, 'opportunity', 'created_at'):
        click.echo('Adding created_at column...')
        cursor.execute('ALTER TABLE opportunity ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        migrations_applied.append('Added created_at column')
    
    # Migration 3: Add role to user table if missing
    if not check_column_exists(cursor, 'user', 'role'):
        click.echo('Adding role column to user table...')
        cursor.execute("ALTER TABLE user ADD COLUMN role TEXT DEFAULT 'verifier'")
        cursor.execute("UPDATE user SET role = 'verifier' WHERE role IS NULL")
        migrations_applied.append('Added role column to user table')
    
    if not check_column_exists(cursor, 'user', 'created_at'):
        click.echo('Adding created_at column to user table...')
        cursor.execute('ALTER TABLE user ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
        migrations_applied.append('Added created_at column to user table')
    
    # Migration 4: Create verification table if missing
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='verification'")
    if not cursor.fetchone():
        click.echo('Creating verification table...')
        cursor.execute("""
            CREATE TABLE verification (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              opportunity_id INTEGER NOT NULL,
              user_id INTEGER NOT NULL,
              status TEXT NOT NULL,
              notes TEXT,
              verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (opportunity_id) REFERENCES opportunity (id),
              FOREIGN KEY (user_id) REFERENCES user (id)
            )
        """)
        migrations_applied.append('Created verification table')
    
    db.commit()
    
    if migrations_applied:
        click.echo('\nMigrations applied successfully:')
        for migration in migrations_applied:
            click.echo(f'  ✓ {migration}')
    else:
        click.echo('Database is already up to date. No migrations needed.')
    
    click.echo('\nDatabase migration complete!')


def init_app(app):
    """Register migration command with Flask app."""
    app.cli.add_command(migrate_db_command)
