# CLI script for creating text overlays
import os
import random
import argparse

from ImageProcessor import ImageProcessor
from TextParser import Parser, Quote


def generate_meme(path=None, body=None, author=None):
    # Generate a text overlay given an image path and quote
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/images/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    elif type(path) == str:
        img = path
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/SimpleLines/SimpleLines.txt',
                       './_data/SimpleLines/SimpleLines.docx',
                       './_data/SimpleLines/SimpleLines.pdf',
                       './_data/SimpleLines/SimpleLines.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Parser.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = Quote(body, author)

    overlay = ImageProcessor('./tmp')
    path = overlay.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Text overlay generator.')
    parser.add_argument('--path', type=str, help='Path of a image file.')
    parser.add_argument('--body', type=str, help='Message to insert into the image.')
    parser.add_argument('--author', type=str, help='Author of the message.')

    args = parser.parse_args()
    path = args.path
    body = args.body
    author = args.author

    print(generate_meme(args.path, args.body, args.author))
