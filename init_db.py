#!/usr/bin/env python3
"""
Database initialization script for ProcessLens
Creates the PostgreSQL database and tables
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from app import app, db

def init_database():
    """Initialize the database and create tables"""
    load_dotenv()
    
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL', 'postgresql://localhost/processlens')
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Create tables within app context
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Available tables: {', '.join(tables)}")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Ensure the database exists")
        print("4. Verify your database credentials")
        sys.exit(1)

if __name__ == '__main__':
    print("🚀 Initializing ProcessLens database...")
    init_database()
    print("✅ Database initialization complete!") 