"""Sphinx configuration for the muru-hosting documentation."""

from __future__ import annotations

import sys
from pathlib import Path

# Local extensions.

sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

project = "muru-hosting"
author = "Graham Dumpleton"
copyright = "2026, Graham Dumpleton"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
    "adr_index",
]

source_suffix = {".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "project/adr/template.md"]

# MyST: mermaid fences render as diagrams, and headings get anchors for cross references.

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "tasklist", "attrs_inline"]
myst_fence_as_directive = ["mermaid"]
myst_heading_anchors = 3

html_theme = "furo"
html_title = "muru-hosting"
html_theme_options = {
    "source_repository": "https://github.com/muruhq/muru-hosting/",
    "source_branch": "main",
    "source_directory": "docs/",
}

copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True
