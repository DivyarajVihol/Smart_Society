---
name: 21st-dev
description: "Search, discover, and install UI components, Tailwind CSS themes, templates, and SVG brand logos from 21st.dev (the design engineer component registry) using the 21st CLI."
---

# 21st.dev Component Registry Skill

Use this skill when you need to find, inspect, or install modern UI components, Tailwind CSS themes, design templates, or SVG logos from [21st.dev](https://21st.dev).

## Quick Reference Commands

All commands can be executed directly via `npx -y @21st-dev/cli`:

### 1. Search Components & Themes
Search for UI elements, cards, hero sections, modals, inputs, and animations:
```bash
# Search for components
npx -y @21st-dev/cli search "pricing table" --free

# Search specifically for themes
npx -y @21st-dev/cli search "dark modern" --type theme

# Search templates
npx -y @21st-dev/cli search "dashboard" --type template
```

### 2. Retrieve Component Source Code
Inspect the complete code and implementation of a component found via search:
```bash
npx -y @21st-dev/cli get <component-id>
```

### 3. Install a Component
Install a published component into your project by author and slug:
```bash
npx -y @21st-dev/cli add <author>/<slug>
```

### 4. Fetch Theme CSS
Get the CSS variables for light and dark modes:
```bash
npx -y @21st-dev/cli theme <theme-id>
```

### 5. Search & Download SVG Brand/UI Logos
Free, instant SVG search (no authentication required):
```bash
npx -y @21st-dev/cli logo <brand-name>
```

### 6. Review Local UI
Run deterministic local UI/UX review checks:
```bash
npx -y @21st-dev/cli review <path-to-file-or-dir>
```

---

## Authentication & API Keys (Optional)
While public search and logo retrieval work out of the box, advanced features (like private drafts or AI sketch generations) can use an API key:
- Sign in: `npx -y @21st-dev/cli login` or set the environment variable `TWENTYFIRST_TOKEN` / `API_KEY_21ST`.
- Get a free key at [https://21st.dev/mcp](https://21st.dev/mcp).
