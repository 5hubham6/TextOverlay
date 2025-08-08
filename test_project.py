#!/usr/bin/env python3
"""
Test script for Dynamic Meme Creator
Run this script to verify the project works correctly.
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    try:
        import flask
        import PIL
        import pandas
        import docx
        import requests
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_project_structure():
    """Test that required directories and files exist."""
    print("🔍 Testing project structure...")
    
    required_files = [
        'app.py',
        'meme.py',
        'requirements.txt',
        'README.md',
        'LICENSE'
    ]
    
    required_dirs = [
        'MemeEngine',
        'QuoteEngine', 
        'templates',
        '_data/SimpleLines',
        '_data/photos/images',
        'fonts'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    for dir in required_dirs:
        if not os.path.exists(dir):
            missing_dirs.append(dir)
    
    if missing_files or missing_dirs:
        if missing_files:
            print(f"❌ Missing files: {missing_files}")
        if missing_dirs:
            print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ All required files and directories present")
    return True

def test_quote_loading():
    """Test that quotes can be loaded from sample files."""
    print("🔍 Testing quote loading...")
    try:
        from QuoteEngine import Ingestor
        
        quote_files = [
            './_data/SimpleLines/SimpleLines.txt',
            './_data/SimpleLines/SimpleLines.csv',
            './_data/SimpleLines/SimpleLines.docx'
        ]
        
        total_quotes = 0
        for file in quote_files:
            if os.path.exists(file):
                quotes = Ingestor.parse(file)
                total_quotes += len(quotes)
                print(f"  📄 {file}: {len(quotes)} quotes loaded")
        
        if total_quotes > 0:
            print(f"✅ Successfully loaded {total_quotes} total quotes")
            return True
        else:
            print("❌ No quotes loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error loading quotes: {e}")
        return False

def test_image_availability():
    """Test that sample images are available."""
    print("🔍 Testing image availability...")
    
    images_dir = "_data/photos/images"
    if not os.path.exists(images_dir):
        print(f"❌ Images directory not found: {images_dir}")
        return False
    
    image_files = [f for f in os.listdir(images_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    
    if len(image_files) > 0:
        print(f"✅ Found {len(image_files)} sample images")
        return True
    else:
        print("❌ No image files found")
        return False

def test_meme_generation():
    """Test that memes can be generated."""
    print("🔍 Testing meme generation...")
    try:
        from meme import generate_meme
        
        # Test with default parameters (random)
        result = generate_meme()
        
        if result and os.path.exists(result):
            print(f"✅ Successfully generated meme: {result}")
            return True
        else:
            print("❌ Meme generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error generating meme: {e}")
        return False

def test_flask_app():
    """Test that Flask app can be imported and initialized."""
    print("🔍 Testing Flask application...")
    try:
        from app import app
        
        # Test that app has the required routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        required_routes = ['/', '/create']
        
        missing_routes = [route for route in required_routes if route not in routes]
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        
        print("✅ Flask application initialized successfully")
        print(f"  Available routes: {routes}")
        return True
        
    except Exception as e:
        print(f"❌ Error with Flask app: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Dynamic Meme Creator - Project Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_project_structure,
        test_quote_loading,
        test_image_availability,
        test_meme_generation,
        test_flask_app
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your project is ready to run.")
        print("\n🚀 Quick start commands:")
        print("  Web app: python app.py")
        print("  CLI tool: python meme.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
