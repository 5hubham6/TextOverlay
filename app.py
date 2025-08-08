# TextOverlay - simple web app for putting text on images
# Built this when I was bored and wanted to make some quick image edits
import random
import os
import requests
from flask import Flask, render_template, request
import tempfile

from ImageProcessor import ImageProcessor
from TextParser import Parser, Quote

app = Flask(__name__)

# Initialize image processor 
overlay = ImageProcessor('./static')


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
        # Add user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
            
            # Download the image
            response = requests.get(image_url, timeout=10)
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
        
        return render_template('meme.html', path=path)
        
    except requests.RequestException as e:
        return render_template('error.html', 
                             error=f'Could not download image: {str(e)}')
    except Exception as e:
        # Clean up temporary file if it exists
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        return render_template('error.html', 
                             error=f'Could not generate meme: {str(e)}')


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
