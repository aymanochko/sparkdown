"""
SparkDown - Markdown Renderer Module
Handles markdown rendering to HTML and PDF
"""

import os
import tempfile

import markdown


class MarkdownRenderer:
    """Renders markdown content to various formats"""

    # HTML template with dark theme
    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg-color: #1E1E1E;
            --text-color: #D4D4D4;
            --heading-color: #569CD6;
            --code-bg: #2D2D2D;
            --code-color: #CE9178;
            --link-color: #4EC9B0;
            --border-color: #3C3C3C;
            --blockquote-border: #4EC9B0;
            --table-border: #3C3C3C;
        }}

        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: var(--heading-color);
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }}

        h1 {{ border-bottom: 2px solid var(--border-color); padding-bottom: 0.3em; }}
        h2 {{ border-bottom: 1px solid var(--border-color); padding-bottom: 0.2em; }}

        a {{
            color: var(--link-color);
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        code {{
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: var(--code-bg);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            color: var(--code-color);
        }}

        pre {{
            background-color: var(--code-bg);
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
        }}

        pre code {{
            padding: 0;
            background: none;
        }}

        blockquote {{
            border-left: 4px solid var(--blockquote-border);
            margin: 1em 0;
            padding: 0.5em 1em;
            background-color: rgba(78, 201, 176, 0.1);
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}

        th, td {{
            border: 1px solid var(--table-border);
            padding: 0.5em 1em;
            text-align: left;
        }}

        th {{
            background-color: var(--code-bg);
        }}

        hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 2em 0;
        }}

        img {{
            max-width: 100%;
            height: auto;
        }}

        ul, ol {{
            padding-left: 2em;
        }}

        li {{
            margin: 0.3em 0;
        }}

        .task-list-item {{
            list-style: none;
            margin-left: -1.5em;
        }}

        .task-list-item input {{
            margin-right: 0.5em;
        }}

        /* Syntax highlighting colors */
        .highlight .hll {{ background-color: #ffffcc }}
        .highlight .c {{ color: #6A9955; font-style: italic }} /* Comment */
        .highlight .k {{ color: #569CD6 }} /* Keyword */
        .highlight .o {{ color: #D4D4D4 }} /* Operator */
        .highlight .cm {{ color: #6A9955; font-style: italic }} /* Comment.Multiline */
        .highlight .cp {{ color: #569CD6 }} /* Comment.Preproc */
        .highlight .c1 {{ color: #6A9955; font-style: italic }} /* Comment.Single */
        .highlight .cs {{ color: #6A9955; font-style: italic }} /* Comment.Special */
        .highlight .gd {{ color: #F14C4C }} /* Generic.Deleted */
        .highlight .ge {{ font-style: italic }} /* Generic.Emph */
        .highlight .gr {{ color: #F14C4C }} /* Generic.Error */
        .highlight .gh {{ color: #569CD6; font-weight: bold }} /* Generic.Heading */
        .highlight .gi {{ color: #4EC9B0 }} /* Generic.Inserted */
        .highlight .go {{ color: #808080 }} /* Generic.Output */
        .highlight .gp {{ color: #569CD6; font-weight: bold }} /* Generic.Prompt */
        .highlight .gs {{ font-weight: bold }} /* Generic.Strong */
        .highlight .gu {{ color: #569CD6; font-weight: bold }} /* Generic.Subheading */
        .highlight .gt {{ color: #F14C4C }} /* Generic.Traceback */
        .highlight .kc {{ color: #569CD6 }} /* Keyword.Constant */
        .highlight .kd {{ color: #569CD6 }} /* Keyword.Declaration */
        .highlight .kn {{ color: #4EC9B0 }} /* Keyword.Namespace */
        .highlight .kp {{ color: #569CD6 }} /* Keyword.Pseudo */
        .highlight .kr {{ color: #569CD6 }} /* Keyword.Reserved */
        .highlight .kt {{ color: #DCDCAA }} /* Keyword.Type */
        .highlight .m {{ color: #B5CEA8 }} /* Literal.Number */
        .highlight .s {{ color: #CE9178 }} /* Literal.String */
        .highlight .na {{ color: #9CDCFE }} /* Name.Attribute */
        .highlight .nb {{ color: #569CD6 }} /* Name.Builtin */
        .highlight .nc {{ color: #4EC9B0; font-weight: bold }} /* Name.Class */
        .highlight .no {{ color: #569CD6 }} /* Name.Constant */
        .highlight .nd {{ color: #DCDCAA }} /* Name.Decorator */
        .highlight .ni {{ color: #569CD6 }} /* Name.Entity */
        .highlight .ne {{ color: #4EC9B0; font-weight: bold }} /* Name.Exception */
        .highlight .nf {{ color: #DCDCAA }} /* Name.Function */
        .highlight .nl {{ color: #9CDCFE }} /* Name.Label */
        .highlight .nn {{ color: #569CD6 }} /* Name.Namespace */
        .highlight .nt {{ color: #569CD6; font-weight: bold }} /* Name.Tag */
        .highlight .nv {{ color: #9CDCFE }} /* Name.Variable */
        .highlight .ow {{ color: #D4D4D4 }} /* Operator.Word */
        .highlight .w {{ color: #D4D4D4 }} /* Text.Whitespace */
        .highlight .mf {{ color: #B5CEA8 }} /* Literal.Number.Float */
        .highlight .mh {{ color: #B5CEA8 }} /* Literal.Number.Hex */
        .highlight .mi {{ color: #B5CEA8 }} /* Literal.Number.Integer */
        .highlight .mo {{ color: #B5CEA8 }} /* Literal.Number.Oct */
        .highlight .sb {{ color: #CE9178 }} /* Literal.String.Backtick */
        .highlight .sc {{ color: #CE9178 }} /* Literal.String.Char */
        .highlight .sd {{ color: #CE9178 }} /* Literal.String.Doc */
        .highlight .s2 {{ color: #CE9178 }} /* Literal.String.Double */
        .highlight .se {{ color: #CE9178; font-weight: bold }} /* Literal.String.Escape */
        .highlight .sh {{ color: #CE9178 }} /* Literal.String.Heredoc */
        .highlight .si {{ color: #CE9178 }} /* Literal.String.Interpol */
        .highlight .sx {{ color: #CE9178 }} /* Literal.String.Other */
        .highlight .sr {{ color: #CE9178 }} /* Literal.String.Regex */
        .highlight .s1 {{ color: #CE9178 }} /* Literal.String.Single */
        .highlight .ss {{ color: #CE9178 }} /* Literal.String.Symbol */
        .highlight .bp {{ color: #569CD6 }} /* Name.Builtin.Pseudo */
        .highlight .vc {{ color: #9CDCFE }} /* Name.Variable.Class */
        .highlight .vg {{ color: #9CDCFE }} /* Name.Variable.Global */
        .highlight .vi {{ color: #9CDCFE }} /* Name.Variable.Instance */
        .highlight .il {{ color: #B5CEA8 }} /* Literal.Number.Integer.Long */
    </style>
</head>
<body>
{content}
</body>
</html>"""

    def __init__(self):
        """Initialize the markdown renderer"""
        self._setup_extensions()

    def _setup_extensions(self):
        """Setup markdown extensions"""
        self.extensions = [
            "extra",
            "codehilite",
            "tables",
            "toc",
            "fenced_code",
            "nl2br",
            "sane_lists",
            "def_list",
            "abbr",
            "attr_list",
            "legacy_attrs",
            "md_in_html",
        ]

        self.extension_configs = {
            "codehilite": {"css_class": "highlight", "linenums": False},
            "toc": {"permalink": True},
        }

    def render_to_html(self, markdown_content: str, title: str = "SparkDown Document") -> str:
        """Convert markdown to HTML"""
        md = markdown.Markdown(extensions=self.extensions, extension_configs=self.extension_configs)

        html_content = md.convert(markdown_content)

        # Wrap in full HTML document
        full_html = self.HTML_TEMPLATE.format(title=title, content=html_content)

        return full_html

    def render_to_html_fragment(self, markdown_content: str) -> str:
        """Convert markdown to HTML fragment (without full document)"""
        md = markdown.Markdown(extensions=self.extensions, extension_configs=self.extension_configs)

        return md.convert(markdown_content)

    def render_to_pdf(
        self, markdown_content: str, output_path: str, title: str = "SparkDown Document"
    ) -> bool:
        """Convert markdown to PDF using weasyprint"""
        try:
            from weasyprint import HTML

            html_content = self.render_to_html(markdown_content, title)

            # Write to temporary HTML file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".html", delete=False, encoding="utf-8"
            ) as tmp:
                tmp.write(html_content)
                tmp_path = tmp.name

            try:
                # Convert HTML to PDF
                HTML(filename=tmp_path).write_pdf(output_path)
                return True
            finally:
                # Cleanup temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        except ImportError:
            raise ImportError(
                "weasyprint is required for PDF export. Install with: pip install weasyprint"
            ) from None
        except Exception as e:
            raise RuntimeError(f"PDF conversion failed: {e}") from e

    def get_toc(self, markdown_content: str) -> list:
        """Extract table of contents from markdown"""
        md = markdown.Markdown(extensions=["toc"])
        md.convert(markdown_content)

        if hasattr(md, "Meta") and "toc" in md.Meta:
            return md.Meta.get("toc", [])
        return []

    def get_word_count(self, markdown_content: str) -> int:
        """Count words in markdown content"""
        # Remove code blocks
        import re

        text = re.sub(r"```[\s\S]*?```", "", markdown_content)
        text = re.sub(r"`[^`]+`", "", text)

        # Remove markdown syntax
        text = re.sub(r"[#*\-\[\](){}|]", "", text)

        # Count words
        words = text.split()
        return len(words)

    def get_line_count(self, markdown_content: str) -> int:
        """Count lines in markdown content"""
        return len(markdown_content.split("\n"))
