# Volunteer Connect - Quick Start Guide

## Getting Started in 3 Steps

### Step 1: Run the Application

```bash
./run_webapp.sh
```

The script will:
- Create a virtual environment (if needed)
- Install dependencies
- Initialize the database
- Offer to import opportunities from CSV
- Start the web server

### Step 2: Access the Application

Open your browser and go to: **http://127.0.0.1:5000/**

### Step 3: Create an Account

1. Click "Register" or go to http://127.0.0.1:5000/auth/register
2. Choose a username and password
3. Log in with your credentials

## What You Can Do

### For Verifiers

1. **View Your Assigned Opportunities**
   - After login, you'll see opportunities assigned to you
   - Status badges show: Pending, Verified, Rejected, or Needs Review

2. **Assign Opportunities to Yourself**
   - Go to "All Opportunities" in the navigation
   - Click "Assign to Me" on any unassigned opportunity

3. **Verify Opportunities**
   - Click "Verify Now" on any pending opportunity
   - Review all the details
   - Choose a verification status:
     - ✓ **Verified**: Information is accurate
     - ✗ **Rejected**: Information is incorrect/outdated
     - ⚠ **Needs Review**: Uncertain, needs more investigation
   - Add optional notes about your findings
   - Submit your verification

4. **Track Your Progress**
   - Go to "Statistics" to see your completion rate
   - View overall platform statistics

## Common Tasks

### Import Opportunities from CSV

If you have a CSV file with opportunity data:

```bash
export FLASK_APP=webapp
source venv/bin/activate
flask import-opportunities your_file.csv
```

Expected CSV format:
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

### Reset the Database

If you need to start fresh:

```bash
rm instance/flaskr.sqlite
export FLASK_APP=webapp
source venv/bin/activate
flask init-db
flask import-opportunities volunteer_output.csv
```

## Navigation Guide

- **My Opportunities**: Opportunities assigned to you
- **All Opportunities**: Complete list with filtering options
- **Statistics**: Your progress and platform-wide metrics
- **Username Dropdown**: View profile and logout

## Verification Tips

When verifying an opportunity:

1. **Check the URL**: Visit the link to confirm it's active
2. **Verify Details**: Cross-reference organization name, title, and description
3. **Check Dates**: Ensure the position date is current
4. **Location**: Confirm the address or virtual status
5. **Requirements**: Verify age and skill requirements match
6. **Add Notes**: Document any issues or observations

## Troubleshooting

### Can't Access the App?
- Make sure the server is running (you should see "Running on http://127.0.0.1:5000/")
- Check that port 5000 is not already in use

### Database Issues?
- Try resetting the database (see "Reset the Database" above)
- Check that the `instance` directory exists and is writable

### Import Not Working?
- Verify your CSV has the correct column headers
- Check that the CSV file is properly formatted (UTF-8 encoding)

## Keyboard Shortcuts

- **Tab**: Navigate between form fields
- **Enter**: Submit forms
- **Esc**: Close modal dialogs (if implemented)

## Next Steps

Once you're comfortable with the basics:

1. Verify multiple opportunities to build your statistics
2. Use the filter buttons on "All Opportunities" to focus on specific statuses
3. Review the verification history on opportunity detail pages
4. Collaborate with other verifiers by viewing their notes

## Need Help?

- Check the full README at `webapp/README.md`
- Review the database schema in `webapp/schema.sql`
- Inspect the code in the `webapp/` directory

## Production Deployment

For production use:

1. Change the `SECRET_KEY` in `webapp/__init__.py`
2. Set `FLASK_ENV=production`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Configure HTTPS
5. Use a production database (PostgreSQL, MySQL)
6. Set up proper logging and monitoring

---

**Happy Verifying!** 🎯
