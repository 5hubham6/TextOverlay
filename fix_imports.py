#!/usr/bin/env python3
"""
Quick fix script to update critical imports for renamed modules
"""

import os
import glob

def update_file_imports(file_path, replacements):
    """Update imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
        else:
            print(f"⏭️ No changes needed: {file_path}")
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")

def main():
    print("🔧 Quick Fix: Updating critical imports for renamed modules...")
    
    # Critical replacements to make the app run
    replacements = {
        # Class name updates
        'class QuoteModel:': 'class Quote:',
        'QuoteModel': 'Quote',
        'class IngestorInterface': 'class TextParserInterface',
        'IngestorInterface': 'TextParserInterface',
        'class CSVIngestor': 'class CSVParser',
        'CSVIngestor': 'CSVParser',
        'class DOCXIngestor': 'class DOCXParser', 
        'DOCXIngestor': 'DOCXParser',
        'class TXTIngestor': 'class TXTParser',
        'TXTIngestor': 'TXTParser',
        'class PDFIngestor': 'class PDFParser',
        'PDFIngestor': 'PDFParser',
        'class Ingestor': 'class Parser',
        'class MemeEngine': 'class ImageProcessor',
        'MemeEngine': 'ImageProcessor',
        
        # Import updates
        'from .QuoteModel import QuoteModel': 'from .Quote import Quote',
        'from .IngestorInterface import IngestorInterface': 'from .TextParserInterface import TextParserInterface',
        'from .CSVIngestor import CSVIngestor': 'from .CSVParser import CSVParser',
        'from .DOCXIngestor import DOCXIngestor': 'from .DOCXParser import DOCXParser',
        'from .TXTIngestor import TXTIngestor': 'from .TXTParser import TXTParser',
        'from .PDFIngestor import PDFIngestor': 'from .PDFParser import PDFParser',
        'from .Ingestor import Ingestor': 'from .Parser import Parser',
        'from .MemeEngine import MemeEngine': 'from .ImageProcessor import ImageProcessor',
    }
    
    # Update all Python files
    python_files = glob.glob('**/*.py', recursive=True)
    
    for file_path in python_files:
        if '__pycache__' not in file_path:
            update_file_imports(file_path, replacements)
    
    print("🎉 Critical imports updated! The app should now run.")

if __name__ == "__main__":
    main()
