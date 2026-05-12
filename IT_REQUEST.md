# IT Support Request — Swimming Lesson Analytics Dashboard
**West Lancashire Borough Council — Leisure Services**
**Date:** 14 May 2026
**Requested by:** Thomas Waugh

---

## What this system does

A lightweight internal web dashboard that displays live swimming lesson booking data for managers at Park Pool and Nye Bevan. It replaces a manual weekly process of building spreadsheet reports.

Managers export a CSV file from Scuba (the leisure management system), drop it into a shared folder, and the dashboard updates automatically within seconds. No data leaves the council network.

---

## What we are asking IT to support

We have two options depending on what is feasible. **Option A is preferred** but Option B requires no network changes at all.

---

### Option A — Preferred: Live web dashboard (all managers access via browser)

**What it requires:**

| Item | Detail |
|------|--------|
| **Python 3.11+** | Installed on one designated host PC |
| **Firewall rule** | Allow inbound TCP on port **8080**, local network only (no internet exposure) |
| **Task Scheduler job** | Auto-start the dashboard server when the host PC boots |
| **G: drive folder** | A subfolder created on the G: drive, e.g. `G:\Leisure\Swimming Exports` |
| **G: drive access** | The host PC's service account needs read access to that folder |

**How it works:**
- The server runs on one PC (could be the server, or a designated office PC)
- All managers on the same network open a browser and go to `http://[host-PC-IP]:8080`
- Nothing is installed on managers' individual machines
- The server only listens on the local network — no internet access required or used

**Data & security:**
- All data stays on the council network — no cloud, no external services
- No login or authentication needed (local network only)
- No personal data — booking numbers and class names only
- The only external request the dashboard makes is loading a Google Font — this can be removed if required

---

### Option B — Fallback: Standalone file generator (no network changes needed)

If a firewall change is not possible, this option requires only Python to be installed on one machine.

**What it requires:**

| Item | Detail |
|------|--------|
| **Python 3.11+** | Installed on one PC (the manager who exports from Scuba) |
| **Task Scheduler job** | Optional — auto-run the generator script on a schedule |
| **G: drive folder** | A subfolder created on the G: drive |

**How it works:**
- Manager exports CSV from Scuba → saves to G: drive folder
- Double-clicks `generate.bat` (or it runs automatically via Task Scheduler)
- A `dashboard.html` file is created in the G: drive folder
- Any manager opens that file in their browser — no server, no port, no network changes

---

## Technical specifications

| Component | Detail |
|-----------|--------|
| Language | Python 3.11+ |
| Dependencies | FastAPI, Uvicorn, Watchdog, Pandas (all installable via pip) |
| Port | 8080 (TCP, inbound, local network only) |
| Host OS | Windows 10/11 |
| Disk space | < 50 MB including Python dependencies |
| Network | Local network only — no outbound internet required for core function |
| Data stored | None — everything held in memory, CSV is the source of truth |
| Logs | Plain text log file written locally (`logs/activity.log`) |

---

## Questions for IT

1. Can Python 3.11+ be installed on a council PC? If not, can we use a bundled executable (.exe) instead?
2. Can a firewall rule be created to allow TCP port 8080, local network traffic only?
3. Is there a designated always-on PC or server we could use as the host?
4. Can a Task Scheduler job be created to auto-start a script on system boot?
5. Can a subfolder be created on the G: drive and access granted to the relevant user accounts?
6. Are there any restrictions on running pip / installing Python packages?
7. If a bundled .exe is preferred to a raw Python install, is that something IT would approve?

---

## Contact

Thomas Waugh — [add contact details]

---

*The full source code for this system is available for IT review at:*
*https://github.com/ThomasWaugh/council-swimming-analytics*
