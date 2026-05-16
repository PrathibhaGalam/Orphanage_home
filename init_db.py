#!/usr/bin/env python
"""
Database Setup Script
Initialize the orphanage management system database
"""

from app import create_app, db

app = create_app('development')

with app.app_context():
    print("🔧 Creating database tables...")
    try:
        db.create_all()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

    try:
        from database.models import User

        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("📝 Creating sample admin user...")
            admin = User(username='admin', email='admin@orphanage.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created (Username: admin, Password: admin123)")
        else:
            print("⚠️  Admin user already exists")
    except Exception as e:
        print(f"⚠️  Warning creating sample data: {e}")

    print("\n✅ Database setup complete!")

        print(f"📝 Ensuring database '{db_name}' exists...")
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Database '{db_name}' ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🏠 Orphanage Management System - Database Setup")
    print("=" * 60)
    
    # Verify connection
    if not verify_connection():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    print("\n✅ Setup complete! You can now run: python run.py")
