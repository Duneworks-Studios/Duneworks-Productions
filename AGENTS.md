# AGENTS.md

## Learned User Preferences

- Demands premium, award-level (Awwwards-caliber) design quality; rejects anything that feels amateur, like a generic SaaS template, or AI-generated.
- Dislikes forced or unreliable animations; wants one coherent, polished motion system rather than patched-together effect layers.
- Prefers iterating on the existing site over full rebuilds: first inspect and understand what already works, then improve in place and remove only what is broken or low-quality.
- Current theme direction: pure black-and-white monochrome (no red accent), minimalistic typography with Inter, and smaller uppercase headings with wide letter-spacing.
- Wants the logo to have a transparent background, with a dark-text variant used in light theme.
- Expects the agent to boot or restart the local dev server and share the localhost link after site changes, and to stop the server when asked to "turn site off".
- Expects the agent to commit and push changes to the GitHub repository when asked.

## Learned Workspace Facts

- Static single-page marketing site for Duneworks Productions (cinematography / motorsport media agency); the entire app is one `index.html` (~5,400 lines of inline HTML/CSS/JS) with no framework, no build system, and no package manifest.
- Git remote is `https://github.com/Duneworks-Studios/Duneworks-Productions.git`, branch `main`.
- Local preview is served with a static file server at `http://localhost:5500`.
- Site features include trilingual i18n (EN/RU/UZ via `data-i18n` attributes), a light/dark theme toggle, an intro loading screen, a custom camera cursor, a partner logo marquee, a "Duna AI" chat widget backed by the DeepSeek API, and a contact form posting to formsubmit.co.
- Brand logo files live in `assets/` as `duneworks-logo.png` (dark theme) and `duneworks-logo-light.png` (light theme); their transparent backgrounds were generated with `process_logo.py`.
- Keep secrets out of client-side code and chat: a DeepSeek API key was previously exposed in `index.html` and a GitHub token was once pasted in chat; treat any exposed credential as compromised and never commit one.
