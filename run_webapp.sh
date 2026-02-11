#!/bin/bash

# Volunteer Connect Web Application Runner

echo "Starting Volunteer Connect Web Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r webapp/requirements.txt

# Set Flask app
export FLASK_APP=webapp
export FLASK_ENV=development

# Check if database exists
if [ ! -f "instance/flaskr.sqlite" ]; then
    echo ""
    echo "Initializing database..."
    flask init-db
    
    # Ask if user wants to import data
    if [ -f "volunteer_output.csv" ]; then
        echo ""
        read -p "Would you like to import opportunities from volunteer_output.csv? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Importing opportunities..."
            flask import-opportunities volunteer_output.csv
        fi
    fi
fi

echo ""
echo "================================================"
echo "Volunteer Connect Web Application is starting!"
echo "================================================"
echo ""
echo "Access the application at: http://127.0.0.1:5000/"
echo ""
echo "First time? Register an account at: http://127.0.0.1:5000/auth/register"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run the Flask application
flask run --host=0.0.0.0 --port=5000
