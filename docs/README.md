# Documentation Site

This directory contains the documentation for doctai, organized for GitHub Pages.

## Structure

```
docs/
├── index.md              # Home page
├── getting-started/      # Installation and setup guides
├── guides/               # Feature guides and how-tos
├── reference/            # Technical reference
├── changelog/            # Feature changelogs
├── _config.yml           # Jekyll configuration
└── Gemfile              # Ruby dependencies
```

## Local Development

To run the documentation site locally:

```bash
cd docs

# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Open http://localhost:4000
```

## GitHub Pages Setup

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` or `master`
4. Folder: `/docs`
5. Save

GitHub will automatically build and deploy your documentation.

## Customization

Edit `_config.yml` to customize:
- Site title and description
- Theme and colors
- Navigation
- Footer
- GitHub links

## Theme

This site uses [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme, which provides:
- Clean, modern design
- Built-in search
- Responsive navigation
- Code syntax highlighting
- Dark mode support
- Mobile-friendly

## Adding New Pages

1. Create a new `.md` file in the appropriate directory
2. Add front matter:
   ```yaml
   ---
   layout: default
   title: Page Title
   parent: Section Name
   nav_order: 1
   ---
   ```
3. Write your content in Markdown
4. Commit and push

## Links

- [Just the Docs Documentation](https://just-the-docs.github.io/just-the-docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)

