# Moyosore Baiye

Portfolio of Moyosore Baiye: Senior DevSecOps Engineer and Team Lead, Certified Data Protection Officer and DevOps educator.

Live site: https://mbaiye.github.io/moyosore.baiye/

## Editing the site

The pages are static and GitHub Pages serves this branch as-is, so generated files are committed.

| To change | Edit |
| --- | --- |
| Text | `_src/content.json` |
| Dates, links, certifications, skills | `_src/build.py` |
| Styling and behaviour | `assets/css/style.css`, `assets/js/script.js` |

Then regenerate the pages (Python 3, no dependencies) and commit the result:

```bash
python3 _src/build.py
```

If the site moves to a custom domain, update `SITE_URL` in `_src/build.py`.

Do not edit `index.html` directly: the next build overwrites it.
