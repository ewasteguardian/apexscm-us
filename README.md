# apexscm.us

Hand-coded static website for APEX SCM Corp. No framework, no build dependencies beyond Python 3.

- `build.py` — single source of truth: layout, navigation, page content, metadata. Run `python3 build.py` to regenerate `docs/`.
- `src/` — stylesheet, small JS (mobile nav + reveal), fonts (self-hosted) and images.
- `docs/` — generated output served by GitHub Pages (branch `main`, folder `/docs`). Do not edit by hand.

Preview build for the github.io address: `BASE=/apexscm-us python3 build.py`.
Production build (writes `CNAME` for apexscm.us): `python3 build.py`.

Brand: Midnight Blue `#2e395f` · Harvest Gold `#d0b36f` · Limestone `#ede4d1` · Manrope (headings) · Montserrat (body).

## Contact form

`/contact/` posts to [Web3Forms](https://web3forms.com) (no account; the access key is emailed to
info@apexscm.us). Paste the key into `WEB3FORMS_KEY` in `build.py`, rebuild, push. While the key is
empty the form hands the message to the visitor's mail app instead, so nothing is ever lost.
Submissions arrive at info@ with the visitor's email as Reply-To.
