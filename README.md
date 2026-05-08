# Council Swimming Analytics

A suite of interactive data tools built for **West Lancashire Borough Council** to analyse weekly swimming lesson performance across two sites — **Park Pool** and **Nye Bevan**.

Built and delivered end-to-end: from raw weekly booking CSV exports to council-ready management dashboards, currently in active use and being presented to the local council.

---

## Tools

### 🔄 Weekly Analyser (`swimming_weekly_analyser.html`)
The core tool. Drop in any weekly bookings CSV and it instantly generates a full performance report — no server, no login, no setup required.

**Produces automatically:**
- Combined summary across both pools
- Park Pool vs Nye Bevan side-by-side comparison
- Capacity utilisation breakdown (green / amber / red)
- Fill rate by stage, sorted best to worst
- Under-utilised classes flagged (<50% full)
- Teacher workload and average fill rate

**[▶ Try it live](https://thomasjdwaugh.github.io/council-swimming-analytics/swimming_weekly_analyser.html)**

---

### 🏊 Park Pool Dashboard (`park_pool_dashboard.html`)
Detailed lesson-level view for Park Pool — 130 group lessons, filterable by day, stage, teacher, and class name. Shows bookings, capacity, and fill rate per lesson.

### 🏊 Nye Bevan Dashboard (`nye_bevan_dashboard.html`)
Same dashboard for Nye Bevan — 63 lessons across 5 teachers with full fill rate breakdown.

### 📊 Council Insights Dashboard (`council_insights_dashboard.html`)
Executive summary built for council presentation — pool comparison, capacity utilisation buckets, stage-level fill rates, and a flagged list of under-utilised classes requiring action.

---

## How It Works

All tools are **standalone HTML files** — no backend, no dependencies, no installation. They run entirely in the browser using vanilla JavaScript.

The weekly analyser reads the CSV client-side, infers teachers from class names, filters private 1-2-1 lessons automatically, and renders the full dashboard in under a second.

**Expected CSV columns:**
```
Description | Class Name | Class Date Time | Bookings | Class Size | % Uptake | Income
```

---

## Stack

`HTML` · `CSS` · `Vanilla JavaScript` · `CSV parsing` · `GitHub Pages`

---

## Context

This project was built alongside my role as a Lifeguard/Gym Instructor at West Lancashire Borough Council. Management needed a way to identify underperforming lessons — classes with low fill rates, imbalanced teacher workloads, and capacity being wasted — without relying on manual spreadsheet analysis each week.

The result is a zero-dependency, self-service reporting tool that any non-technical manager can use by dragging and dropping a CSV file. The insights generated are now being used to make operational timetabling decisions and are being presented directly to the council.

---

## Author

**Thomas Waugh** — AI Engineer · MSc Data Science · BSc Human Biology & Infectious Disease

[GitHub](https://github.com/ThomasJDWaugh) · [LinkedIn](https://linkedin.com/in/tomwaugh-msc)# council-swimming-analytics
