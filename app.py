"""
FoxBot Grid Trading Flask Web App.

This is a minimalist Flask web app for the FoxBot Grid Trading platform.
It renders the 'index.html' template.

Author: Sebastien Tetaud
Email: tetaud.sebastien@gmail.com
Date: August 9, 2023
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the index.html template.

    Returns:
        str: Rendered HTML content.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
