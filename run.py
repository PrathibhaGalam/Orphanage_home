import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Add database to shell context"""
    return {'db': db}

if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
