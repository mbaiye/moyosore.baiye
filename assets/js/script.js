'use strict';

(function () {
  const root = document.documentElement;

  // Storage can throw in private windows, so every access goes through these.
  const store = {
    get(key) { try { return localStorage.getItem(key); } catch (err) { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch (err) { /* not persisted */ } },
  };

  // Theme: follows the system until the visitor chooses.
  const themeButton = document.querySelector('[data-theme-toggle]');
  if (themeButton) {
    themeButton.addEventListener('click', () => {
      const dark = root.dataset.theme
        ? root.dataset.theme === 'dark'
        : matchMedia('(prefers-color-scheme: dark)').matches;
      const next = dark ? 'light' : 'dark';
      root.dataset.theme = next;
      store.set('theme', next);
    });
  }

  // Mobile menu
  const menuButton = document.querySelector('[data-menu-toggle]');
  const nav = document.getElementById('nav');
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    menuButton.setAttribute('aria-expanded', String(open));
  };
  if (menuButton && nav) {
    menuButton.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenu(false);
    });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menuButton && nav) setMenu(false);
  });

  // Lagos time.
  const timeEl = document.querySelector('[data-local-time]');
  if (timeEl) {
    const format = new Intl.DateTimeFormat('en', {
      timeZone: 'Africa/Lagos', hour: '2-digit', minute: '2-digit',
    });
    const tick = () => { timeEl.textContent = format.format(new Date()) + ' '; };
    tick();
    setInterval(tick, 30000);
  }

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  // Highlight the current section in the nav.
  const navLinks = new Map(
    [...document.querySelectorAll('.nav a')].map((a) => [a.getAttribute('href').slice(1), a])
  );
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((a) => a.removeAttribute('aria-current'));
        const active = navLinks.get(entry.target.id);
        if (active) active.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    navLinks.forEach((_, id) => {
      const section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }
})();
