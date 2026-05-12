# Swimming Lessons Live Dashboard

A live web dashboard that automatically updates whenever you export a CSV from Scuba and drop it into your OneDrive folder. No technical knowledge needed to use it day-to-day.

---

## Quick Start

### Windows (most common)

1. **Download** the `council-swimming-live` folder to your PC.
2. **Double-click `run.bat`** — a black window will open and the server will start.
3. Your browser will open automatically at **http://localhost:8080**.
4. Export your CSV from Scuba and drop it into your OneDrive folder.
5. The dashboard updates within a few seconds — no button to press.

> **Keep the black window open** while you want the dashboard to run. Closing it stops the server.

### Mac / Linux

1. Open Terminal.
2. Navigate to the folder: `cd /path/to/council-swimming-live`
3. Run: `bash run.sh`
4. Your browser will open automatically.

---

## Changing the Watch Folder

The watch folder is the OneDrive folder where you drop your Scuba CSV exports.

1. Open `config.json` in Notepad (right-click → Open with → Notepad).
2. Find the line that says `"watch_folder"` and change the path to your folder.
3. Save the file and restart the server (close and re-run `run.bat`).

**Example:**

```json
{
  "watch_folder": "C:/Users/YourName/OneDrive - West Lancashire BC/Swimming Exports",
  "server_host": "0.0.0.0",
  "server_port": 8080,
  "auto_open_browser": true
}
```

> **Tip:** Use forward slashes (`/`) in the path, not backslashes (`\`). Both work on Windows but forward slashes are safer.

---

## Setting Up Auto-Start on Windows (Recommended)

If you want the dashboard to start automatically every time the PC turns on, follow these steps. You only need to do this once.

1. Press **Windows key + R**, type `taskschd.msc`, and press Enter. This opens Task Scheduler.

2. In the right-hand panel, click **Create Basic Task…**

3. Give it a name, e.g. `Swimming Dashboard`, and click **Next**.

4. For **Trigger**, choose **When the computer starts**, then click **Next**.

5. For **Action**, choose **Start a program**, then click **Next**.

6. Click **Browse** and find `run.bat` inside your `council-swimming-live` folder.

7. In the **Start in** box, type the full path to the `council-swimming-live` folder  
   (e.g. `C:\Users\Manager\Documents\council-swimming-live`).

8. Click **Next**, then **Finish**.

9. To test it: right-click the new task in the list and choose **Run**.

The dashboard will now start automatically every time Windows starts.

---

## What the Colours Mean

| Colour | Fill Rate | Meaning |
|--------|-----------|---------|
| 🟢 **Green** | 80% or above | Class is well-attended — on target |
| 🟡 **Amber** | 50–79% | Class needs monitoring — consider promotion |
| 🔴 **Red** | Below 50% | Class is under-utilised — action may be needed |

---

## How to Export from Scuba

1. Open Scuba and go to your class/booking reports section.
2. Run the report for the relevant week.
3. Export as **CSV**.
4. Save the file into your OneDrive watch folder (the path in `config.json`).

The dashboard will detect the new file automatically and refresh within seconds.

---

## Troubleshooting

**Dashboard shows "Waiting for data"**  
→ No CSV has been detected yet. Drop a CSV file into the watch folder and wait a few seconds.

**Port already in use**  
→ Open `config.json` in Notepad and change `"server_port"` from `8080` to another number (e.g. `8081`). Save and restart.

**CSV not being picked up**  
→ Check that the `watch_folder` path in `config.json` matches your OneDrive folder exactly, including capital letters. Open File Explorer, navigate to the folder, and copy the path from the address bar.

**Browser doesn't open automatically**  
→ Manually open your browser and go to `http://localhost:8080`.

**"pip is not recognised" error when running run.bat**  
→ Python is not installed. Download Python from [python.org](https://www.python.org/downloads/), run the installer, and make sure to tick **"Add Python to PATH"** before clicking Install.

---

## Upgrading to Automatic Exports (Future)

If Delta Computer Services confirm that Scuba can export CSVs automatically to a network folder, simply update `watch_folder` in `config.json` to point at that folder. The system will then update with no manual steps at all — every export becomes a live dashboard update automatically.

---

## Technical Notes (for IT support)

- The server runs on `http://0.0.0.0:8080` by default (accessible on local network).
- All data is held in memory — there is no database. The CSV is the only source of truth.
- Logs are written to `logs/activity.log`.
- No authentication is implemented — intended for a trusted local network only.
- Dependencies: FastAPI, Uvicorn, Watchdog, Pandas (see `requirements.txt`).
