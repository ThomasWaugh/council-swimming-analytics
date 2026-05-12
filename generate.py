#!/usr/bin/env python3
"""
Generate a standalone HTML dashboard from the most recent CSV in the watch folder.
Double-click generate.bat (Windows) to run, or schedule via Task Scheduler.
No server or network needed — output is a single HTML file anyone can open.
"""

import json
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"watch_folder": str(BASE_DIR / "exports")}
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    config = load_config()
    watch_folder = Path(config.get("watch_folder", BASE_DIR / "exports"))

    if not watch_folder.exists():
        print(f"\nERROR: Watch folder not found:\n  {watch_folder}")
        print("\nPlease open config.json and update the watch_folder path.")
        input("\nPress Enter to close...")
        sys.exit(1)

    csvs = sorted(watch_folder.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not csvs:
        print(f"\nERROR: No CSV files found in:\n  {watch_folder}")
        print("\nDrop a Scuba CSV export into that folder and run this again.")
        input("\nPress Enter to close...")
        sys.exit(1)

    latest = csvs[0]
    print(f"\nProcessing: {latest.name}")

    sys.path.insert(0, str(BASE_DIR))
    from app.processor import process_csv

    try:
        data = process_csv(str(latest))
    except Exception as exc:
        print(f"\nERROR processing CSV: {exc}")
        input("\nPress Enter to close...")
        sys.exit(1)

    output_path = watch_folder / "dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(_build_html(data))

    print(f"Done! Dashboard saved to:\n  {output_path}")
    print("\nOpening in browser...")
    webbrowser.open(output_path.as_uri())


def _build_html(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    generated_at = datetime.now().strftime("%d %b %Y at %H:%M")
    week = f"{data['week_range']['from']} – {data['week_range']['to']}" if data.get("week_range") else ""
    filename = data.get("filename", "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Swimming Lessons — Dashboard ({generated_at})</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --green: #15803D; --green-bg: #DCFCE7;
      --amber: #B45309; --amber-bg: #FEF3C7;
      --red:   #B91C1C; --red-bg:   #FEE2E2;
      --grey:  #6B7280; --border: #E5E7EB;
      --card:  #FFFFFF; --page:   #F3F4F6;
      --header: #1E293B; --header-fg: #F8FAFC;
    }}
    body {{ font-family: 'DM Sans', -apple-system, sans-serif; background: var(--page); color: #111827; }}
    header {{
      background: var(--header); color: var(--header-fg);
      padding: 0 2rem; display: flex; align-items: center;
      justify-content: space-between; min-height: 60px; flex-wrap: wrap; gap: .5rem; padding-top: .75rem; padding-bottom: .75rem;
    }}
    header h1 {{ font-size: 1rem; font-weight: 600; }}
    .header-right {{ display: flex; align-items: center; gap: 1.25rem; font-size: .82rem; color: #94A3B8; flex-wrap: wrap; }}
    .snapshot-badge {{
      background: #1E3A5F; color: #BAE6FD;
      padding: .22rem .65rem; border-radius: 9999px; font-size: .78rem; font-weight: 600;
    }}
    .week-chip {{ background: #1E3A5F; color: #BAE6FD; padding: .2rem .55rem; border-radius: 9999px; font-size: .78rem; }}
    .notice {{
      background: #EFF6FF; border-left: 4px solid #3B82F6; color: #1E40AF;
      padding: .7rem 1.5rem; font-size: .82rem; font-weight: 500;
    }}
    main {{ max-width: 1280px; margin: 0 auto; padding: 1.75rem 1.5rem 3rem; }}
    .section-title {{
      font-size: .7rem; font-weight: 700; letter-spacing: .1em;
      text-transform: uppercase; color: var(--grey); margin: 2rem 0 .75rem;
    }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: .875rem; }}
    .card {{ background: var(--card); border: 1px solid var(--border); border-radius: .625rem; padding: 1.1rem 1.25rem; }}
    .card .label {{ font-size: .75rem; color: var(--grey); font-weight: 500; margin-bottom: .35rem; }}
    .card .value {{ font-size: 1.9rem; font-weight: 700; line-height: 1.1; }}
    .card.green-accent {{ border-left: 4px solid var(--green); }}
    .card.amber-accent {{ border-left: 4px solid var(--amber); }}
    .card.red-accent   {{ border-left: 4px solid var(--red); }}
    .pool-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: .875rem; }}
    @media (max-width: 640px) {{ .pool-grid {{ grid-template-columns: 1fr; }} }}
    .pool-card {{ background: var(--card); border: 1px solid var(--border); border-radius: .625rem; padding: 1.25rem; }}
    .pool-card h3 {{ font-size: .95rem; font-weight: 700; margin-bottom: 1rem; }}
    .pool-stat-row {{ display: flex; justify-content: space-between; align-items: center; padding: .35rem 0; border-bottom: 1px solid var(--border); font-size: .875rem; }}
    .pool-stat-row:last-child {{ border-bottom: none; }}
    .pool-stat-row .stat-val {{ font-weight: 600; }}
    .bucket-grid {{ display: grid; grid-template-columns: repeat(3,1fr); gap: .875rem; }}
    @media (max-width: 640px) {{ .bucket-grid {{ grid-template-columns: 1fr; }} }}
    .bucket {{ border-radius: .625rem; padding: 1.1rem 1.25rem; font-size: .875rem; }}
    .bucket.green {{ background: var(--green-bg); }}
    .bucket.amber {{ background: var(--amber-bg); }}
    .bucket.red   {{ background: var(--red-bg); }}
    .bucket .bkt-label {{ font-weight: 700; font-size: .8rem; margin-bottom: .5rem; }}
    .bucket.green .bkt-label {{ color: var(--green); }}
    .bucket.amber .bkt-label {{ color: var(--amber); }}
    .bucket.red   .bkt-label {{ color: var(--red); }}
    .bucket .bkt-count {{ font-size: 2rem; font-weight: 700; }}
    .bucket .bkt-sub {{ font-size: .75rem; color: var(--grey); margin-top: .15rem; }}
    .table-wrap {{ background: var(--card); border: 1px solid var(--border); border-radius: .625rem; overflow: hidden; }}
    table {{ width: 100%; border-collapse: collapse; font-size: .85rem; }}
    thead th {{ background: #F9FAFB; padding: .65rem 1rem; text-align: left; font-weight: 600; font-size: .78rem; color: var(--grey); border-bottom: 1px solid var(--border); white-space: nowrap; }}
    tbody td {{ padding: .6rem 1rem; border-bottom: 1px solid var(--border); vertical-align: middle; }}
    tbody tr:last-child td {{ border-bottom: none; }}
    tbody tr:hover {{ background: #F9FAFB; }}
    .pill {{ display: inline-block; padding: .2rem .55rem; border-radius: 9999px; font-size: .72rem; font-weight: 700; }}
    .pill.green {{ background: var(--green-bg); color: var(--green); }}
    .pill.amber {{ background: var(--amber-bg); color: var(--amber); }}
    .pill.red   {{ background: var(--red-bg);   color: var(--red); }}
    .bar-wrap {{ display: flex; align-items: center; gap: .5rem; }}
    .bar-bg {{ flex: 1; height: 8px; background: var(--border); border-radius: 9999px; overflow: hidden; min-width: 60px; }}
    .bar-fill {{ height: 100%; border-radius: 9999px; }}
    .bar-fill.green {{ background: var(--green); }}
    .bar-fill.amber {{ background: var(--amber); }}
    .bar-fill.red   {{ background: var(--red); }}
    .bar-label {{ font-size: .8rem; font-weight: 600; min-width: 40px; text-align: right; }}
    .teacher-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .875rem; }}
    .teacher-card {{ background: var(--card); border: 1px solid var(--border); border-radius: .625rem; padding: 1.1rem 1.25rem; }}
    .teacher-card h4 {{ font-size: .9rem; font-weight: 700; margin-bottom: .75rem; }}
    .t-stat {{ display: flex; justify-content: space-between; font-size: .8rem; margin-bottom: .3rem; }}
    .t-stat .t-val {{ font-weight: 600; }}
    @media print {{
      header {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .notice {{ display: none; }}
    }}
  </style>
</head>
<body>
<header>
  <h1>West Lancashire — Swimming Lessons Dashboard</h1>
  <div class="header-right">
    <span class="week-chip">{week}</span>
    <span>{filename}</span>
    <span>Generated {generated_at}</span>
    <span class="snapshot-badge">Snapshot</span>
  </div>
</header>
<div class="notice">
  This is a saved snapshot — data will not update automatically.
  To refresh, drop a new CSV into the watch folder and run <strong>generate.bat</strong> again.
</div>
<main id="main-content"></main>

<script>
const DATA = {data_json};

function colorClass(u) {{ return u >= 80 ? 'green' : u >= 50 ? 'amber' : 'red'; }}
function pill(u) {{ const c = colorClass(u); return `<span class="pill ${{c}}">${{u.toFixed(1)}}%</span>`; }}
function bar(u) {{
  const c = colorClass(u), w = Math.min(100, u).toFixed(1);
  return `<div class="bar-wrap"><div class="bar-bg"><div class="bar-fill ${{c}}" style="width:${{w}}%"></div></div><span class="bar-label" style="color:var(--${{c}})">${{u.toFixed(1)}}%</span></div>`;
}}
function fmt(n) {{ return Number(n).toLocaleString(); }}

function renderPoolCard(title, s) {{
  return `<div class="pool-card"><h3>${{title}}</h3>
    <div class="pool-stat-row"><span>Total Classes</span><span class="stat-val">${{fmt(s.total_lessons)}}</span></div>
    <div class="pool-stat-row"><span>Booked</span><span class="stat-val">${{fmt(s.total_booked)}}</span></div>
    <div class="pool-stat-row"><span>Capacity</span><span class="stat-val">${{fmt(s.total_capacity)}}</span></div>
    <div class="pool-stat-row"><span>Avg Fill Rate</span>${{bar(s.avg_fill_rate)}}</div>
  </div>`;
}}

function renderBuckets(lessons) {{
  const g = lessons.filter(l => l.uptake >= 80).length;
  const a = lessons.filter(l => l.uptake >= 50 && l.uptake < 80).length;
  const r = lessons.filter(l => l.uptake < 50).length;
  return `
    <div class="bucket green"><div class="bkt-label">≥ 80% — Good</div><div class="bkt-count">${{g}}</div><div class="bkt-sub">classes at or above target</div></div>
    <div class="bucket amber"><div class="bkt-label">50–79% — Monitor</div><div class="bkt-count">${{a}}</div><div class="bkt-sub">classes needing attention</div></div>
    <div class="bucket red"><div class="bkt-label">&lt; 50% — Low</div><div class="bkt-count">${{r}}</div><div class="bkt-sub">under-utilised classes</div></div>`;
}}

function renderStageTable(stages) {{
  const rows = stages.map(s => `<tr><td>${{s.stage}}</td><td>${{s.lessons}}</td><td>${{fmt(s.booked)}}</td><td>${{fmt(s.capacity)}}</td><td>${{bar(s.avg_fill_rate)}}</td></tr>`).join('');
  return `<div class="table-wrap"><table><thead><tr><th>Stage</th><th>Classes</th><th>Booked</th><th>Capacity</th><th>Fill Rate</th></tr></thead><tbody>${{rows}}</tbody></table></div>`;
}}

function renderUnderUtilised(lessons) {{
  if (!lessons.length) return `<div class="bucket green" style="border-radius:.625rem;padding:1.1rem 1.25rem"><div class="bkt-label">All clear</div><div style="font-size:.875rem;color:var(--green);margin-top:.35rem">No classes below 50% utilisation.</div></div>`;
  const rows = lessons.map(l => `<tr><td>${{l.class_name}}</td><td>${{l.pool}}</td><td>${{l.day}}</td><td>${{l.time}}</td><td>${{l.stage}}</td><td>${{l.teacher}}</td><td>${{l.bookings}} / ${{l.class_size}}</td><td>${{pill(l.uptake)}}</td></tr>`).join('');
  return `<div class="table-wrap"><table><thead><tr><th>Class</th><th>Pool</th><th>Day</th><th>Time</th><th>Stage</th><th>Teacher</th><th>Booked / Cap</th><th>Fill</th></tr></thead><tbody>${{rows}}</tbody></table></div>`;
}}

function renderTeacherCards(teachers) {{
  return teachers.map(t => `<div class="teacher-card"><h4>${{t.teacher}}</h4>
    <div class="t-stat"><span>Classes</span><span class="t-val">${{t.lessons}}</span></div>
    <div class="t-stat"><span>Booked</span><span class="t-val">${{fmt(t.booked)}}</span></div>
    <div class="t-stat"><span>Capacity</span><span class="t-val">${{fmt(t.capacity)}}</span></div>
    <div style="margin-top:.5rem">${{bar(t.avg_fill_rate)}}</div>
  </div>`).join('');
}}

const s = DATA.summary;
const allLessons = [...(DATA.park_pool || []), ...(DATA.nye_bevan || [])];

document.getElementById('main-content').innerHTML = `
  <p class="section-title">Summary</p>
  <div class="summary-grid">
    <div class="card"><div class="label">Total Classes</div><div class="value">${{fmt(s.total_lessons)}}</div></div>
    <div class="card"><div class="label">Total Booked</div><div class="value">${{fmt(s.total_booked)}}</div></div>
    <div class="card"><div class="label">Total Capacity</div><div class="value">${{fmt(s.total_capacity)}}</div></div>
    <div class="card ${{colorClass(s.avg_fill_rate)}}-accent">
      <div class="label">Avg Fill Rate</div>
      <div class="value" style="color:var(--${{colorClass(s.avg_fill_rate)}})">${{s.avg_fill_rate.toFixed(1)}}%</div>
    </div>
  </div>
  <p class="section-title">Pool Comparison</p>
  <div class="pool-grid">
    ${{renderPoolCard('Park Pool', DATA.pool_comparison.park_pool)}}
    ${{renderPoolCard('Nye Bevan', DATA.pool_comparison.nye_bevan)}}
  </div>
  <p class="section-title">Capacity Utilisation</p>
  <div class="bucket-grid">${{renderBuckets(allLessons)}}</div>
  <p class="section-title">Stage Breakdown</p>
  ${{renderStageTable(DATA.stage_breakdown)}}
  <p class="section-title">Under-Utilised Classes <span style="font-weight:400;text-transform:none;letter-spacing:0;font-size:.75rem;color:var(--red)">(below 50%, worst first)</span></p>
  ${{renderUnderUtilised(DATA.under_utilised)}}
  <p class="section-title">Teacher Breakdown</p>
  <div class="teacher-grid">${{renderTeacherCards(DATA.teacher_breakdown)}}</div>
`;
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()
