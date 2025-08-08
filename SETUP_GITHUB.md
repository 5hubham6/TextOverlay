# GitHub Setup Instructions

## Creating the Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" button in the top right corner
3. Select "New repository"
4. Repository name: `TextOverlay`
5. Description: `Simple web app for putting text on images - built when I was bored`
6. Make it **Public** (for portfolio visibility)
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Push your code

After creating the repo on GitHub, run these commands:

```bash
cd TextOverlay
git remote add origin https://github.com/YOUR_USERNAME/TextOverlay.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Repository Settings

After pushing:

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll down to "GitHub Pages" 
4. You can add topics/tags like: `flask`, `docker`, `image-processing`, `python`, `text-overlay`

## Additional commits you might want to make

```bash
# Add some improvements later
git add .
git commit -m "added better error handling"
git push

# Or feature additions
git commit -m "improved text positioning algorithm" 
git push

# Keep commit messages casual and personal
git commit -m "fixed that annoying font size bug"
git push
```

Your repo is ready to showcase in your portfolio!
