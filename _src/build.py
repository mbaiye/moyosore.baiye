#!/usr/bin/env python3
"""Generate the static portfolio page. Standard library only.

    python3 _src/build.py

GitHub Pages serves the repository as-is, so the generated index.html and
sitemap.xml are committed. Jekyll skips folders that start with "_", so this
folder is not published.

Text lives in _src/content.json. Facts (dates, links, certifications, skills)
live in this file.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = Path(__file__).resolve().parent / "content.json"

# Change this one line when the site moves to a custom domain.
SITE_URL = "https://mbaiye.github.io/moyosore.baiye/"

CV = "assets/Moyosore_Baiye_DevSecOps_DPO_CV.pdf"
PORTRAIT = "assets/images/moyosore-baiye.jpg"
EMAIL = "moyosorebaiye@gmail.com"
PHONE = "+234 706 437 9501"
GITHUB = "https://github.com/mbaiye"
LINKEDIN = "https://www.linkedin.com/in/moyobaiye"

# (year, month) with month None when only the year is known. end None = present.
EXPERIENCE = [
    {"org": "Octosoft Technologies Limited", "url": "https://www.octosoft.ai", "start": (2022, 7), "end": None},
    {"org": "Lagos State Coroner System", "url": None, "start": (2020, 1), "end": (2022, 6)},
    {"org": "TTC Mobile World USA", "url": None, "start": (2020, 10), "end": (2021, 3)},
    {"org": "Venture Garden Group", "url": None, "start": (2020, 1), "end": (2020, 6)},
]

PLATFORMS = [
    {"url": "https://www.veribuy.shop/", "host": "veribuy.shop",
     "stack": ["Next.js", "React", "Node.js", "FastAPI", "PostgreSQL", "AWS", "Stripe"]},
    {"url": "https://cleancoatcontractorsltd.co.uk/", "host": "cleancoatcontractorsltd.co.uk",
     "stack": ["Next.js", "React", "Node.js", "CI/CD"]},
    {"url": "https://havilah.ng/", "host": "havilah.ng",
     "stack": ["JavaScript", "Cloud hosting"]},
    {"url": None, "host": None,
     "stack": ["AWS", "Terraform", "Docker", "GitHub Actions", "CloudWatch"]},
]

# Official names stay in English so they match what a verifier will find.
CERTS = [
    ("CDPO", "Certified Data Protection Officer", "", None),
    ("KCNA", "Kubernetes and Cloud Native Associate", "The Linux Foundation", None),
    ("SAA-C02", "AWS Certified Solutions Architect – Associate", "Amazon Web Services", (2021, 12)),
    ("CLF-C01", "AWS Certified Cloud Practitioner", "Amazon Web Services", (2022, 8)),
    ("AZ-700", "Azure Network Engineer Associate", "Microsoft", (2022, 9)),
    ("AZ-204", "Azure Developer Associate", "Microsoft", (2021, 9)),
    ("AZ-104", "Azure Administrator Associate", "Microsoft", (2021, 2)),
    ("DP-900", "Azure Data Fundamentals", "Microsoft", (2021, 5)),
    ("Google", "IT Automation Professional Certificate", "Google / Coursera", (2022, 4)),
    ("Google", "IT Support Professional Certificate", "Google / Coursera", (2021, 10)),
    ("Google", "Africa Developer Training: Mobile Web", "Google Developers", (2021, 2)),
]

EDUCATION = [
    {"degree": "MSc Information Technology", "school": "University of Lagos", "start": (2022, 1), "end": (2024, 1), "distinction": False},
    {"degree": "BTech Computer Science", "school": "Federal University of Technology, Akure", "start": (2014, 9), "end": (2019, 12), "distinction": False},
    {"degree": "Advanced Diploma in Software Engineering", "school": "Aptech Computer Education", "start": (2010, None), "end": (2012, None), "distinction": True},
]

SKILLS = [
    ["DPIA", "HIPAA", "GDPR", "NDPR", "Threat modeling", "IAM hardening", "Vault", "KMS", "Trivy", "Snyk", "OWASP Top 10"],
    ["AWS", "Microsoft Azure", "Terraform", "CloudFormation", "Linux", "Multi-AZ architecture"],
    ["Docker", "Kubernetes", "Helm", "Container hardening", "Microservices"],
    ["GitHub Actions", "Jenkins", "Ansible", "Blue/green deployments", "Canary deployments"],
    ["CloudWatch", "GuardDuty", "Prometheus", "Grafana"],
    ["Python", "Bash", "JavaScript", "C#", "Next.js", "React", "Node.js", "FastAPI", "PostgreSQL", "MySQL"],
]

SECTIONS = ["focus", "experience", "platforms", "teaching", "credentials", "contact"]


def svg(body: str) -> str:
    return ('<svg class="icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


ICONS = {
    "theme": svg('<path d="M20 14.500A8.500 8.500 0 0 1 9.500 4 8.500 8.500 0 1 0 20 14.500z"/>'),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "download": svg('<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>'),
    "arrow": svg('<path d="M7 17 17 7M9 7h8v8"/>'),
    "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "phone": svg('<path d="M21 16.500v3a1.500 1.500 0 0 1-1.600 1.500A17 17 0 0 1 3 4.600 1.500 1.500 0 0 1 4.500 3h3a1 1 0 0 1 1 .8l.7 3.200a1 1 0 0 1-.3 1L7.300 9.600a14 14 0 0 0 7.100 7.100l1.600-1.600a1 1 0 0 1 1-.3l3.200.7a1 1 0 0 1 .8 1z"/>'),
    "github": svg('<path d="M9 19c-4 1.300-4-2-6-2.500m12 5v-3.400a3 3 0 0 0-.8-2.300c2.700-.3 5.500-1.300 5.500-6a4.700 4.700 0 0 0-1.300-3.200 4.300 4.300 0 0 0-.1-3.200s-1-.3-3.400 1.300a11.500 11.500 0 0 0-6 0C6.500 2.100 5.500 2.400 5.500 2.400a4.300 4.300 0 0 0-.1 3.200 4.700 4.700 0 0 0-1.300 3.200c0 4.700 2.800 5.700 5.500 6a3 3 0 0 0-.8 2.300V21"/>'),
    "linkedin": svg('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 10.500V17M8 7.500v.01M12 17v-6.500M12 13.500c0-1.700 1.300-3 3-3s2.500 1.200 2.500 3V17"/>'),
}

e = html.escape


def fmt_date(value, months) -> str:
    year, month = value
    return f"{months[month - 1]} {year}" if month else str(year)


def date_range(start, end, t) -> str:
    months = t["months"]
    last = fmt_date(end, months) if end else t["experience"]["present"]
    return f"{fmt_date(start, months)} – {last}"


def section_head(tag: str, title: str, index: int) -> str:
    return (f'<header class="section-head"><p class="kicker"><span>{index:02d}</span> {e(tag)}</p>'
            f'<h2>{e(title)}</h2></header>')


def render_header(t: dict) -> str:
    links = "".join(f'<li><a href="#{s}">{e(t["nav"][s])}</a></li>' for s in SECTIONS)
    return f"""<a class="skip" href="#main">{e(t['ui']['skip'])}</a>
  <header class="topbar">
    <div class="wrap topbar-inner">
      <a class="brand" href="#top">Moyosore Baiye</a>
      <nav class="nav" id="nav" aria-label="{e(t['ui']['menu'], quote=True)}"><ul>{links}</ul></nav>
      <div class="tools">
        <button class="icon-btn" type="button" data-theme-toggle aria-label="{e(t['ui']['theme'], quote=True)}" title="{e(t['ui']['theme'], quote=True)}">{ICONS['theme']}</button>
        <a class="btn-cv" href="{CV}" download aria-label="{e(t['ui']['cv'], quote=True)}">{ICONS['download']}<span>{e(t['ui']['cv_short'])}</span></a>
        <button class="icon-btn menu-btn" type="button" data-menu-toggle aria-expanded="false" aria-controls="nav" aria-label="{e(t['ui']['menu'], quote=True)}">{ICONS['menu']}</button>
      </div>
    </div>
  </header>"""


def render_hero(t: dict) -> str:
    roles = "".join(f"<li>{e(r)}</li>" for r in t["hero"]["roles"])
    f = t["facts"]
    return f"""<section class="hero" id="top">
      <div class="wrap hero-grid">
        <div class="hero-copy">
          <ul class="roles">{roles}</ul>
          <h1>{e(t['hero']['title'])}</h1>
          <p class="lead">{e(t['hero']['lead'])}</p>
          <div class="actions">
            <a class="btn btn-primary" href="{CV}" download>{ICONS['download']}<span>{e(t['ui']['cv'])}</span></a>
            <a class="btn btn-ghost" href="{LINKEDIN}" rel="noopener">{ICONS['linkedin']}<span>{e(t['contact']['linkedin'])}</span></a>
            <a class="btn btn-ghost" href="{GITHUB}" rel="noopener">{ICONS['github']}<span>{e(t['contact']['github'])}</span></a>
          </div>
        </div>
        <div class="hero-side">
          <figure class="portrait"><img src="{PORTRAIT}" alt="Moyosore Baiye" width="700" height="900" fetchpriority="high"></figure>
          <dl class="facts">
            <div><dt>{e(f['location'])}</dt><dd>{e(f['location_value'])}</dd></div>
            <div><dt>{e(f['time'])}</dt><dd><span data-local-time></span>WAT (UTC+1)</dd></div>
            <div><dt>{e(f['work'])}</dt><dd>{e(f['work_value'])}</dd></div>
            <div><dt>{e(f['status'])}</dt><dd class="status"><i aria-hidden="true"></i>{e(f['status_value'])}</dd></div>
          </dl>
        </div>
      </div>
    </section>"""


def render_metrics(t: dict) -> str:
    items = "".join(f'<li><strong>{e(m["value"])}</strong><span>{e(m["label"])}</span></li>' for m in t["metrics"])
    return f'<section class="metrics" aria-label="{e(t["nav"]["experience"], quote=True)}"><ul class="wrap">{items}</ul></section>'


def render_focus(t: dict) -> str:
    items = "".join(
        f'<li><span class="num">{chr(65 + i)}</span><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></li>'
        for i, x in enumerate(t["focus"]["items"]))
    return f"""<section class="section" id="focus"><div class="wrap">
      {section_head(t['focus']['tag'], t['focus']['title'], 1)}
      <ul class="focus-grid">{items}</ul>
    </div></section>"""


def render_experience(t: dict) -> str:
    rows = []
    for fact, item in zip(EXPERIENCE, t["experience"]["items"]):
        bullets = "".join(
            "<li>" + (f'<strong>{e(b["label"])}:</strong> ' if b["label"] else "") + f'{e(b["text"])}</li>'
            for b in item["bullets"])
        org = (f'<a href="{fact["url"]}" rel="noopener">{e(fact["org"])}</a>' if fact["url"] else e(fact["org"]))
        rows.append(f"""<li class="job">
          <div class="job-meta"><p class="when">{e(date_range(fact['start'], fact['end'], t))}</p><p>{e(item['place'])}</p></div>
          <div class="job-body">
            <h3>{e(item['role'])}</h3>
            <p class="org">{org} <span>· {e(item['sector'])}</span></p>
            <ul>{bullets}</ul>
          </div>
        </li>""")
    return f"""<section class="section section-alt" id="experience"><div class="wrap">
      {section_head(t['experience']['tag'], t['experience']['title'], 2)}
      <ol class="jobs">{''.join(rows)}</ol>
    </div></section>"""


def render_platforms(t: dict) -> str:
    cards = []
    for fact, item in zip(PLATFORMS, t["platforms"]["items"]):
        stack = "".join(f"<li>{e(s)}</li>" for s in fact["stack"])
        if fact["url"]:
            link = (f'<a class="site-link" href="{fact["url"]}" rel="noopener" '
                    f'aria-label="{e(t["ui"]["visit"], quote=True)}: {e(item["title"], quote=True)}">'
                    f'<span>{e(fact["host"])}</span>{ICONS["arrow"]}</a>')
        else:
            link = f'<span class="site-link muted">{e(t["platforms"]["confidential"])}</span>'
        cards.append(f"""<li class="platform">
          <p class="platform-role">{e(item['role'])}</p>
          <h3>{e(item['title'])}</h3>
          <p>{e(item['text'])}</p>
          <ul class="chips">{stack}</ul>
          {link}
        </li>""")
    return f"""<section class="section" id="platforms"><div class="wrap">
      {section_head(t['platforms']['tag'], t['platforms']['title'], 3)}
      <ul class="platform-grid">{''.join(cards)}</ul>
    </div></section>"""


def render_teaching(t: dict) -> str:
    items = "".join(f'<li><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></li>' for x in t["teaching"]["items"])
    return f"""<section class="section section-alt" id="teaching"><div class="wrap teaching">
      <div>
        {section_head(t['teaching']['tag'], t['teaching']['title'], 4)}
        <p class="section-lead">{e(t['teaching']['lead'])}</p>
      </div>
      <ul class="teaching-list">{items}</ul>
    </div></section>"""


def render_credentials(t: dict) -> str:
    c = t["credentials"]
    certs = "".join(
        f'<tr><td class="code">{e(code)}</td><td><b>{e(name)}</b>'
        + (f'<small>{e(issuer)}</small>' if issuer else "")
        + f'</td><td class="when">{e(fmt_date(date, t["months"])) if date else ""}</td></tr>'
        for code, name, issuer, date in CERTS)
    edu = "".join(
        f'<li><h4>{e(x["degree"])}</h4><p>{e(x["school"])}</p>'
        f'<p class="when">{e(date_range(x["start"], x["end"], t))}'
        + (f' <span class="badge">{e(c["distinction"])}</span>' if x["distinction"] else "")
        + "</p></li>"
        for x in EDUCATION)
    groups = "".join(
        f'<div><dt>{e(title)}</dt><dd><ul class="chips">{"".join(f"<li>{e(s)}</li>" for s in skills)}</ul></dd></div>'
        for title, skills in zip(t["skills"]["groups"], SKILLS))
    return f"""<section class="section" id="credentials"><div class="wrap">
      {section_head(c['tag'], c['title'], 5)}
      <div class="cred-grid">
        <div>
          <h3 class="sub">{e(c['certs_title'])}</h3>
          <table class="certs"><tbody>{certs}</tbody></table>
        </div>
        <div>
          <h3 class="sub">{e(c['edu_title'])}</h3>
          <ul class="edu">{edu}</ul>
        </div>
      </div>
      <h3 class="sub skills-title">{e(t['skills']['title'])}</h3>
      <dl class="skills">{groups}</dl>
    </div></section>"""


def render_contact(t: dict) -> str:
    c = t["contact"]
    phone_href = "tel:" + PHONE.replace(" ", "")
    return f"""<section class="contact" id="contact"><div class="wrap">
      <p class="kicker"><span>06</span> {e(c['tag'])}</p>
      <h2>{e(c['title'])}</h2>
      <p class="lead">{e(c['text'])}</p>
      <div class="actions">
        <a class="btn btn-primary" href="mailto:{EMAIL}">{ICONS['mail']}<span>{EMAIL}</span></a>
        <a class="btn btn-ghost" href="{LINKEDIN}" rel="noopener">{ICONS['linkedin']}<span>{e(c['linkedin'])}</span></a>
        <a class="btn btn-ghost" href="{GITHUB}" rel="noopener">{ICONS['github']}<span>{e(c['github'])}</span></a>
        <a class="btn btn-ghost" href="{phone_href}">{ICONS['phone']}<span>{PHONE}</span></a>
      </div>
    </div></section>"""


def json_ld(t: dict) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Moyosore Baiye",
        "url": SITE_URL,
        "image": SITE_URL + PORTRAIT,
        "email": f"mailto:{EMAIL}",
        "jobTitle": t["hero"]["roles"][0],
        "description": t["meta"]["description"],
        "worksFor": {"@type": "Organization", "name": "Octosoft Technologies Limited", "url": "https://www.octosoft.ai"},
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": x["school"]} for x in EDUCATION[:2]],
        "address": {"@type": "PostalAddress", "addressLocality": "Lagos", "addressCountry": "NG"},
        "sameAs": [LINKEDIN, GITHUB],
    }
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_page(t: dict) -> str:
    title = e(t["meta"]["title"], quote=True)
    description = e(t["meta"]["description"], quote=True)
    return f"""<!DOCTYPE html>
<!-- Generated by _src/build.py. Edit _src/content.json, not this file. -->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{SITE_URL}">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{SITE_URL}">
  <meta property="og:image" content="{SITE_URL}{PORTRAIT}">
  <meta name="twitter:card" content="summary">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicon-32x32.png">
  <link rel="apple-touch-icon" href="assets/images/android-chrome-192x192.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/style.css">
  <script>try{{var s=localStorage.getItem('theme');if(s)document.documentElement.dataset.theme=s}}catch(e){{}}</script>
  <script type="application/ld+json">{json_ld(t)}</script>
</head>
<body>
  {render_header(t)}
  <main id="main">
    {render_hero(t)}
    {render_metrics(t)}
    {render_focus(t)}
    {render_experience(t)}
    {render_platforms(t)}
    {render_teaching(t)}
    {render_credentials(t)}
    {render_contact(t)}
  </main>
  <footer class="footer"><div class="wrap">
    <p>© <span data-year>2026</span> Moyosore Baiye. {e(t['ui']['footer'])}</p>
  </div></footer>
  <script src="assets/js/script.js" defer></script>
</body>
</html>
"""


def validate(t: dict) -> None:
    """Stop the build if text and facts have drifted apart."""
    checks = [
        (len(t["experience"]["items"]), len(EXPERIENCE), "experience"),
        (len(t["platforms"]["items"]), len(PLATFORMS), "platforms"),
        (len(t["skills"]["groups"]), len(SKILLS), "skills"),
        (len(t["months"]), 12, "months"),
    ]
    errors = [f"{name}: {a} text items but {b} facts" for a, b, name in checks if a != b]
    if errors:
        sys.exit("Build failed:\n  " + "\n  ".join(errors))


def main() -> None:
    t = json.loads(CONTENT.read_text("utf-8"))
    validate(t)
    (ROOT / "index.html").write_text(render_page(t), "utf-8")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE_URL}</loc></url>\n</urlset>\n", "utf-8")
    print("wrote index.html and sitemap.xml")


if __name__ == "__main__":
    main()
