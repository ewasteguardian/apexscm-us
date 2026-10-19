#!/usr/bin/env python3
"""Static site generator for apexscm.us.

Single source of truth for layout (header/footer), page content and metadata.
Run:  python3 build.py   ->  writes the deployable site into ./docs (GitHub Pages).
"""
from pathlib import Path
import os, re, shutil

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
SITE = "https://apexscm.us"
BASE = os.environ.get("BASE", "").rstrip("/")  # e.g. "/apexscm-us" for a github.io preview build
EMAIL = "info@apexscm.us"
CONTACT = f"mailto:{EMAIL}?subject=Enquiry%20via%20apexscm.us"

NAV = [("Home", "/"), ("About", "/about/"), ("Solutions", "/solutions/"), ("Services", "/services/")]

# ---------------------------------------------------------------- icons (inline SVG, 24px grid)
I = {
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>',
    "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>',
    "refresh": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M7 16v-5"/><path d="M12 16V8"/><path d="M17 16v-3"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 2 9.5 5.5v9L12 22l-9.5-5.5v-9z"/><path d="M2.5 7.5 12 13l9.5-5.5"/><path d="M12 13v9"/></svg>',
    "file": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h8"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "menu": '<svg class="bars" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg><svg class="x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
}

# ---------------------------------------------------------------- layout
def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for t, h in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="APEX SCM home"><img src="/assets/img/logo.png" alt="APEX SCM" width="1024" height="204"></a>
<nav class="nav" aria-label="Primary">{links}<a class="btn btn-gold btn-sm" href="{CONTACT}">Contact Us</a></nav>
<button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="mobile-nav">{I["menu"]}</button>
</div>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">{links}<a class="btn btn-gold" href="{CONTACT}">Contact Us</a></nav>
</header>'''

def footer():
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in NAV)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div class="foot-brand"><img src="/assets/img/logo-reversed.png" alt="APEX" width="1024" height="319"><p>Integrated circular supply infrastructure for enterprise technology. Precision. Security. Scale.</p></div>
<div><p class="foot-h">Navigation</p><ul class="foot-links">{links}<li><a href="{CONTACT}">Contact</a></li></ul></div>
<div><p class="foot-h">Contact</p><div class="foot-contact"><a href="mailto:{EMAIL}">{EMAIL}</a><span>North America · Europe</span></div></div>
</div>
<div class="foot-bottom"><p>&copy; 2026 APEX SCM Corp. All rights reserved.</p><span class="tag">PRECISION. SECURITY. SCALE.</span></div>
</div></footer>'''

def page(*, title, desc, path, body, og_image="/assets/img/og-cover.jpg"):
    full = "APEX SCM" if path == "/" else f"{title} | APEX SCM"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="APEX SCM">
<meta property="og:title" content="{full}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2e395f">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<link rel="preload" href="/assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script>document.documentElement.classList.add('js')</script><script src="/site.js" defer></script>
</body>
</html>'''

def hero(*, img, eyebrow, h1, lead, actions="", home=False, tagline=True):
    cls = "hero hero-home" if home else "hero hero-sub"
    eb = f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
    act = f'<div class="actions">{actions}</div>' if actions else ""
    tag = '<p class="tagline">PRECISION. SECURITY. SCALE.</p>' if tagline else ""
    return f'''<section class="{cls}"><div class="hero-bg"><img src="/assets/img/{img}" alt="" fetchpriority="high"></div>
<div class="wrap"><div>{eb}<h1>{h1}</h1><p class="lead">{lead}</p>{act}</div></div>{tag}</section>'''

def cards(items, cls="grid grid-4", gold=False, numbered=False):
    out = []
    for n, (icon, h, p) in enumerate(items, 1):
        head = f'<div class="num">{n:02d}</div>' if numbered else (f'<div class="icon">{I[icon]}</div>' if icon else "")
        out.append(f'<div class="card{" card-gold" if gold else ""} reveal">{head}<h3>{h}</h3><p>{p}</p></div>')
    return f'<div class="{cls}">{"".join(out)}</div>'

def checks(items):
    return '<ul class="checks">' + "".join(f'<li>{I["check"]}<span>{t}</span></li>' for t in items) + "</ul>"

# ---------------------------------------------------------------- pages
HOME = hero(
    img="hero-home.webp", home=True, eyebrow="Precision. Security. Scale.",
    h1='Circular Supply<br><span class="gold">Infrastructure</span><br>for Enterprise.',
    lead="APEX operates a fully integrated circular supply platform built for enterprise environments where control, accountability, and performance are non-negotiable.",
    actions=f'<a class="btn btn-gold" href="/solutions/">Our Solutions {I["arrow"]}</a><a class="btn btn-outline" href="/services/">Critical Minerals Supply</a>',
) + f'''
<section class="section-tight section-muted bordered"><div class="wrap reveal">
<p class="eyebrow" style="display:block;margin-bottom:1rem">Strategic Positioning</p>
<p class="statement">APEX is not positioned as a recycler or transactional ITAD provider. <b>We are the infrastructure.</b></p>
<p class="sub">We convert sustainability from discretionary spend into structured enterprise advantage.</p>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Business Impact</span><h2 class="h2">Measurable outcomes across<br>four dimensions.</h2></div>
{cards([
    ("trend", "Financial Performance", "Asset recovery, resale, and material refinement generate return on depreciated technology."),
    ("shield", "Risk Mitigation", "Certified data destruction and secure chain-of-custody reduce legal, reputational, and operational exposure."),
    ("refresh", "Supply Resilience", "Closed-loop reintegration strengthens procurement continuity and material availability."),
    ("chart", "Strategic ESG Alignment", "Quantifiable circular metrics support sustainability mandates and reporting frameworks."),
])}
</div></section>

<section class="section section-muted"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Two operations. One supply chain.</span><h2 class="h2">Electronics recovered in America.<br>Minerals secured for America.</h2></div>
<div class="split">
<a class="service service-link reveal" href="/services/"><figure><img src="/assets/img/hero-home.webp" alt="Enterprise server infrastructure" loading="lazy" style="object-position:center 40%"></figure>
<p class="tag">01 · United States</p><h3>Collection, processing and refining of enterprise electronics.</h3>
<p>Secure, documented recovery of end-of-life technology under chain-of-custody control, returning material value to U.S. supply chains.</p></a>
<a class="service service-link reveal" href="/services/"><figure><img src="/assets/img/mine-aerial.webp" alt="Terraced open-pit mine at sunrise" loading="lazy"></figure>
<p class="tag">02 · International</p><h3>Primary gold and silver production, with co-product critical minerals.</h3>
<p>Export-licensed supply of tungsten, copper, uranium, cobalt, antimony, zinc, lead and iron, allocated exclusively to U.S. refining and off-take partners.</p></a>
</div>
<div class="reveal" style="margin-top:2rem"><a class="btn btn-navy" href="/services/">Explore Our Services {I["arrow"]}</a></div>
</div></section>

<section class="section section-navy"><div class="wrap two-col">
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:1rem">Value Proposition</span>
<h2 class="h2">Where others process waste,<br>APEX engineers circular infrastructure.</h2>
<p class="sub" style="margin-top:1.5rem">APEX converts end-of-life technology from cost exposure into structured enterprise value.</p>
<div style="margin-top:2rem"><a class="btn btn-gold" href="/solutions/">Explore Our Platform {I["arrow"]}</a></div></div>
<div class="reveal">{checks(["Fully integrated lifecycle control","Institutional-grade security infrastructure","Structured, auditable reporting","Multi-margin value capture","Export-licensed critical-mineral supply to the United States","Enterprise partnership model"])}</div>
</div></section>

<section class="section"><div class="wrap cta reveal">
<span class="eyebrow">Get In Touch</span>
<h2 class="h2">Ready to secure your supply chain?</h2>
<p class="sub">Precision execution, documented accountability and scalable infrastructure, from one partner rather than a chain of vendors.</p>
<a class="btn btn-navy" href="{CONTACT}">Contact APEX {I["arrow"]}</a>
</div></section>'''

ABOUT = hero(
    img="hero-about.webp", eyebrow="Our Competitive Advantage",
    h1="We operate as infrastructure.<br>Not a recycler.",
    lead="APEX exists to eliminate waste, unmanaged risk, and fragmented recovery practices in global supply chains.",
) + f'''
<section class="section"><div class="wrap two-col two-col-top">
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:.75rem">Purpose</span><h2 class="h2 h2-sm">Control, accountability, and measurable value.</h2>
<p class="sub" style="margin-top:1.25rem">To bring control, accountability, and measurable value to the circular management of enterprise technology.</p>
<p class="sub" style="margin-top:1rem">We make circularity a standard operating practice, embedding security, structure and performance into every stage of the technology lifecycle.</p></div>
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:.75rem">Vision</span><h2 class="h2 h2-sm">The global benchmark for circular supply infrastructure.</h2>
<p class="sub" style="margin-top:1.25rem">To become the global benchmark for integrated circular supply infrastructure — where technology recovery drives financial performance, risk resilience, and sustainable growth.</p>
<p style="margin-top:1rem;font-weight:600;font-size:.95rem">Transforming end-of-life technology from cost exposure into a continuous source of value and competitive advantage.</p></div>
</div></section>

<section class="section-tight section-navy"><div class="wrap quote reveal">
<blockquote>“APEX is engineered for disciplined growth. We combine operational precision, secure environments, and scalable systems to define a new standard in circular supply infrastructure.”</blockquote>
<span class="eyebrow">Our value is measurable. Our execution is controlled. Our impact compounds over time.</span>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Core Values</span><h2 class="h2">Operational principles that guide<br>execution and partnership.</h2></div>
{cards([
    (None, "Precision", "We execute with technical rigor and documented control. Every asset is tracked. Every process is measured. Every outcome is auditable."),
    (None, "Accountability", "We quantify impact — financial, operational, and environmental. If it cannot be measured, it cannot be claimed."),
    (None, "Discipline", "We prioritize systems over shortcuts and structure over opportunism. Scalable performance requires controlled execution."),
    (None, "Partnership", "We integrate with enterprise operations, not alongside them. Long-term value is built through alignment and trust."),
    (None, "Security", "Data protection and chain-of-custody integrity are non-negotiable. We operate to enterprise and regulatory standards — without compromise."),
], cls="grid grid-3", gold=True, numbered=True)}
</div></section>

<section class="section section-muted"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Strategic Priorities</span><h2 class="h2">Where we are taking<br>the business.</h2></div>
{cards([
    ("check", "Establish Category Leadership", "Position APEX as the benchmark for integrated circular supply infrastructure — not transactional ITAD."),
    ("check", "Drive Enterprise Adoption", "Embed lifecycle recovery into enterprise procurement and risk frameworks as a standard operating requirement."),
    ("check", "Expand Platform Integration", "Scale geographically and vertically, from electronics recovery and refining in the United States to primary mineral production at our international mining operations."),
    ("check", "Increase Margin Capture", "Control more of the lifecycle, from collection to refined material, to optimize value recovery and refinement economics."),
    ("check", "Institutionalize ESG Performance", "Deliver quantifiable sustainability metrics that meet investor, regulatory, and stakeholder scrutiny."),
    ("check", "Secure Critical-Mineral Supply", "Allocate export-licensed co-product minerals from our international mining operations to U.S. refining and off-take partners."),
], cls="grid grid-3")}
</div></section>'''

PILLARS = [
    ("shield", "Security &amp; Risk Control", "Risk is identified, controlled, and auditable.", "Enterprise-grade data destruction and documented chain-of-custody across every lifecycle stage.", "Reduced regulatory exposure. Reduced reputational risk. Verified compliance."),
    ("trend", "Structured Value Recovery", "End-of-life does not equal end-of-value.", "Technology assets are processed through controlled systems that maximize residual and material value.", "Improved asset ROI. Margin recovery. Transparent financial reporting."),
    ("refresh", "Integrated Lifecycle Infrastructure", "No fragmented vendors. No blind spots.", "Collection, processing, refinement, and reintegration operate within one coordinated platform.", "Operational efficiency. Vendor consolidation. Simplified governance."),
    ("chart", "Compliance &amp; ESG Performance", "Sustainability is documented, not implied.", "Quantified environmental metrics and certified processing standards.", "Investor-grade ESG reporting. Regulatory alignment. Stakeholder confidence."),
    ("lock", "Scalable Partnership Model", "APEX embeds into systems, not alongside them.", "Designed to integrate into enterprise procurement and IT governance structures.", "Long-term operational resilience and predictable performance."),
]
VERTICALS = [
    ("Financial Services", "High compliance and data sensitivity requirements."),
    ("Healthcare &amp; Life Sciences", "Regulated asset disposition with audit trail requirements."),
    ("Government &amp; Public Sector", "Certified destruction and security-cleared processing."),
    ("Technology &amp; Telecommunications", "High-volume refresh cycles with multi-site logistics."),
    ("Enterprise Manufacturing", "Complex asset pools requiring lifecycle optimization."),
]
SOLUTIONS = hero(
    img="hero-solutions.webp", eyebrow="Our Platform",
    h1="Five pillars of<br>enterprise infrastructure.",
    lead="Our model integrates collection, secure processing, data destruction, asset refurbishment, material refinement, and reintegration into a controlled ecosystem.",
) + f'''
<section class="section-tight section-muted" style="padding:4rem 0;border-bottom:1px solid var(--border)"><div class="wrap">
<ul class="pills">{"".join(f"<li>{t}</li>" for t in ["Chain-of-custody integrity","Certified data security","Asset value recovery","Regulatory alignment","ESG quantification","Margin capture"])}</ul>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Platform Pillars</span><h2 class="h2">Integrated lifecycle control.</h2></div>
{"".join(f'''<article class="pillar reveal"><div class="n">{n}</div>
<div><div class="icon">{I[ic]}</div><h3>{h}</h3><p class="hook">{hook}</p></div>
<p class="desc">{d}</p>
<div class="impact"><span class="lbl">Enterprise Impact</span>{imp}</div></article>''' for n,(ic,h,hook,d,imp) in enumerate(PILLARS,1))}
</div></section>

<section class="section section-muted"><div class="wrap two-col two-col-top">
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:.75rem">Industry Verticals</span><h2 class="h2 h2-sm" style="margin-bottom:2.5rem">Sectors where risk, compliance, and data sensitivity are high.</h2>
<ul class="verticals">{"".join(f"<li><div><strong>{h}</strong><span>{p}</span></div></li>" for h,p in VERTICALS)}</ul></div>
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:.75rem">What we document</span><h2 class="h2 h2-sm" style="margin-bottom:2.5rem">Records you can hold us to.</h2>
{checks(["Certified data destruction certificates","Chain-of-custody documentation for every asset","Processing facility controls and audit trails","Recovery-rate and material-yield reporting","ESG impact reporting aligned to recognised frameworks","Technical review of our mineral operations, available on request"])}</div>
</div></section>

<section class="section section-navy"><div class="wrap cta reveal">
<span class="eyebrow">Most competitors specialize in one stage.</span>
<h2 class="h2">Few control the full system.</h2>
<p class="sub">From secure collection and refining in the United States to primary mineral production at our international operations, APEX operates the stages others outsource.</p>
<div style="display:flex;flex-wrap:wrap;gap:1rem;justify-content:center"><a class="btn btn-gold" href="{CONTACT}">Engage APEX {I["arrow"]}</a><a class="btn btn-outline" href="/services/">Critical Minerals Supply</a></div>
</div></section>'''

MINERALS_OWN = ["Gold", "Silver"]
MINERALS_PARTNER = ["Tungsten", "Copper", "Uranium", "Cobalt", "Antimony", "Zinc", "Lead", "Iron"]
SERVICES = hero(
    img="rock-specimen.webp", eyebrow="U.S. electronics recovery · International mining · Export licensed",
    h1='Critical minerals.<br><span class="gold">Secured for America.</span>',
    lead="APEX SCM collects, processes and refines electronics in the United States. Internationally, our mining operations produce gold and silver as primary products, and the same mineralized ground hosts the critical minerals American industry depends on. With our export license in place, we are seeking a U.S. refinery or off-take partner to strengthen their supply chain.",
    actions=f'<a class="btn btn-gold" href="#portfolio">View Our Portfolio {I["arrow"]}</a><a class="btn btn-outline" href="{CONTACT}">Start a Conversation</a>',
) + f'''
<section class="section"><div class="wrap">
<div class="section-head reveal"><span class="eyebrow">Two operations. One supply chain.</span><h2 class="h2">What we do, and where.</h2></div>
<div class="split">
<article class="service reveal"><figure><img src="/assets/img/hero-home.webp" alt="Enterprise server infrastructure" loading="lazy" style="object-position:center 40%"></figure>
<p class="tag">01 · In the United States</p><h3>Electronics: collected, processed, refined.</h3>
<p>We are an established operator in the collection, secure processing and refining of end-of-life electronics. Our lifecycle model connects data destruction and refurbishment with material recovery and reintegration, under chain-of-custody control and documented outcomes.</p>
<ul><li>Secure collection and certified data destruction</li><li>Processing, refurbishment and material recovery</li><li>Refining and reintegration into U.S. supply chains</li></ul></article>
<article class="service reveal"><figure><img src="/assets/img/mine-aerial.webp" alt="Terraced open-pit mine at sunrise" loading="lazy"></figure>
<p class="tag">02 · International</p><h3>Primary gold and silver production. A broader mineral endowment.</h3>
<p>Our international mining operations produce gold and silver as primary products, processed and refined within the APEX value chain. The same mineralized system hosts a broader suite of critical minerals, which we allocate to qualified U.S. refining and off-take partners. Our field record documents surface excavation and underground workings, and our technical review covers gold-focused exploration across the licensed area.</p>
<ul><li>Primary production processed within the APEX value chain</li><li>Geological, alteration and aeromagnetic review</li><li>Export license in place for U.S.-bound supply</li></ul></article>
</div></div></section>

<section class="section section-navy"><div class="wrap">
<div class="section-head reveal" style="margin-bottom:3rem"><span class="eyebrow">What we bring</span><h2 class="h2">The foundation, the access, the license.</h2></div>
<div class="pillars3 reveal">
<div><h3>01 · The foundation</h3><p>Established operations at home and abroad: electronics processing and refining in the United States, and mining internationally.</p></div>
<div><h3>02 · The access</h3><p>Our own operations: primary gold and silver production, with co-product tungsten, copper, uranium, cobalt, antimony, zinc, lead and iron.</p></div>
<div><h3>03 · The license</h3><p>An export license in hand, so material can move from our international operations to refineries in the United States.</p></div>
</div></div></section>

<section class="section section-muted" id="portfolio"><div class="wrap two-col two-col-top">
<div class="reveal"><span class="eyebrow" style="display:block;margin-bottom:.75rem">The partner we're seeking</span><h2 class="h2 h2-sm">A U.S. refinery or off-taker that needs a dependable, licensed source of critical minerals.</h2>
<p class="sub" style="margin-top:1.25rem">We bring the resource, the operations and the export license; the right partner brings the demand. Our critical-mineral supply is allocated exclusively to the United States.</p>
<div style="margin-top:2rem"><a class="btn btn-navy" href="{CONTACT}">Let's secure the supply chain together {I["arrow"]}</a></div></div>
<div class="minerals reveal"><figure><img src="/assets/img/minerals.webp" alt="Row of raw critical-mineral ore specimens" loading="lazy"></figure>
<h3>Our mineral portfolio</h3>
<div class="mrow"><span class="lbl">Primary production · Refined within the APEX value chain</span><ul class="chips">{"".join(f"<li>{m}</li>" for m in MINERALS_OWN)}</ul></div>
<div class="mrow"><span class="lbl">Co-product supply · Allocated to U.S. off-take partners</span><ul class="chips">{"".join(f"<li>{m}</li>" for m in MINERALS_PARTNER)}</ul></div>
</div></div></section>


<section class="section section-navy"><div class="wrap cta reveal">
<span class="eyebrow">Our commercial focus: the United States</span>
<h2 class="h2">Let's secure the supply chain together.</h2>
<p class="sub">Refiners, off-takers, industry and capital partners. We welcome the conversation.</p>
<a class="btn btn-gold" href="{CONTACT}">{EMAIL} {I["arrow"]}</a>
</div></section>'''

PAGES = [
    dict(path="/", title="Home", desc="APEX SCM: circular supply infrastructure for enterprise technology in the United States, and export-licensed critical-mineral supply from our international mining operations. Precision. Security. Scale.", body=HOME),
    dict(path="/about/", title="About", desc="APEX operates as infrastructure, not a recycler. Purpose, vision, core values and strategic objectives.", body=ABOUT),
    dict(path="/solutions/", title="Solutions", desc="Five pillars of enterprise circular supply infrastructure: security, value recovery, lifecycle integration, ESG performance and partnership, plus critical-mineral supply.", body=SOLUTIONS),
    dict(path="/services/", title="Services", desc="U.S. electronics collection, processing and refining. Primary gold and silver production at our international mining operations with co-product critical minerals, export licensed, allocated to U.S. off-take partners.", body=SERVICES, og_image="/assets/img/mine-aerial.webp"),
]

# Legacy Base44 routes (case-sensitive on GitHub Pages) -> new paths
REDIRECTS = {"/Home/": "/", "/About/": "/about/", "/Solutions/": "/solutions/", "/Services/": "/services/"}

def redirect(target):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{SITE}{target}"><script>location.replace("{target}")</script></head><body><a href="{target}">Continue to {target}</a></body></html>'

NOT_FOUND = page(title="Page not found", desc="The page you requested does not exist.", path="/404.html", body=f'''
<section class="section"><div class="wrap cta" style="padding-top:4rem"><span class="eyebrow">404</span><h2 class="h2">That page doesn't exist.</h2>
<p class="sub">The address may be out of date. Head back to the homepage or get in touch.</p>
<a class="btn btn-navy" href="/">Back to Home {I["arrow"]}</a></div></section>''')

def rebase(html):
    """Prefix root-relative URLs with BASE (no-op for the production build)."""
    return re.sub(r'((?:href|src|data)=")/(?!/)', r'\1' + BASE + '/', html) if BASE else html

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(SRC / "assets", OUT / "assets")
    shutil.copy(SRC / "styles.css", OUT / "styles.css")
    shutil.copy(SRC / "site.js", OUT / "site.js")
    for p in PAGES:
        d = OUT / p["path"].strip("/")
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(rebase(page(**p)), encoding="utf-8")
    for old, new in REDIRECTS.items():
        d = OUT / old.strip("/")
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(rebase(redirect(BASE + new)), encoding="utf-8")
    (OUT / "404.html").write_text(rebase(NOT_FOUND), encoding="utf-8")
    if not BASE:
        (OUT / "CNAME").write_text("apexscm.us\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p['path']}</loc></url>" for p in PAGES)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    (OUT / "manifest.json").write_text('{"name":"APEX SCM","short_name":"APEX SCM","start_url":"/","display":"browser","background_color":"#faf8f5","theme_color":"#2e395f","icons":[{"src":"/assets/img/apple-touch-icon.png","sizes":"180x180","type":"image/png"}]}')
    n = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"[{'preview '+BASE if BASE else 'production'}] built {len(PAGES)} pages + {len(REDIRECTS)} redirects -> {OUT} ({n} files)")

if __name__ == "__main__":
    build()
