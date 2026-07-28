// hub.js - Shared Navigation & Utilities for Analysis Hub

// ── Default User Identity ────────────────────────────────────
const USER_IDENTITY = {
  name:   'Yash Vasudeva',
  email:  'yash@analysis.hub',
  avatar: 'YV',
  role:   'Data Analyst',
  bio:    'Analyzing crime, economic, and climate datasets. Building interactive reports and KPIs.'
};

document.addEventListener('DOMContentLoaded', () => {

  // ── Active nav item ───────────────────────────────────────
  const file = window.location.pathname.split('/').pop() || 'index.html';
  const navMap = {
    'index.html':    'nav-dashboard',
    '':              'nav-dashboard',
    'reports.html':  'nav-reports',
    'datasets.html': 'nav-datasets',
    'analytics.html':'nav-analytics',
    'settings.html': 'nav-settings',
    'help.html':     'nav-help',
  };
  const activeEl = document.getElementById(navMap[file]);
  if (activeEl) activeEl.classList.add('active');

  // ── Global search ──────────────────────────────────────────
  const searchEl = document.getElementById('search-input');
  if (searchEl) {
    const handleSearch = (query) => {
      const q = query.trim().toLowerCase();
      document.querySelectorAll('[data-search]').forEach(el => {
        const text = (el.dataset.search || el.textContent).toLowerCase();
        el.style.display = (q === '' || text.includes(q)) ? '' : 'none';
      });
      document.querySelectorAll('.report-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = (q === '' || text.includes(q)) ? '' : 'none';
      });
      document.querySelectorAll('.report-row').forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = (q === '' || text.includes(q)) ? '' : 'none';
      });
      document.querySelectorAll('.cat-row').forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = (q === '' || text.includes(q)) ? '' : 'none';
      });
    };
    searchEl.addEventListener('input', e => handleSearch(e.target.value));
    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
        e.preventDefault(); searchEl.focus(); searchEl.select();
      }
      if (e.key === 'Escape' && document.activeElement === searchEl) {
        searchEl.value = ''; handleSearch(''); searchEl.blur();
      }
    });
  }

  // ── Sync topbar search with local filter bar ──────────────
  const reportSearch = document.getElementById('report-search');
  if (searchEl && reportSearch) {
    searchEl.addEventListener('input', e => {
      reportSearch.value = e.target.value;
      reportSearch.dispatchEvent(new Event('input'));
    });
    reportSearch.addEventListener('input', e => { searchEl.value = e.target.value; });
  }

  // ── Filter tabs ────────────────────────────────────────────
  document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const group = tab.closest('.filter-tabs');
      if (group) group.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.filter;
      const grid   = tab.dataset.target ? document.getElementById(tab.dataset.target) : null;
      if (!grid) return;
      grid.querySelectorAll('[data-status]').forEach(card => {
        card.style.display = (filter === 'all' || card.dataset.status === filter) ? '' : 'none';
      });
    });
  });

  // ── Settings tabs ──────────────────────────────────────────
  document.querySelectorAll('.settings-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.settings-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.settings-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const panel = document.getElementById(tab.dataset.panel);
      if (panel) panel.classList.add('active');
    });
  });

  // ── FAQ accordion ──────────────────────────────────────────
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-question');
    if (q) q.addEventListener('click', () => item.classList.toggle('open'));
  });

  // ── User Identity Population ───────────────────────────────
  document.querySelectorAll('.user-name').forEach(el => el.textContent = USER_IDENTITY.name);
  document.querySelectorAll('.user-email').forEach(el => el.textContent = USER_IDENTITY.email);
  document.querySelectorAll('.user-avatar').forEach(el => el.textContent = USER_IDENTITY.avatar);

  const avatarCircle = document.querySelector('.user-avatar-circle');
  if (avatarCircle) avatarCircle.textContent = USER_IDENTITY.avatar;

  // Populate settings form fields
  const nameInput  = document.getElementById('setting-name');
  const roleInput  = document.getElementById('setting-role');
  const bioInput   = document.getElementById('setting-bio');
  const emailInput = document.getElementById('setting-email');
  if (nameInput)  nameInput.value          = USER_IDENTITY.name;
  if (roleInput)  roleInput.value          = USER_IDENTITY.role;
  if (bioInput)   bioInput.value           = USER_IDENTITY.bio;
  if (emailInput) emailInput.value         = USER_IDENTITY.email;
});
