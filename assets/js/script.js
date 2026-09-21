'use strict';

// Mobile Navigation Toggle
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');

if (mobileToggle && navLinks) {
  mobileToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
  });

  // Close nav on link click
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('active');
    });
  });
}

// Active Nav state on scroll
const sections = document.querySelectorAll('section[id]');
function handleScroll() {
  const scrollY = window.pageYOffset;

  sections.forEach(current => {
    const sectionHeight = current.offsetHeight;
    const sectionTop = current.offsetTop - 100;
    const sectionId = current.getAttribute('id');
    const navLink = document.querySelector(`.nav-links a[href*='${sectionId}']`);

    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
      if (navLink) navLink.classList.add('active');
    } else {
      if (navLink) navLink.classList.remove('active');
    }
  });
}

window.addEventListener('scroll', handleScroll);

// Smooth console greeting for engineers inspecting the source
console.log(
  '%c🔒 Moyosore Baiye — Senior DevSecOps Engineer & Data Protection Officer\n%cLooking for enterprise infrastructure security, HIPAA/NDPR compliance, or Kubernetes automation? Let’s connect: moyosorebaiye@hotmail.com',
  'color: #38BDF8; font-size: 14px; font-weight: bold;',
  'color: #94A3B8; font-size: 12px;'
);
