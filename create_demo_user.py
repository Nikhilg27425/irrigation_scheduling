"""Create a demo user for testing"""
from app import app, db, User

with app.app_context():
    # Create tables
    db.create_all()
    
    # Check if demo user exists
    demo_user = User.query.filter_by(username='farmer').first()
    
    if not demo_user:
        # Create demo user
        demo_user = User(
            username='farmer',
            email='farmer@example.com',
            farm_name='Green Valley Farm',
            location='Punjab, India',
            farm_size=25.5
        )
        demo_user.set_password('farmer123')
        
        db.session.add(demo_user)
        db.session.commit()
        
        print("✓ Demo user created successfully!")
        print("\nLogin credentials:")
        print("Username: farmer")
        print("Password: farmer123")
    else:
        print("Demo user already exists!")
        print("\nLogin credentials:")
        print("Username: farmer")
        print("Password: farmer123")
