#!/usr/bin/env python3
"""
A self-contained diagnostic script to debug PDF rendering issues.
Run this directly to test image rendering in isolation.
"""

from pathlib import Path
import json
import sys
from weasyprint import HTML
from jinja2 import Template

# Simple HTML template with direct image display for testing
TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Test</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .card { margin: 20px; padding: 10px; border: 1px solid #ccc; }
        .title { font-weight: bold; }
        img { max-width: 300px; border: 1px dashed red; }
    </style>
</head>
<body>
    <h1>Image Path Test</h1>
    {% for card in cards %}
    <div class="card">
        <div class="title">{{ card.title }}</div>
        <p>Path: {{ card.art_url }}</p>
        <img src="{{ card.art_url }}" alt="{{ card.title }}">
    </div>
    {% endfor %}
</body>
</html>
"""


def test_image_rendering(deck_path, output_dir):
    """Test image rendering with a minimal example."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load deck
    deck_path = Path(deck_path)
    print(f"Loading deck from {deck_path.absolute()}")

    try:
        data = json.loads(deck_path.read_text(encoding="utf-8"))
        cards = data.get("cards", []) if isinstance(data, dict) else data

        if not cards:
            print("No cards found in deck!")
            return

        # Process image paths
        base_dir = deck_path.parent
        for card in cards:
            if "art_url" in card:
                path_str = card["art_url"]
                if not path_str.startswith(("http://", "https://", "file://")):
                    path = Path(path_str)
                    if not path.is_absolute():
                        path = (base_dir / path).resolve()
                    if path.exists():
                        card["art_url"] = path.as_uri()
                        print(f"✓ Image exists: {path}")
                    else:
                        print(f"✗ Image NOT found: {path}")
                        # Fall back to a placeholder
                        card["art_url"] = (
                            "https://via.placeholder.com/300x180?text=Missing+Image"
                        )

        # Generate test HTML
        template = Template(TEST_HTML)
        html_string = template.render(cards=cards)

        # Save HTML for inspection
        html_path = output_dir / "test_images.html"
        html_path.write_text(html_string, encoding="utf-8")
        print(f"HTML saved to {html_path.absolute()}")

        # Render PDF
        pdf_path = output_dir / "test_images.pdf"
        HTML(string=html_string).write_pdf(str(pdf_path))
        print(f"PDF saved to {pdf_path.absolute()}")

        # List all image paths for reference
        path_file = output_dir / "image_paths.txt"
        with path_file.open("w", encoding="utf-8") as f:
            for idx, card in enumerate(cards):
                f.write(f"Card {idx+1}: {card.get('title', 'Untitled')}\n")
                f.write(f"Image: {card.get('art_url', 'No image')}\n\n")

        print(f"Image paths saved to {path_file.absolute()}")

    except Exception as e:
        import traceback

        print(f"Error: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_test.py path/to/deck.json [output_dir]")
        sys.exit(1)

    deck_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "debug_output"

    test_image_rendering(deck_path, output_dir)
