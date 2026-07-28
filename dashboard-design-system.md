# Analysis Hub — Dashboard Design System

Reference: the "Donezo" project-management dashboard screenshot.
Goal app: instead of managing projects, this dashboard manages **data analysis reports** you upload — starting from something like [`cpi_inflation_analysis`](https://github.com/yashvasudeva1/cpi_inflation_analysis) (a Flask + Chart.js CPI inflation dashboard), except here each report is one *entry* in a bigger hub, not the whole app.

Use this file as the spec sheet any time you (or an AI assistant) build a new screen for this product — it fixes the visual language so every screen looks like it belongs to the same app.

---

## 1. Design tokens

### Color palette

| Token | Hex | Use |
|---|---|---|
| `--bg` | `#F4F6F5` | Page background (very light, faint green-gray tint — not pure white) |
| `--surface` | `#FFFFFF` | Cards, sidebar, topbar |
| `--green-900` | `#0E3B2E` | Deepest green — hero stat card, sidebar active pill background |
| `--green-700` | `#155C46` | Primary buttons, active nav icon bg, time-tracker card |
| `--green-500` | `#2E9370` | Mid accent — chart bars, progress ring "completed" segment |
| `--green-300` | `#8FD6B4` | Light accent bar in charts |
| `--mint-100` | `#E3F5EA` | Badge/pill backgrounds, hover states |
| `--text-900` | `#14181B` | Headings, primary numbers |
| `--text-500` | `#6B7280` | Body/secondary text |
| `--text-400` | `#9AA1A9` | Placeholder, timestamps, inactive nav |
| `--border` | `#ECEEED` | Card borders, dividers |
| `--amber-bg` / `--amber-text` | `#FFF4D6` / `#B7791F` | "In Progress" badge |
| `--gray-bg` / `--gray-text` | `#EFF1F0` / `#6B7280` | "Pending" badge |
| `--green-bg` / `--green-text` | `#E1F5EA` / `#1F8A5F` | "Completed" badge |

Treat green as the *only* saturated brand color. Everything else is neutral. Badges are the only place other hues (amber) show up, and only at low saturation.

### Typography

- Font family: a rounded-geometric sans — **Plus Jakarta Sans** or **Inter** both match well. Load 400/500/600/700/800.
- Big stat numbers: 700–800 weight, `text-3xl`–`text-4xl`, tabular-nums, `--text-900`.
- Card titles: 600 weight, `text-base`, `--text-900`.
- Body/labels: 400–500 weight, `text-sm`, `--text-500`.
- Section eyebrows (e.g. "MENU", "GENERAL"): 600 weight, `text-xs`, letter-spacing wide, `--text-400`.

### Spacing, radius, shadow

- Page gutter: 24–32px. Card gap: 20–24px.
- Radius: outer app shell `28px`, cards `20–24px`, small icon buttons/avatars fully round, buttons `999px` (pill) except primary action rectangles which use `12–14px`.
- Shadow: very soft, ambient only — `0 1px 2px rgba(16,24,21,0.04), 0 12px 24px rgba(16,24,21,0.05)`. No hard drop shadows.
- Card padding: `20–24px`.

---

## 2. Layout shell

```
┌─ App shell (rounded 28px, sits on --bg, slight outer margin) ───────────┐
│ ┌────────────┐ ┌────────────────────────────────────────────────────┐ │
│ │            │ │ Topbar: search (⌘F) ... mail  bell  avatar+name   │ │
│ │  Sidebar   │ ├────────────────────────────────────────────────────┤ │
│ │  240px     │ │ Page header: H1 + subtitle .......... [primary btn]│ │
│ │            │ │                                        [outline btn]│
│ │  logo      │ ├────────────────────────────────────────────────────┤ │
│ │  MENU      │ │  4-up stat card row (equal width)                  │ │
│ │  items     │ ├───────────────┬───────────────┬────────────────────┤ │
│ │  GENERAL   │ │ Chart card    │ List/CTA card │ List card (+New)   │ │
│ │  items     │ │ (wide)        │ (narrow)      │ (narrow)           │ │
│ │            │ ├───────────────┴───────┬───────┴────────────────────┤ │
│ │  promo     │ │ List card (wide)      │ Donut card │ Dark card    │ │
│ │  card      │ │                        │            │ (timer)      │ │
│ └────────────┘ └────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

Grid: 12-column, cards snap to 3/4/5-column widths depending on content. Row heights are content-driven, not fixed.

---

## 3. Components

### Sidebar
- Logo + wordmark top-left, "MENU" eyebrow, nav items with icon + label.
- Active item: soft mint pill background, dark green icon chip, thin green bar on the far-left edge of the row.
- Inactive items: gray icon + gray text, no background.
- A count badge (small dark green pill, white text) can sit at the end of a nav row, e.g. an unread/open count.
- "GENERAL" section below with a visual gap (Settings/Help/Logout).
- Bottom of sidebar: a dark rounded promo card (illustration + short line + pill CTA button) — pinned, not part of scroll.

### Topbar
- Left: search input, pill-rounded, light gray fill, magnifier icon, keyboard-shortcut chip (`⌘F`) right-aligned inside the field.
- Right: two circular icon buttons (mail, notifications — notification has a small red dot), then a user chip: circular avatar + name (600 weight) + email (muted, smaller) stacked.

### Page header
- H1 (large, bold) + one-line muted subtitle beneath.
- Right-aligned actions: one solid dark-green pill button with a `+` icon (primary action, e.g. "Add Project"), one outline pill button (secondary action, e.g. "Import Data").

### Stat card (4-up row)
- White (or, for the *first/hero* card only, a dark green diagonal gradient) rounded card.
- Top row: label (left) + small circular icon button with a diagonal arrow (top-right).
- Big number, bold, directly under the label.
- Small pill underneath: icon + "Increased from last month" / status text, in a muted or on-brand tone depending on card background.

### Analytics bar-chart card
- Title top-left ("Project Analytics").
- 7 vertical bars (S M T W T F S), rounded pill-shaped bars of varying height; the tallest/active bar is solid dark green with a small percentage callout bubble above it; the rest alternate solid mid-green, light-green, and a diagonal-hatched pattern for "no data"/empty days.
- Day-letter labels under each bar, small muted text.

### Reminder / CTA card
- Title + one bold highlighted line (e.g. an event name) + a metadata line (time range).
- One solid pill button with an icon, full-width or near-full-width, dark green — this is the card's single call to action.

### List card with "+ New"
- Title + circular "+ New" pill button top-right.
- Rows: small colorful rounded-square icon (unique flat color per row, not the brand green — used only for visual distinction between item *types*), title (600 weight), muted due-date subtext.
- No dividers between rows; spacing does the separating.

### Team/collaboration list
- Title + "+ Add Member" outline pill button top-right.
- Rows: circular avatar photo, name (600 weight), muted "Working on **bold item name**" line, and a status badge pill right-aligned (Completed / In Progress / Pending — colors per the badge table above).

### Progress donut card
- Title top-left.
- Large rounded-cap donut arc (thick stroke, not thin), dark green primary segment, lighter green secondary, hatched pattern for the empty/remaining segment.
- Big bold percentage centered in the donut, small muted caption under it (e.g. "Project Ended").
- Legend row below: colored dot + label for each segment (Completed / In Progress / Pending).

### Time-tracker / live-status card
- Full dark-green card (not white) with a faint decorative topographic/line pattern in the background at low opacity.
- Title (light text), big monospace/tabular timer number, two circular control buttons (pause = white circle, stop = red circle) bottom-left.

### Badges
Small pill, 500-weight text, no border: green/completed, amber/in-progress, gray/pending. Always paired with a plain-language label, never just a color.

---

## 4. Icon set

Use a single consistent icon library (e.g. `lucide-react`) at 18–20px, 1.5–1.75 stroke weight:
`layout-dashboard`, `check-square`, `calendar`, `bar-chart-2`, `users`, `settings`, `help-circle`, `log-out`, `search`, `mail`, `bell`, `plus`, `arrow-up-right`, `video`, `pause`, `square` (stop).

---

## 5. Application blueprint — "Analysis Hub"

Mapping the same layout to your actual use case: **a place to upload and browse multiple data-analysis projects/reports** (CPI inflation being the first one).

### Sidebar nav
- Dashboard
- Reports *(badge = count of reports needing review)*
- Datasets
- Analytics *(cross-report insights)*
- Team
- —
- Settings, Help, Logout

### Topbar
- Search across report titles/tags (`⌘F`)
- Notifications (e.g. "new forecast ready", "upload failed")
- User chip

### Page header
- H1: **Reports** or **Dashboard**
- Subtitle: "Upload, track, and compare your data analysis reports."
- Primary button: **+ New Report** (single upload/create flow)
- Secondary button: **Import Data** (bulk upload — multiple CSVs/notebooks/exported dashboards at once)

### Stat row (direct swap for Total/Ended/Running/Pending Projects)
| Reference card | Analysis Hub equivalent |
|---|---|
| Total Projects | **Total Reports** |
| Ended Projects | **Completed Analyses** |
| Running Projects | **In Progress** (currently processing/being written) |
| Pending Project | **Pending Review** |

### Analytics chart card
Swap the S–S weekly bars for **reports uploaded per week**, or overlay it with something meaningful across all reports at once — e.g. average model R² this week, or upload volume — the empty/hatched bars naturally represent days with no uploads.

### Reminder card
Repurpose as **"Next scheduled refresh"** or **"Model retrain due"** for a report with a live/forecasting component (like the CPI repo's 12-month forecast) — CTA button becomes **"Run Refresh"** instead of "Start Meeting".

### Report list ("+ New" list card)
Each row = one uploaded report. Icon color-codes the *category* (economics, sales, ops, etc.). Example rows drawn from the CPI repo's own feature set:
- CPI Inflation Analysis — *Due/updated Nov 26, 2025*
- Sector Volatility Report — *Nov 28, 2025*
- COVID Impact Study — *Nov 30, 2025*
- 12-Month CPI Forecast — *Dec 5, 2025*
- Correlation Heatmap Refresh — *Dec 6, 2025*

### Team collaboration list
Same pattern, but "Working on **X**" refers to a shared report/dataset, and the status pill reflects that report's review state (Completed / In Progress / Pending) instead of a generic task.

### Progress donut
**% of reports reviewed/validated** this cycle, or **% of ML models currently meeting your R²/MAE threshold** — legend keeps Completed / In Progress / Pending.

### Dark "live status" card
Instead of a stopwatch, this becomes a **live processing card**: "Parsing datafile.csv…", a progress percentage instead of a timer, pause/cancel controls — shown while a bulk import is being ingested and validated.

---

## 6. Data model (per report/project)

Each uploaded analysis is one record — this is what a "project" card is rendered from:

```json
{
  "id": "cpi-inflation-2025",
  "title": "CPI Inflation Analysis",
  "description": "Time-series analysis of India's CPI, 2013–2025",
  "category": "Economics",
  "status": "in_progress",          // completed | in_progress | pending
  "owner": "Yash Vasudeva",
  "uploaded_at": "2025-11-20",
  "due_or_updated_at": "2025-11-26",
  "source_files": ["datafile.csv", "Commodities.ipynb"],
  "kpis": [
    { "label": "R-Squared (test)", "value": 0.8828 },
    { "label": "MAE (test)", "value": 1.35 }
  ],
  "charts": ["trend", "seasonality", "correlation-heatmap", "volatility"],
  "insights": [
    "General CPI rose ~90% cumulatively, 2013–2025",
    "Vegetables/spices show >35% coefficient of variation"
  ]
}
```

New uploads should map to this same shape regardless of source (CSV, notebook, an existing Flask+Chart.js mini-app like the CPI repo, a PDF report, etc.), so the dashboard can render any of them as a uniform card/list entry and roll them up into the top-level stat cards and charts.

## 7. Suggested build path

1. **Frontend:** React + Tailwind (or plain HTML/CSS/JS + Chart.js, matching the CPI repo's own stack, if you want to keep one language across projects) using the tokens/components above.
2. **Backend:** Flask (consistent with the reference repo) with routes namespaced per report: `/api/reports`, `/api/reports/<id>/kpis`, `/api/reports/<id>/trends`, etc. — essentially the CPI repo's existing API pattern, generalized so any report registers its own endpoints under its `id`.
3. **Storage:** one folder per uploaded report (data + notebook + generated metadata.json following the schema above); a lightweight registry (SQLite or a single `reports.json`) that the dashboard reads to render cards, stats, and charts.
4. **Upload flow:** "Import Data" accepts multiple files at once → backend validates/parses each → creates a `pending` report entry → status flips to `in_progress` while charts/KPIs are generated → `completed` once validated.
