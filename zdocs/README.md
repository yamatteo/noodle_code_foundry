# Zola + MATbook Documentation Site

This directory contains a complete Zola static site setup with MATbook theme for automatic deployment.

## Quick Start

### Local Development
```bash
cd zdocs
zola serve
```
Visit http://127.0.0.1:1111

### Build
```bash
cd zdocs
zola build
```
Output in `public/` directory.

## Deployment

### GitHub Pages (Default)
- Push to `main` branch
- GitHub Actions automatically builds and deploys
- Site available at: `${ZOLA_BASE_URL}`

### GitLab Pages (Alternative)
- Use `.gitlab-ci.yml` configuration
- GitLab Runner builds and deploys to Pages
- Uncomment GitLab Pages detection in CI file

## Features

- ✅ MathJax support for mathematical content
- ✅ Chapter navigation with numbering
- ✅ Responsive design
- ✅ Search functionality
- ✅ Git integration

## Content Structure

```
content/
├── _index.md           # Homepage
├── chapter1/           # Python patterns
│   ├── _index.md       # Chapter intro
│   └── section1.md     # Environment management
└── chapter2/           # Agent skills
    ├── _index.md       # Chapter intro
    └── section2.md     # MCP configuration
```

## Theme Configuration

- **Theme**: MATbook
- **MathJax**: Enabled
- **Chapter Numbering**: Enabled
- **Navigation**: Sidebar with chapters/sections

## Customization

Edit `config.toml` to modify:
- Site metadata (title, description)
- Theme settings
- Navigation menu
- MathJax configuration
