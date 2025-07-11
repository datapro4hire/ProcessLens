#!/usr/bin/env python3
"""
Test script to verify ProcessLens setup
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔍 Testing environment variables...")
    
    required_vars = [
        'SECRET_KEY',
        'DATABASE_URL',
        'GITHUB_CLIENT_ID',
        'GITHUB_CLIENT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    else:
        print("✅ All environment variables are set")
        return True

def test_imports():
    """Test Python imports"""
    print("🔍 Testing Python imports...")
    
    try:
        import flask
        import flask_dance
        import flask_sqlalchemy
        import flask_login
        import flask_session
        # Note: psycopg2 not needed for SQLite development
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Test connection with SQLite
            db.engine.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your DATABASE_URL and ensure the database is accessible")
        return False

def test_app_creation():
    """Test Flask app creation"""
    print("🔍 Testing Flask app creation...")
    
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ProcessLens Setup Test")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    tests = [
        test_environment,
        test_imports,
        test_app_creation,
        test_database_connection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ProcessLens is ready to run.")
        print("\nNext steps:")
        print("1. Set up GitHub OAuth (see README.md)")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
        print("4. Click 'Login with GitHub' to test authentication")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 