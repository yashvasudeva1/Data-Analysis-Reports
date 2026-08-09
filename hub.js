// hub.js - Shared Navigation, Mobile Drawer & Utilities for Analysis Hub

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

  // ── Mobile Menu Toggle & Navigation Drawer ────────────────
  const topbar = document.querySelector('.topbar');
  if (topbar && !document.querySelector('.mobile-menu-btn')) {
    const menuBtn = document.createElement('button');
    menuBtn.className = 'mobile-menu-btn';
    menuBtn.setAttribute('aria-label', 'Open Menu');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.setAttribute('aria-controls', 'mobile-nav-drawer');
    menuBtn.innerHTML = '☰';
    topbar.insertBefore(menuBtn, topbar.firstChild);

    const backdrop = document.createElement('div');
    backdrop.className = 'mobile-nav-backdrop';
    backdrop.innerHTML = `
      <div class="mobile-nav-drawer" id="mobile-nav-drawer" role="dialog" aria-modal="true" aria-label="Navigation menu">
        <div class="mobile-drawer-header">
          <div>
            <div class="logo-name" style="font-size:16px">Analysis Hub</div>
            <div class="logo-sub">Data Reports</div>
          </div>
          <button class="mobile-drawer-close">✕</button>
        </div>
        <div class="nav-section">
          <p class="nav-eyebrow">Menu</p>
          <a href="index.html" class="nav-item ${file === 'index.html' || file === '' ? 'active' : ''}"><span class="nav-label">Dashboard</span></a>
          <a href="reports.html" class="nav-item ${file === 'reports.html' ? 'active' : ''}"><span class="nav-label">Reports</span><span class="nav-badge">3</span></a>
          <a href="datasets.html" class="nav-item ${file === 'datasets.html' ? 'active' : ''}"><span class="nav-label">Datasets</span></a>
          <a href="analytics.html" class="nav-item ${file === 'analytics.html' ? 'active' : ''}"><span class="nav-label">Analytics</span></a>
        </div>
        <div class="sidebar-divider"></div>
        <div class="nav-section">
          <p class="nav-eyebrow">General</p>
          <a href="settings.html" class="nav-item ${file === 'settings.html' ? 'active' : ''}"><span class="nav-label">Settings</span></a>
          <a href="help.html" class="nav-item ${file === 'help.html' ? 'active' : ''}"><span class="nav-label">Help</span></a>
        </div>
      </div>
    `;
    document.body.appendChild(backdrop);

    const closeBtn = backdrop.querySelector('.mobile-drawer-close');
    closeBtn.setAttribute('aria-label', 'Close menu');
    const toggleMenu = (open) => {
      backdrop.classList.toggle('open', open);
      document.body.classList.toggle('mobile-menu-open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      if (open) closeBtn.focus();
      else menuBtn.focus();
    };

    menuBtn.addEventListener('click', () => toggleMenu(true));
    closeBtn.addEventListener('click', () => toggleMenu(false));
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) toggleMenu(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && backdrop.classList.contains('open')) toggleMenu(false);
    });
  }

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
