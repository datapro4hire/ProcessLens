#!/usr/bin/env python3
"""
Production deployment script for ProcessLens
"""

import os
import secrets
import subprocess
import sys
from pathlib import Path

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def check_environment():
    """Check if we're in a production environment"""
    print("🔍 Checking environment...")
    
    # Check for production environment variables
    prod_vars = ['DATABASE_URL', 'GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET']
    missing = [var for var in prod_vars if not os.environ.get(var)]
    
    if missing:
        print(f"❌ Missing production environment variables: {', '.join(missing)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def setup_database():
    """Set up the database"""
    print("🔍 Setting up database...")
    
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
            return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def install_dependencies():
    """Install production dependencies"""
    print("🔍 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_production_config():
    """Create production configuration"""
    print("🔍 Creating production configuration...")
    
    # Generate secret key if not set
    if not os.environ.get('SECRET_KEY'):
        secret_key = generate_secret_key()
        print(f"Generated SECRET_KEY: {secret_key}")
        print("Please set this as an environment variable")
    
    # Check for HTTPS in production
    if os.environ.get('FLASK_ENV') == 'production':
        if not os.environ.get('HTTPS_ENABLED'):
            print("⚠️  Warning: HTTPS not enabled for production")
            print("Please set HTTPS_ENABLED=true for production")
    
    print("✅ Production configuration ready")
    return True

def main():
    """Main deployment function"""
    print("🚀 ProcessLens Production Deployment")
    print("=" * 50)
    
    steps = [
        ("Environment Check", check_environment),
        ("Install Dependencies", install_dependencies),
        ("Setup Database", setup_database),
        ("Production Config", create_production_config)
    ]
    
    passed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            passed += 1
        else:
            print(f"❌ {step_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Deployment Results: {passed}/{total} steps completed")
    
    if passed == total:
        print("🎉 Deployment successful!")
        print("\nProduction checklist:")
        print("✅ Environment variables configured")
        print("✅ Dependencies installed")
        print("✅ Database setup complete")
        print("✅ Production configuration ready")
        print("\nNext steps:")
        print("1. Set up a production web server (Gunicorn, uWSGI)")
        print("2. Configure reverse proxy (Nginx)")
        print("3. Set up SSL certificates")
        print("4. Configure monitoring and logging")
    else:
        print("❌ Deployment failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main() 