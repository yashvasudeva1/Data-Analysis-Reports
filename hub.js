// hub.js — Shared Navigation & Utilities for Analysis Hub

// ── User identity config ────────────────────────────────────
const ADMIN_IDENTITY = {
  name:   'Yash Vasudeva',
  email:  'yash@analysis.hub',
  avatar: 'YV',
  role:   'Data Analyst',
  bio:    'Analyzing crime, economic, and climate datasets. Building interactive reports and KPIs.'
};
const GUEST_IDENTITY = {
  name:   'Guest',
  email:  'guest@analysis.hub',
  avatar: 'G',
  role:   'Guest Viewer',
  bio:    'Read-only view of published analysis reports and datasets.'
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

  // ── Logout: clear role on Logout link click ────────────────
  document.querySelectorAll('a[href="login.html"]').forEach(link => {
    link.addEventListener('click', () => localStorage.removeItem('hub-role'));
  });

  // ── RBAC & User Identity ───────────────────────────────────
  const role = localStorage.getItem('hub-role') || 'guest';
  document.body.classList.add('role-' + role);

  const identity = (role === 'admin') ? ADMIN_IDENTITY : GUEST_IDENTITY;
  const isGuest  = (role !== 'admin');

  // Topbar chip
  document.querySelectorAll('.user-name').forEach(el => el.textContent = identity.name);
  document.querySelectorAll('.user-email').forEach(el => el.textContent = identity.email);
  document.querySelectorAll('.user-avatar').forEach(el => el.textContent = identity.avatar);

  // Large avatar circle in settings (if present)
  const avatarCircle = document.querySelector('.user-avatar-circle');
  if (avatarCircle) avatarCircle.textContent = identity.avatar;

  if (isGuest) {
    document.body.classList.add('role-viewer');

    // Show guest alert banner on settings page
    const alertEl = document.getElementById('guest-settings-alert');
    if (alertEl) alertEl.style.display = 'flex';

    // Disable all setting fields
    document.querySelectorAll('.setting-field').forEach(el => {
      el.disabled = true;
      el.style.opacity = '0.55';
      el.style.cursor  = 'not-allowed';
      if (el.tagName === 'BUTTON') el.style.pointerEvents = 'none';
    });
  }

  // Populate settings form fields with correct identity values
  const nameInput  = document.getElementById('setting-name');
  const roleInput  = document.getElementById('setting-role');
  const bioInput   = document.getElementById('setting-bio');
  const emailInput = document.getElementById('setting-email');
  if (nameInput)  nameInput.value          = identity.name;
  if (roleInput)  roleInput.value          = identity.role;
  if (bioInput)   bioInput.value           = identity.bio;
  if (emailInput) emailInput.value         = identity.email;
});
