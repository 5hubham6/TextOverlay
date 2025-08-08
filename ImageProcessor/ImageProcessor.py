# Image processing for text overlays
import textwrap
from random import randrange, randint
from PIL import Image, ImageDraw, ImageFont

class ImageProcessor:
    # Handles putting text on images
    
    def __init__(self, output_dir='./out_img'):
        self.output_dir = output_dir

    
    def make_meme(self, img_path, text: str, author: str, width=500, 
                  font_size=30, font_family='Impact', text_color='white', position_x=50, position_y=50, 
                  add_outline=True) -> str:
        # Main function - adds text to an image
        
        self.img_path = img_path
        self.text = text
        self.author = author
        self.width = width

        try:
            img = Image.open(img_path)
        except(FileNotFoundError):
            raise Exception('Cannot open image file')
        
        # Resize image while maintaining aspect ratio
        ratio = width / float(img.size[0])
        height = int(ratio * float(img.size[1]))
        img = img.resize((width, height), Image.NEAREST)

        draw = ImageDraw.Draw(img)
        
        # Try to load custom font with selected family, fallback to system fonts
        font_candidates = [
            f'{font_family}',  # System font
            './fonts/LilitaOne-Regular.ttf',  # Custom font
            'arial.ttf',  # Windows system font
            'Arial.ttf',  # Alternative Arial
            'helvetica.ttf',  # macOS/Linux
        ]
        
        font = None
        for font_candidate in font_candidates:
            try:
                if font_candidate.endswith('.ttf'):
                    font = ImageFont.truetype(font_candidate, size=font_size)
                else:
                    # Try to use system font
                    font = ImageFont.truetype(font_candidate, size=font_size)
                break
            except:
                continue
        
        # Final fallback to default font
        if font is None:
            try:
                font = ImageFont.load_default()
                # Scale default font size (it's quite small)
                font = ImageFont.load_default().font_variant(size=font_size//2)
            except:
                font = ImageFont.load_default()
        
        # Convert position percentages to actual coordinates
        text_x_position = int((position_x / 100) * width)
        text_y_position = int((position_y / 100) * height)
        
        # Define color mapping
        color_map = {
            'white': 'white',
            'black': 'black',
            'red': '#FF0000',
            'blue': '#0000FF',
            'green': '#00FF00',
            'yellow': '#FFFF00',
            'purple': '#800080',
            'orange': '#FFA500'
        }
        
        text_fill_color = color_map.get(text_color, 'white')
        outline_color = 'black' if text_color == 'white' else 'white'
        
        # Wrap text and calculate total text height
        wrapped_lines = textwrap.wrap(text, width=40)  # Adjust wrap width based on font size
        
        # Add author line only if author is provided and not empty
        if author and author.strip():
            author_line = f"- {author.strip()}"
            wrapped_lines.append(author_line)
        
        # Calculate line height and total text block height
        line_height = font_size + 5
        total_text_height = len(wrapped_lines) * line_height
        
        # Adjust starting Y position to center the text block
        start_y = text_y_position - (total_text_height // 2)
        
        # Draw each line of text
        for i, line in enumerate(wrapped_lines):
            # Calculate text width for centering if needed
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            
            # Adjust x position based on text width (center horizontally around the chosen position)
            line_x = text_x_position - (text_width // 2)
            line_y = start_y + (i * line_height)
            
            # Ensure text doesn't go outside image bounds
            line_x = max(5, min(line_x, width - text_width - 5))
            line_y = max(5, min(line_y, height - font_size - 5))
            
            if add_outline:
                # Draw text outline by drawing text in outline color at offset positions
                for dx in [-2, -1, 0, 1, 2]:
                    for dy in [-2, -1, 0, 1, 2]:
                        if dx != 0 or dy != 0:  # Don't draw on the center position
                            draw.text((line_x + dx, line_y + dy), line, font=font, fill=outline_color)
            
            # Draw the main text
            draw.text((line_x, line_y), line, font=font, fill=text_fill_color)

        # Save the image
        try:
            extension = img_path.split('.')[-1]
            filename = f'{randint(0,1000000)}'
            destination = self.output_dir + '/' + filename + '.' + extension
            img.save(destination, format='JPEG')
        except:
            raise Exception('cannot save image into file')

        return destination
    
