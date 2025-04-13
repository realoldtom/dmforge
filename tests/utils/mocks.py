# tests/utils/mocks.py

from weasyprint import HTML as WeasyHTML


class HTMLCapture:
    """Context manager to capture HTML string passed to WeasyPrint.HTML(string=...)"""

    def __init__(self):
        self.captured = {}

    def __enter__(self):
        self._original_html = WeasyHTML

        def mock_HTML(*args, **kwargs):
            self.captured["html"] = kwargs.get("string", "")
            return self._original_html(*args, **kwargs)

        import src.deck_forge.render_pdf as render_pdf

        self._render_pdf = render_pdf
        self._render_pdf.HTML = mock_HTML
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._render_pdf.HTML = self._original_html
