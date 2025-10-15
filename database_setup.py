# database_setup.py
import os
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_database():
    """
    Ensures the instance folder exists, creates all database tables,
    and seeds an initial admin user with a hashed password if one doesn't exist.
    """
    # Ensure the 'instance' folder exists where the database will be stored
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"Created directory: {instance_path}")

    # The 'with app.app_context()' is crucial as it sets up the necessary
    # application context for database operations to work.
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

        # Check if the admin user already exists to avoid duplicates
        if not User.query.filter_by(username='admin').first():
            print("Creating default admin user...")
            
            # --- SECURITY: Hash the password before storing it in the database ---
            hashed_pw = generate_password_hash('password123')
            admin_user = User(username='admin', password=hashed_pw, role='admin')
            
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    # This block allows you to run 'python database_setup.py' from the terminal
    create_database()