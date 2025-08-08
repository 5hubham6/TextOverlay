# TextOverlay

Was getting bored and this idea came to mind - a simple web app for putting text on images. Started as just a quick project but ended up adding more features as I went along.

Turns out it's actually pretty useful! 🎯

## What it does

```
📸 Upload Image  →  ✏️ Add Text  →  🎯 Position  →  ⬇️ Export
     |                  |              |             |
  [your pic]      [custom text]   [drag & drop]   [download]
```

- Web interface for adding text to images
- Upload images or paste URLs
- Drag and drop text positioning
- Different fonts, colors, and text effects
- Real-time preview as you edit
- Export your creations
- Works on mobile too

## Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Frontend      │    │   Flask App  │    │  Database   │
│                 │◄──►│              │◄──►│             │
│ • Bootstrap UI  │    │ • Image proc │    │ • Postgres  │
│ • Drag & Drop   │    │ • Text overlay│    │ • User data │
│ • File upload   │    │ • Quote parse│    │ • Images    │
└─────────────────┘    └──────────────┘    └─────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │    Redis     │
                       │   (Cache)    │
                       └──────────────┘
```

## Running it

### Quick start with Docker
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your secure values

docker-compose up
```
Then go to http://localhost:3000

### Manual setup
```bash
pip install -r requirements.txt
python app.py
```

## Current Status

### ✅ What's Working
- Web interface with different editors for different use cases
- Text overlays with basic styling (fonts, colors, outlines)
- Image upload and URL support
- Docker setup with Flask, PostgreSQL, Redis
- Mobile-friendly design
- Image proxy to handle external images

### 🏗️ Infrastructure Setup (Not Connected Yet)
- PostgreSQL database ready but not hooked up
- Redis cache ready but not implemented
- User system designed but no login yet

### 🚀 Next Steps
Connect the database and add user accounts when I get time!

## Features I've built

### Basic Features
- Different editor interfaces for different needs
- Text overlay with custom positioning
- Image upload and URL support
- Responsive design that works on mobile
- Real-time preview

### Under the Hood
- Docker setup with Flask, PostgreSQL, Redis containers
- Image proxy to handle CORS issues
- Tailwind CSS for the UI
- Database schema ready for user accounts
- Build pipeline with PostCSS

### File structure
```
├── app.py              # Main Flask app
├── ImageProcessor/     # Handles image + text combining
├── TextParser/         # Old quote parsing stuff (still there)
├── templates/          # HTML templates
│   ├── modern_landing.html    # Landing page
│   ├── professional_editor.html  # Main editor
│   ├── canvas_creator.html    # Fabric.js editor
│   ├── try_now.html          # Quick demo
│   └── advanced_editor.html  # Another editor option
├── static/             # Generated images
├── _data/             # Sample data
├── package.json       # Frontend build stuff
└── docker-compose.yml # Container setup
```

## Screenshots

### Landing Page
Clean interface with different editor options. Built with Tailwind CSS.

### Different Editors
Multiple ways to add text to images:

**Try Now**: Quick demo with sample images
- Live preview as you type
- Sample images to test with

**Main Editor**: The main text overlay tool
- Drag and drop text positioning
- Font and color controls
- Upload images or use URLs

**Canvas Editor**: Uses Fabric.js for more control
- More precise positioning
- Multiple text layers

## Future ideas (when I get time)

- [x] **Modern Frontend**: ✅ Rebuilt with Tailwind CSS
- [ ] **User accounts**: Connect the database, add login
- [ ] **Templates**: Pre-made layouts and styles
- [ ] **Batch processing**: Upload multiple images at once
- [ ] **Social features**: Share creations, like/comment system
- [ ] **Mobile app**: Native iOS/Android apps
- [ ] **Animation support**: GIF text overlays
- [ ] **AI integration**: Auto-suggest text placement and fonts
- [x] **Export options**: ✅ Different formats working
- [ ] **API endpoints**: Let other apps use this

## Tech stack

**Backend**: Python Flask, PostgreSQL, Redis
**Frontend**: Tailwind CSS, Fabric.js, HTML/CSS/JavaScript
**Infrastructure**: Docker, docker-compose
**Image processing**: Pillow (PIL)
**Build**: PostCSS, Autoprefixer

## Development

### Security Notes
- All passwords and secrets use environment variables
- Copy `.env.example` to `.env` and set your own secure values
- Never commit `.env` file to version control
- Default values are for development only

### Adding new quote parsers
The `TextParser` module uses a strategy pattern. To add support for a new file format:

1. Create a new parser class inheriting from `TextParserInterface`
2. Implement `can_ingest()` and `parse()` methods
3. Add it to the `parsers` list in `Parser.py`

### Database schema
The app uses PostgreSQL with tables for users, images, quotes, and likes. Check `init.sql` for the full schema.

## Why I built this

Honestly just wanted a simple way to add text to images without using heavy software like Photoshop. Also was a good excuse to play around with Docker and learn some new stuff.

What started as a basic Flask app became a fun way to explore modern web design - ended up rebuilding the entire frontend with Tailwind CSS and adding multiple specialized editors. Each one serves a different use case.

The image proxy feature came about because of CORS issues with external images, and the multiple editors happened because I kept thinking "what if someone wants to do X instead?"

Started simple but kept adding features because it was actually pretty useful for making quick social media posts and graphics.

## Contributing

Feel free to fork it or suggest improvements! This is just a personal project but always open to making it better.

Some areas that could use work:
- Hook up the database for user accounts
- Implement Redis caching
- Better mobile experience
- More text effects and fonts
- Add some tests
- Maybe an API

### Development Setup
```bash
# Install frontend stuff
npm install

# Build CSS
npm run build-css

# Run the Flask app
python app.py
```

## License

MIT - do whatever you want with it
