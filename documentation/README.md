# Documentation

This folder contains all documentation-related files for the AIDocGen project.

## Structure

```
documentation/
├── mkdocs.yml          # MkDocs configuration file
├── README.md           # This file
├── source/             # Documentation source files (Markdown)
│   ├── index.md        # Main landing page
│   ├── how-to-guides.md # Setup and usage instructions
│   ├── explanation.md   # Architecture and concepts
│   ├── reference.md     # API reference overview
│   ├── reference/       # Auto-generated API documentation
│   └── stylesheets/     # Custom CSS styling
├── scripts/            # Documentation generation scripts
│   └── generate_docs.py # Automatic code documentation generator
└── build/              # Generated documentation site (auto-generated)
```

## Usage

### Build Documentation

From this directory:

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### How it Works

1. **Source Files**: All documentation content is written in Markdown in the `source/` folder
2. **Auto-generation**: The `scripts/generate_docs.py` script automatically creates documentation for all Python files in the `../microservices/` folder
3. **Build Process**: MkDocs processes the source files and generates a static website in the `build/` folder
4. **Styling**: Custom CSS in `source/stylesheets/extra.css` provides professional styling

### Key Features

- **Automatic Code Documentation**: All 70+ Python files are automatically documented
- **Professional Theme**: Material Design theme with dark/light mode
- **Full-Text Search**: Search across all documentation
- **Responsive Design**: Works on all devices
- **Interactive Navigation**: Easy browsing through component hierarchy

### Customization

- **Content**: Edit files in `source/` folder
- **Styling**: Modify `source/stylesheets/extra.css`
- **Configuration**: Update `mkdocs.yml` for theme and plugin settings
- **Generation Logic**: Modify `scripts/generate_docs.py` for custom documentation generation

This centralized structure keeps all documentation files organized and makes it easy to maintain and deploy the documentation.
