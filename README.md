# KYNETYK site

Plain static site, no build step. Runs on GitHub Pages as is.

## Publish
1. Make a new repo on GitHub (e.g. `kynetyk`), upload everything in this folder to the root.
2. Repo > Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`. Save.
3. Live in a minute or two at `https://<username>.github.io/<repo>/`.

Name the repo `<username>.github.io` if you want it at the root domain instead.
Custom domain: add it under Settings > Pages and point DNS at GitHub.

Note: 404.html uses root paths (`/css/...`), so it only looks right on a root domain or custom domain.

## Fill in
Top of `js/site.js`:
- `LINKS.donate` - Ko-fi, GitHub Sponsors, etc
- `LINKS.windows`, `LINKS.mac`, `LINKS.linux` - release downloads
- `LINKS.github` - repo url
- `LINKS.contact` - `mailto:` or a page
- `VERSION`

Empty links show greyed out as "Coming soon".

## Media
`media/demo.mp4` is the looping demo, `media/poster.jpg` its still.
Gallery shots are `media/cuelist.jpg`, `curves.jpg`, `showmode.jpg`, `remote.jpg` (1600x940ish).
`media/og.png` is the link preview image.

Fonts are bundled in `fonts/` (Archivo, Doto, Space Grotesk, all OFL, licences included).
