# Quick Fix for "no such column: assigned_user_id" Error

## The Problem
You're getting this error:
```
sqlite3.OperationalError: no such column: assigned_user_id
```

## The Solution

Run this single command to fix your database:

```bash
flask migrate-db
```

### Step-by-Step Instructions

#### On Windows (PyCharm):
```bash
# 1. Open Terminal in PyCharm (bottom panel)

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Set Flask app
set FLASK_APP=webapp

# 4. Run migration
flask migrate-db

# 5. Restart your application
flask run
```

#### On Linux/Mac:
```bash
# 1. Open terminal in project directory

# 2. Activate virtual environment
source venv/bin/activate

# 3. Set Flask app
export FLASK_APP=webapp

# 4. Run migration
flask migrate-db

# 5. Restart your application
flask run
```

## What This Does

The migration command will:
- ✅ Check your current database schema
- ✅ Add any missing columns
- ✅ Rename old columns to new names
- ✅ Create missing tables
- ✅ **Preserve all your existing data**

No data will be lost!

## Verification

After running the migration, you should see output like:
```
Checking database schema...
Migrations applied successfully:
  ✓ Added assigned_user_id column
  ✓ Added verification_status column
  ✓ Created verification table
Database migration complete!
```

## Alternative: Start Fresh

If you don't have important data and want to start over:

```bash
# Delete the database
rm instance/flaskr.sqlite

# Recreate it
flask init-db

# Import data
flask import-opportunities volunteer_output.csv

# Run the app
flask run
```

## Still Having Issues?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more detailed solutions.

## Quick Access to Your App

After fixing:
1. Open browser
2. Go to: http://127.0.0.1:5000/
3. Login with your account
4. Start verifying opportunities!
