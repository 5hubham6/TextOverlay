# TextOverlay - simple web app for putting text on images
# Built this when I was bored and wanted to make some quick image edits
# Flask app handles the web interface
import random
import os
import requests
import json
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import tempfile
import uuid
from datetime import datetime

from ImageProcessor import ImageProcessor
from TextParser import Parser, Quote

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database setup (ready for when you connect PostgreSQL)
DATABASE_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'textoverlay'),
    'user': os.environ.get('DB_USER', 'textuser'),
    'password': os.environ.get('DB_PASSWORD', 'defaultpass'),
    'port': os.environ.get('DB_PORT', '5432')
}

# File-based user storage
USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Create default demo user if file doesn't exist or is corrupted
    default_users = {
        'demo': {
            'id': str(uuid.uuid4()),
            'username': 'demo',
            'email': 'demo@textoverlay.com',
            'password_hash': generate_password_hash('demo123'),
            'created_at': datetime.now().isoformat()
        }
    }
    save_users(default_users)
    return default_users

def save_users(users_data):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving users: {e}")

# Load users from file
users_db = load_users()

# Initialize image processor 
overlay = ImageProcessor('./static')

# Authentication helpers
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' not in session:
        return None
    user_id = session['user_id']
    for user in users_db.values():
        if user['id'] == user_id:
            return user
    return None

def create_user(username, email, password):
    # Check if user already exists
    for user in users_db.values():
        if user['username'] == username or user['email'] == email:
            return None
    
    # Create new user
    user_id = str(uuid.uuid4())
    user = {
        'id': user_id,
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password),
        'created_at': datetime.now().isoformat()
    }
    users_db[username] = user
    
    # Save to file
    save_users(users_db)
    
    return user


def setup():
    # Load quotes and images on startup
    quote_files = ['./_data/SimpleLines/SimpleLines.txt',
                   './_data/SimpleLines/SimpleLines.docx',
                   './_data/SimpleLines/SimpleLines.pdf',
                   './_data/SimpleLines/SimpleLines.csv']

    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Parser.parse(file))
        except Exception as e:
            print(f"Warning: Could not parse {file}: {e}")

    images_path = "./_data/photos/images/"
    imgs = []
    
    if os.path.exists(images_path):
        for root, dirs, files in os.walk(images_path):
            imgs = [os.path.join(root, name) for name in files 
                   if name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if not imgs:
        print("Warning: No images found in the images directory")
    
    return quotes, imgs


# Load resources at startup
quotes, imgs = setup()


@app.route('/')
def landing_page():
    # Show modern landing page with 3 main options
    return render_template('modern_landing.html')


@app.route('/meme_rand')
def meme_rand():
    # Try Now page with samples and interactive demo
    return render_template('try_now.html')


@app.route('/create', methods=['GET'])
def meme_form():
    # Show the form for making custom overlays - Normal Editor
    return render_template('meme_form.html')


@app.route('/canvas_creator', methods=['GET'])
def canvas_creator():
    # Canvas Creator Pro - Full featured editor with Fabric.js
    return render_template('canvas_creator.html')


@app.route('/advanced', methods=['GET'])
def advanced_editor():
    # Advanced editor with drag and drop positioning
    return render_template('advanced_editor.html')


@app.route('/pro', methods=['GET'])
def professional_editor():
    # Professional editor with modern UI
    return render_template('professional_editor.html')


@app.route('/fabric', methods=['GET'])
def fabric_editor():
    # Legacy Fabric.js Editor (redirect to new Canvas Creator)
    return render_template('fabric_editor.html')


@app.route('/proxy-image')
def proxy_image():
    """Proxy endpoint to fetch external images and serve them to avoid CORS issues.
    
    Returns:
        Flask response with image data or error message.
    """
    image_url = request.args.get('url')
    if not image_url:
        return 'URL parameter required', 400
    
    try:
        # Enhanced headers to avoid blocking (same as in meme_post)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.google.com/'
        }
        
        print(f"Fetching image from: {image_url}")  # Debug log
        response = requests.get(image_url, timeout=15, headers=headers)
        response.raise_for_status()
        
        # Validate content type
        content_type = response.headers.get('content-type', '').lower()
        if not any(img_type in content_type for img_type in ['image/', 'application/octet-stream']):
            return f'Invalid content type: {content_type}', 400
        
        print(f"Successfully fetched image, content-type: {content_type}")  # Debug log
        
        # Return the image with proper headers
        return response.content, 200, {
            'Content-Type': content_type,
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Cache-Control': 'max-age=3600'
        }
    except requests.exceptions.Timeout:
        print(f"Timeout fetching image: {image_url}")
        return 'Request timeout - image took too long to load', 408
    except requests.exceptions.ConnectionError:
        print(f"Connection error fetching image: {image_url}")
        return 'Connection error - could not reach the image URL', 502
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching image: {image_url}, status: {e.response.status_code}")
        return f'HTTP error: {e.response.status_code} - {e.response.reason}', e.response.status_code
    except Exception as e:
        print(f"Unexpected error fetching image: {image_url}, error: {str(e)}")
        return f'Failed to fetch image: {str(e)}', 500


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a custom meme from user input.
    
    Returns:
        str: Rendered HTML template with the generated meme or error page.
    """
    body = request.form.get('body', '').strip()
    author = request.form.get('author', '').strip()
    image_source = request.form.get('image_source', 'url')
    
    # Get new customization parameters
    font_size = int(request.form.get('font_size', 30))
    font_family = request.form.get('font_family', 'Impact')
    text_color = request.form.get('text_color', 'white')
    position_x = int(request.form.get('text_position_x', 50))
    position_y = int(request.form.get('text_position_y', 50))
    add_outline = request.form.get('add_outline') is not None  # Checkbox handling
    
    # Validate input
    if not body:
        return render_template('error.html', error='Quote body is required')
    # Author is now optional - no validation needed

    tmp_path = None
    try:
        if image_source == 'file':
            # Handle file upload
            if 'image_file' not in request.files:
                return render_template('error.html', error='Please select a file to upload')
            
            file = request.files['image_file']
            if file.filename == '':
                return render_template('error.html', error='No file selected')
            
            # Check file extension
            allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
            file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if file_ext not in allowed_extensions:
                return render_template('error.html', error='Invalid file type. Please use JPG, PNG, or GIF')
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=f'.{file_ext}', delete=False) as tmp_file:
                file.save(tmp_file.name)
                tmp_path = tmp_file.name
        
        else:
            # Handle URL download
            image_url = request.form.get('image_url', '').strip()
            if not image_url:
                return render_template('error.html', error='Image URL is required when using URL source')
            
            # Set better headers to avoid 403 errors
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'https://www.google.com/'
            }
            
            # Download the image
            response = requests.get(image_url, timeout=15, headers=headers)
            response.raise_for_status()
            
            # Get file extension from URL
            extension = image_url.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'gif']:
                extension = 'jpg'  # Default extension
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=f'.{extension}', delete=False) as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name
        
        # Generate meme with custom styling
        path = overlay.make_meme(
            tmp_path, body, author,
            font_size=font_size,
            font_family=font_family,
            text_color=text_color,
            position_x=position_x,
            position_y=position_y,
            add_outline=add_outline
        )
        
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        # Convert file system path to web URL
        web_path = path.replace('./static/', '/static/').replace('.\\static\\', '/static/').replace('\\', '/')
        if not web_path.startswith('/static/'):
            # If it's a relative path, ensure it starts with /static/
            filename = os.path.basename(path)
            web_path = f'/static/{filename}'
        
        # Check if this is an AJAX request (for staying on the same page)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'image_path': web_path,
                'message': 'Image created successfully!'
            })
        
        # Default behavior (redirect to separate page)
        return render_template('meme.html', path=web_path)
        
    except requests.RequestException as e:
        # Clean up temporary file if it exists
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': f'Could not download image: {str(e)}',
                'message': 'Image download failed. Please check the URL and try again.'
            }), 400
        
        return render_template('error.html', 
                             error=f'Could not download image: {str(e)}')
    except Exception as e:
        # Clean up temporary file if it exists
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': f'Could not generate meme: {str(e)}',
                'message': 'Image generation failed. Please try again.'
            }), 500
        
        return render_template('error.html', 
                             error=f'Could not generate meme: {str(e)}')


@app.route('/download/<path:filename>')
def download_image(filename):
    """Download generated image with different format options."""
    try:
        # Get the format parameter (default to original)
        format_type = request.args.get('format', 'original')
        
        # Read the source image
        image_path = os.path.join(app.static_folder, filename)
        if not os.path.exists(image_path):
            return "Image not found", 404
        
        from PIL import Image
        img = Image.open(image_path)
        
        # Create a temporary file for the converted image
        import tempfile
        import uuid
        
        if format_type == 'png':
            temp_filename = f"download_{uuid.uuid4()}.png"
            temp_path = os.path.join(app.static_folder, temp_filename)
            img.save(temp_path, 'PNG', optimize=True)
            download_name = f"text-overlay-{uuid.uuid4().hex[:8]}.png"
        elif format_type == 'webp':
            temp_filename = f"download_{uuid.uuid4()}.webp"
            temp_path = os.path.join(app.static_folder, temp_filename)
            img.save(temp_path, 'WEBP', quality=90, optimize=True)
            download_name = f"text-overlay-{uuid.uuid4().hex[:8]}.webp"
        elif format_type == 'pdf':
            temp_filename = f"download_{uuid.uuid4()}.pdf"
            temp_path = os.path.join(app.static_folder, temp_filename)
            # Convert to RGB if necessary for PDF
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                rgb_img.save(temp_path, 'PDF', resolution=100.0)
            else:
                img.save(temp_path, 'PDF', resolution=100.0)
            download_name = f"text-overlay-{uuid.uuid4().hex[:8]}.pdf"
        else:  # original format
            temp_path = image_path
            original_ext = filename.split('.')[-1]
            download_name = f"text-overlay-{uuid.uuid4().hex[:8]}.{original_ext}"
        
        # Send the file and clean up temporary file
        def remove_file(response):
            if temp_path != image_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return response
        
        from flask import send_file
        response = send_file(temp_path, as_attachment=True, download_name=download_name)
        
        # Schedule cleanup after response is sent
        if temp_path != image_path:
            import threading
            def cleanup():
                import time
                time.sleep(5)  # Wait a bit before cleanup
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except:
                    pass
            threading.Thread(target=cleanup).start()
        
        return response
        
    except Exception as e:
        return f"Error downloading image: {str(e)}", 500


@app.route('/test-url')
def test_url():
    # Test endpoint to check if a URL works
    test_url = "https://miro.medium.com/v2/resize:fit:1400/1*GI-td9gs8D5OKZd19mAOqA.png"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(test_url, timeout=15, headers=headers)
        response.raise_for_status()
        
        return {
            'status': 'success',
            'url': test_url,
            'content_type': response.headers.get('content-type'),
            'content_length': len(response.content),
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'status': 'error',
            'url': test_url,
            'error': str(e)
        }


# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check user credentials
        user = users_db.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            
            # Redirect to where they were trying to go, or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
        else:
            # Try to create user
            user = create_user(username, email, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash(f'Account created successfully! Welcome, {user["username"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Username or email already exists.', 'error')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out.', 'info')
    return redirect(url_for('landing_page'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    return render_template('profile.html', user=user)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
