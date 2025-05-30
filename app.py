"""
app.py - Main application file for Stock Oracle MVP

This module contains the main Flask application for the Stock Oracle MVP,
including route definitions and configuration.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import json
import random
import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import networkx as nx

# Load environment variables
load_dotenv()

# Import API routes
from api import api_bp

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stock_oracle_secret_key')

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Global variables
DEFAULT_THEME = 'dark'

@app.route('/')
def index():
    """Render the main dashboard page."""
    # Get user theme preference from session or cookie
    theme = request.cookies.get('theme', DEFAULT_THEME)
    return render_template('index.html', theme=theme)

@app.route('/toggle-theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark themes."""
    data = request.get_json()
    theme = data.get('theme', DEFAULT_THEME)
    
    response = jsonify({'success': True})
    response.set_cookie('theme', theme)
    
    return response

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', 'False').lower() == 'true')
