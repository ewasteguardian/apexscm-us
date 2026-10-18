# apexscm.us

Hand-coded static website for APEX SCM Corp. No framework, no build dependencies beyond Python 3.

- `build.py` — single source of truth: layout, navigation, page content, metadata. Run `python3 build.py` to regenerate `docs/`.
- `src/` — stylesheet, small JS (mobile nav + reveal), fonts (self-hosted), images, and the NACM Summit overview PDF.
- `docs/` — generated output served by GitHub Pages (branch `main`, folder `/docs`). Do not edit by hand.

Preview build for the github.io address: `BASE=/apexscm-us python3 build.py`.
Production build (writes `CNAME` for apexscm.us): `python3 build.py`.

Brand: Midnight Blue `#2e395f` · Harvest Gold `#d0b36f` · Limestone `#ede4d1` · Manrope (headings) · Montserrat (body).
