# Troubleshooting Guide

## Common Issues and Solutions

### Error: "no such column: assigned_user_id"

**Cause:** Your database was created with an older version of the schema.

**Solution 1: Migrate Existing Database (Recommended)**
```bash
export FLASK_APP=webapp
source venv/bin/activate  # On Windows: venv\Scripts\activate
flask migrate-db
```

This will update your existing database to the new schema while preserving all data.

**Solution 2: Reset Database (Loses All Data)**
```bash
# Backup first if you have important data
cp instance/flaskr.sqlite instance/flaskr.sqlite.backup

# Delete and recreate
rm instance/flaskr.sqlite
export FLASK_APP=webapp
flask init-db
flask import-opportunities volunteer_output.csv
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Cause:** Flask is not installed or virtual environment is not activated.

**Solution:**
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r webapp/requirements.txt
```

### Error: "No such table: user"

**Cause:** Database has not been initialized.

**Solution:**
```bash
export FLASK_APP=webapp
flask init-db
```

### Error: Port 5000 is already in use

**Solution 1: Use a different port**
```bash
flask run --port=5001
```

**Solution 2: Kill the process using port 5000**
```bash
# On Linux/Mac
lsof -ti:5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Error: "OperationalError: unable to open database file"

**Cause:** The instance directory doesn't exist or has wrong permissions.

**Solution:**
```bash
# Create instance directory
mkdir -p instance

# On Linux/Mac, set permissions
chmod 755 instance

# Initialize database
export FLASK_APP=webapp
flask init-db
```

### Error: "werkzeug.routing.exceptions.BuildError"

**Cause:** Trying to access a route that doesn't exist or blueprint not registered.

**Solution:**
- Check that all blueprints are registered in `__init__.py`
- Verify the route name matches what's in the code
- Ensure you're using the correct blueprint name

### Issue: CSV Import Fails

**Common causes and solutions:**

1. **Wrong CSV format**
   - Ensure CSV has correct column headers
   - Check for UTF-8 encoding
   - Verify no extra commas or quotes

2. **File not found**
   ```bash
   # Use absolute path or run from project root
   flask import-opportunities /full/path/to/file.csv
   ```

3. **Database locked**
   - Close any other connections to the database
   - Check file permissions

### Issue: Can't Login After Registration

**Solution:**
```bash
# Check if user was created
sqlite3 instance/flaskr.sqlite "SELECT * FROM user;"

# If no users, try registering again
# Check for error messages in the browser
```

### Issue: Static Files (CSS) Not Loading

**Solution 1: Clear browser cache**
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

**Solution 2: Check static folder**
```bash
# Verify CSS file exists
ls -la webapp/static/style.css

# Restart Flask
flask run
```

### Issue: Changes Not Appearing

**Solution:**
```bash
# Make sure you're in development mode
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

### Issue: "Session is unavailable"

**Cause:** SECRET_KEY not set or changed.

**Solution:**
Set a consistent SECRET_KEY in `webapp/__init__.py`:
```python
app.config.from_mapping(
    SECRET_KEY='your-secret-key-here',  # Use a strong random key
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
```

## Database Issues

### View Current Schema
```bash
sqlite3 instance/flaskr.sqlite ".schema"
```

### Check What Tables Exist
```bash
sqlite3 instance/flaskr.sqlite ".tables"
```

### View Table Structure
```bash
sqlite3 instance/flaskr.sqlite "PRAGMA table_info(opportunity);"
```

### Count Records
```bash
sqlite3 instance/flaskr.sqlite "SELECT COUNT(*) FROM opportunity;"
```

## Development Tips

### Enable Debug Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run
```

### View All Routes
```bash
flask routes
```

### Access Python Shell with App Context
```bash
flask shell
```

Then in the shell:
```python
from webapp.db import get_db
db = get_db()
# Run queries
users = db.execute('SELECT * FROM user').fetchall()
print(users)
```

## Migration Checklist

If you're upgrading from an older version:

- [ ] Backup your database: `cp instance/flaskr.sqlite instance/backup.sqlite`
- [ ] Pull latest code: `git pull origin webapp`
- [ ] Update dependencies: `pip install -r webapp/requirements.txt`
- [ ] Run migration: `flask migrate-db`
- [ ] Restart application
- [ ] Test login and basic functionality
- [ ] Re-import data if needed

## Production Issues

### Check Logs
```bash
# If using Gunicorn
tail -f gunicorn.error.log

# If using systemd
journalctl -u webapp -f
```

### Database Backup
```bash
# Create backup
sqlite3 instance/flaskr.sqlite ".backup instance/backup_$(date +%Y%m%d).sqlite"

# Restore backup
cp instance/backup_20260210.sqlite instance/flaskr.sqlite
```

### Permissions Issues
```bash
# Set correct ownership
chown -R www-data:www-data instance/

# Set correct permissions
chmod 755 instance/
chmod 644 instance/flaskr.sqlite
```

## Getting Help

1. Check this troubleshooting guide
2. Review the main README.md
3. Check the error logs for details
4. Search for the specific error message
5. Verify all prerequisites are installed

## Quick Health Check

Run this script to verify everything is set up correctly:

```bash
#!/bin/bash
echo "=== Volunteer Connect Health Check ==="
echo ""

# Check Python
echo -n "Python: "
python3 --version || echo "❌ Not found"

# Check virtual environment
echo -n "Virtual environment: "
if [ -d "venv" ]; then
    echo "✓ Found"
else
    echo "❌ Not found - run: python3 -m venv venv"
fi

# Check Flask
echo -n "Flask installed: "
source venv/bin/activate 2>/dev/null
python -c "import flask; print('✓ Version', flask.__version__)" 2>/dev/null || echo "❌ Not installed"

# Check database
echo -n "Database: "
if [ -f "instance/flaskr.sqlite" ]; then
    echo "✓ Found"
else
    echo "❌ Not found - run: flask init-db"
fi

# Check webapp directory
echo -n "Webapp files: "
if [ -d "webapp" ]; then
    echo "✓ Found"
else
    echo "❌ Not found"
fi

echo ""
echo "=== End Health Check ==="
```

Save as `health_check.sh`, make executable with `chmod +x health_check.sh`, and run with `./health_check.sh`.
