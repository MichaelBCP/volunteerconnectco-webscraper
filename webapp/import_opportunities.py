import csv
import sqlite3
import click
from flask import current_app
from webapp.db import get_db


@click.command('import-opportunities')
@click.argument('csv_file')
def import_opportunities_command(csv_file):
    """Import opportunities from a CSV file."""
    db = get_db()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            try:
                db.execute(
                    'INSERT INTO opportunity ('
                    'organization_name, volunteer_title, url, image, position_date, '
                    'description, age_requirement, skill_requirement, address_virtual, '
                    'passion_areas, specific_skills, filters'
                    ') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (
                        row.get('Organization Name', ''),
                        row.get('Volunteer Title', ''),
                        row.get('URL', ''),
                        row.get('Image', ''),
                        row.get('Position Date', ''),
                        row.get('Description', ''),
                        row.get('Age Requirement', ''),
                        row.get('Skill Requirements', ''),
                        row.get('Address/Virtual', ''),
                        row.get('Passion Areas', ''),
                        row.get('Specific Skills', ''),
                        row.get('Filters', '')
                    )
                )
                count += 1
            except Exception as e:
                click.echo(f'Error importing row: {e}')
                continue
        
        db.commit()
        click.echo(f'Successfully imported {count} opportunities.')


def init_app(app):
    app.cli.add_command(import_opportunities_command)
