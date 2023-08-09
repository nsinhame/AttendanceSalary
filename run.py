# Import the app and database

from main import app, db

# Main driver file
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)