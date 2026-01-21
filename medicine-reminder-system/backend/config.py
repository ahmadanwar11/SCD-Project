"""
Configuration file for the Medicine Reminder System
This file contains all the settings needed for the application
"""

import os
from datetime import timedelta

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Main configuration class"""

    # Secret key for session management and JWT tokens
    # In production, this should be a strong random string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'medicine-reminder-secret-key-change-in-production'

    # Database configuration - SQLite database file
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'medicine_reminder.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token valid for 24 hours
    JWT_TOKEN_LOCATION = ['headers']  # Only look for JWT in headers
    JWT_COOKIE_CSRF_PROTECT = False  # Disable CSRF protection for bearer tokens

    # CORS settings - Allow frontend to access backend
    CORS_HEADERS = 'Content-Type'

    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
