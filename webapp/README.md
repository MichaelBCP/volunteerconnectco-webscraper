# Volunteer Connect Verification Web Application

A Flask-based web application for managing and verifying volunteer opportunities.

## Features

- **User Authentication**: Secure login and registration system
- **Opportunity Management**: View, manage, and verify volunteer opportunities
- **Assignment System**: Opportunities can be assigned to specific users
- **Verification Workflow**: Multi-status verification system (pending, verified, rejected, needs_review)
- **Statistics Dashboard**: Track verification progress and completion rates
- **Responsive Design**: Modern, mobile-friendly interface

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   export FLASK_APP=webapp
   flask init-db
   ```

4. **Import opportunities from CSV** (optional):
   ```bash
   flask import-opportunities volunteer_output.csv
   ```

## Upgrading from Previous Version

If you already have a database from a previous version:

```bash
export FLASK_APP=webapp
flask migrate-db
```

This will update your existing database to the new schema while preserving all data. See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for more details.

## Running the Application

### Development Mode

```bash
export FLASK_APP=webapp
export FLASK_ENV=development
flask run
```

The application will be available at `http://127.0.0.1:5000/`

### Production Mode

For production, use a proper WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 'webapp:create_app()'
```

## Usage

### First Time Setup

1. **Start the application** using the commands above
2. **Navigate to** `http://127.0.0.1:5000/`
3. **Register a new account** at `/auth/register`
4. **Log in** with your credentials

### Working with Opportunities

1. **View Your Opportunities**: After logging in, you'll see opportunities assigned to you
2. **All Opportunities**: View all opportunities in the system via the navigation menu
3. **Assign Opportunities**: Unassigned opportunities can be self-assigned from the "All Opportunities" page
4. **Verify Opportunities**: Click "Verify Now" on any pending opportunity
5. **View Statistics**: Check your progress and overall platform statistics

### Verification Workflow

When verifying an opportunity, you can set one of these statuses:

- **Verified**: Information is accurate and up-to-date
- **Rejected**: Information is incorrect or outdated
- **Needs Review**: Uncertain, requires additional review

You can also add notes to document your findings.

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password
- `role`: User role (default: 'verifier')
- `created_at`: Registration timestamp

### Opportunities Table
- `id`: Primary key
- `organization_name`: Name of the organization
- `volunteer_title`: Title of the volunteer position
- `url`: Link to the opportunity
- `image`: Image URL
- `position_date`: Date information
- `description`: Full description
- `age_requirement`: Age requirements
- `skill_requirement`: Required skills
- `address_virtual`: Location information
- `passion_areas`: Related passion areas
- `specific_skills`: Specific skills needed
- `filters`: Additional filters/tags
- `assigned_user_id`: ID of assigned user (foreign key)
- `verification_status`: Current status (pending/verified/rejected/needs_review)
- `created_at`: Creation timestamp

### Verifications Table
- `id`: Primary key
- `opportunity_id`: Reference to opportunity (foreign key)
- `user_id`: Reference to user who verified (foreign key)
- `status`: Verification status
- `notes`: Optional verification notes
- `verified_at`: Verification timestamp

## File Structure

```
webapp/
├── __init__.py              # Application factory
├── auth.py                  # Authentication blueprint
├── db.py                    # Database utilities
├── opportunities.py         # Opportunities blueprint
├── import_opportunities.py  # CSV import command
├── schema.sql              # Database schema
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/
│   └── style.css          # Application styles
└── templates/
    ├── base.html          # Base template
    ├── auth/
    │   ├── login.html    # Login page
    │   └── register.html # Registration page
    └── opportunities/
        ├── index.html    # User's assigned opportunities
        ├── all.html      # All opportunities list
        ├── detail.html   # Opportunity detail view
        ├── verify.html   # Verification form
        └── stats.html    # Statistics dashboard
```

## API Endpoints

### Authentication
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Opportunities
- `GET /` - View assigned opportunities (requires login)
- `GET /all` - View all opportunities (requires login)
- `GET /<id>/detail` - View opportunity details (requires login)
- `GET/POST /<id>/verify` - Verify an opportunity (requires login)
- `POST /<id>/assign` - Assign opportunity to user (requires login)
- `GET /stats` - View statistics (requires login)

## Configuration

You can customize the application by modifying these settings in `__init__.py`:

- `SECRET_KEY`: Change this to a random secret key for production
- `DATABASE`: Path to the SQLite database file

## Importing Data

The application includes a CLI command to import opportunities from CSV files:

```bash
flask import-opportunities path/to/file.csv
```

Expected CSV columns:
- Organization Name
- Volunteer Title
- URL
- Image
- Position Date
- Description
- Age Requirement
- Skill Requirements
- Address/Virtual
- Passion Areas
- Specific Skills
- Filters

## Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Set appropriate file permissions on the database
- Use environment variables for sensitive configuration
- Consider implementing rate limiting for authentication endpoints
- Add CSRF protection for production use

## Future Enhancements

- Admin role with user management
- Bulk assignment of opportunities
- Export verification reports
- Email notifications
- Advanced filtering and search
- Opportunity editing interface
- Batch import improvements
- API for external integrations

## License

See LICENSE file in the root directory.

## Troubleshooting

If you encounter issues:

1. **Database errors**: Run `flask migrate-db` to update your database schema
2. **Module not found**: Ensure virtual environment is activated and dependencies installed
3. **Port in use**: Use `flask run --port=5001` to use a different port

See [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) for detailed solutions.

## Support

For issues or questions, please contact the development team.
