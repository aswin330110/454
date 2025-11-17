#!/bin/bash

echo "================================================================================"
echo "           ADVANCED GIT ZIP EXTRACTOR - WEB INTERFACE"
echo "================================================================================"
echo ""
echo "Starting web server..."
echo ""
echo "Once started, open your browser and go to:"
echo ""
echo "    http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server when done"
echo ""
echo "================================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing required dependencies..."
    echo ""
    pip3 install -r requirements.txt
    echo ""
fi

# Start the web application
python3 web_app.py
