import pandas as pd
from datetime import datetime
from pathlib import Path


ALLOWED_POOLS = {"Park Pool", "Nye Bevan"}
PRIVATE_LESSON_KEYWORDS = ["1-2-1", "2-2-1"]

# ── Park Pool: class_name → teacher (from park_pool_dashboard.html teacherMap) ──
_PARK_POOL_MAP: dict[str, str] = {
    "Adult & Baby 10am Fri": "Mike",
    "Adult & Baby 10am Mon": "Mike",
    "Adult & Baby 11.30am Tue": "Mike",
    "Adult & Baby 1130  Sat": "Mike",
    "Adult & Baby 12.30pm Wed": "Mike",
    "Adult & Toddler 10.30am Fri": "Mike",
    "Adult & Toddler 10.30am Mon": "Mike",
    "Adult & Toddler 10.30am Tue": "Mike",
    "Adult & Toddler 10am Wed": "Mike",
    "Adult & Toddler 11am Mon": "Mike",
    "Adult & Toddler 1200  Sat": "Mike",
    "Adult & Toddler 9.30am Tue": "Mike",
    "Adult Advanced 19.00pm Tue": "Abner",
    "Adult Beginner 20.00pm Tue": "Abner",
    "Adult Improver 19.30pm Tue": "Abner",
    "Bronze & Silver Challenge 18.00pm Tue": "Mike",
    "Bronze & Silver Challenge 18.30pm Wed": "Mike",
    "Duckling 3 09.30 Mike Wed": "Mike",
    "Duckling 3 11.30 Wednesday Mike Wed": "Mike",
    "Duckling 3 12.00 Monday Mike": "Mike",
    "Duckling 3 12.00PM Tuesday Mike": "Mike",
    "Duckling 3 13.00 Mike Fri": "Mike",
    "Duckling 3 13.00 Monday Mike": "Mike",
    "Duckling 3 Fri 12.00 Mike": "Mike",
    "Duckling 4 09.00am Mike Sat": "Mike",
    "Duckling 4 10.00am Mike Sat": "Mike",
    "Duckling 4 11.00am Mike Fri": "Mike",
    "Duckling 4 16.00pm Abner": "Abner",
    "Duckling 4 16.30pm Abner": "Abner",
    "Duckling 4 17.00pm Abner": "Abner",
    "Gold & Honours 19.15pm Challenge Wed": "Mike",
    "Gold & Honours Challenge 18.30pm Fri": "Mike",
    "Gold & Honours Challenge 18.45pm Tue": "Mike",
    "Pre School 10.00am Tue": "Mike",
    "Pre School 10.30am Wed": "Mike",
    "Pre School 11.00am Sat": "Mike",
    "Pre School 11.30am Fri": "Mike",
    "Pre School 11.30am Mon": "Mike",
    "Pre School 11am Tue": "Mike",
    "Pre School 11am Wed": "Mike",
    "Pre School 12.00pm Wed": "Mike",
    "Pre School 13.30pm Fri": "Mike",
    "Pre School 13.30pm Mon": "Mike",
    "Pre School 9.30am Fri": "Mike",
    "Pre School 9.30am Mon": "Mike",
    "Pre School 9.30am Sat": "Mike",
    "Rookie Lifeguard 18.30pm Fri": "Jordan",
    "Stage 1  16.00pm Tue": "Mike",
    "Stage 1 10.30am Sat": "Mike",
    "Stage 1 13.30pm Sat": "Mike",
    "Stage 1 16.00pm Jordan Fri": "Jordan",
    "Stage 1 16.30pm Sat": "Mike",
    "Stage 1 17.00pm Abner Tue": "Abner",
    "Stage 1 17.00pm Thu": "Aimee",
    "Stage 1 17.30pm Abner": "Abner",
    "Stage 1 17.30pm Tue": "Aimee",
    "Stage 1 18.00 Aimee Thu": "Aimee",
    "Stage 1 18.00pm Abner": "Abner",
    "Stage 1 4.30pm Mon": "Aimee",
    "Stage 2 16.00pm Mon": "Aimee",
    "Stage 2 16.00pm Sat": "Mike",
    "Stage 2 16.00pm Thu": "Natalie",
    "Stage 2 16.30 Aimee Tue": "Aimee",
    "Stage 2 16.30pm Fri": "Natalie",
    "Stage 2 17.00pm Tue": "Aimee",
    "Stage 2 17.30pm Abner": "Abner",
    "Stage 2 17.30pm Fri": "Mike",
    "Stage 2 17.30pm Mon": "Abner",
    "Stage 2 18.00pm Nat": "Natalie",
    "Stage 2 5.30pm  Wed": "Mike",
    "Stage 2 5pm Mon": "Natalie",
    "Stage 2 8.30am Sat": "Mike",
    "Stage 2 9.30am Sat": "Aimee",
    "Stage 3 15.30pm Mike Sat": "Mike",
    "Stage 3 16.00pm Abner Tue": "Abner",
    "Stage 3 16.00PM Nat Mon": "Natalie",
    "Stage 3 16.00pm Thu": "Aimee",
    "Stage 3 16.30pm Fri": "Jordan",
    "Stage 3 16.30pm Thu": "Natalie",
    "Stage 3 17.00pm Carlos Wed": "Lola",
    "Stage 3 17.00pm Fri": "Mike",
    "Stage 3 17.30pm Mon": "Aimee",
    "Stage 3 18.00pm Abner": "Abner",
    "Stage 3 9.00am Sat": "Aimee",
    "Stage 3 Mike Friday 18.00pm": "Mike",
    "Stage 4 08.30am Aimee Sat": "Aimee",
    "Stage 4 10.00am Sat": "Aimee",
    "Stage 4 11.30am Sat": "Aimee",
    "Stage 4 16.00 Aimee Tue": "Aimee",
    "Stage 4 16.30 Abner Tue": "Abner",
    "Stage 4 17.30pm Fri": "Natalie",
    "Stage 4 4.00pm wed": "Lola",
    "Stage 4 Fri 5.00pm": "Jordan",
    "Stage 4 Mon 4.30pm": "Abner",
    "Stage 4 Mon 5.30pm": "Natalie",
    "Stage 4 Mon 6.00pm": "Aimee",
    "Stage 4 Thu 5.00pm": "Natalie",
    "Stage 4 Thu 5.30pm": "Aimee",
    "Stage 4 Wed 4.30pm": "Mike",
    "Stage 4 Wed 6.00pm": "Mike",
    "Stage 5 17.30pm Thu": "Natalie",
    "Stage 5 4.30pm wed": "Lola",
    "Stage 5 Fri 4.00pm": "Natalie",
    "Stage 5 Fri 4.30pm": "Mike",
    "Stage 5 Fri 5.30pm": "Jordan",
    "Stage 5 Mon 4.00pm": "Abner",
    "Stage 5 Mon 4.30pm": "Natalie",
    "Stage 5 Mon 5.00pm": "Aimee",
    "Stage 5 Sat 10.30am": "Aimee",
    "Stage 5 Sat 2.30pm": "Mike",
    "Stage 5 Thu 4.30pm": "Aimee",
    "Stage 5 Tue 4.30pm": "Mike",
    "Stage 5 Tue 6.00pm": "Aimee",
    "Stage 6 18.30pm Wed": "Lola",
    "Stage 6 5.30pm Wed": "Lola",
    "Stage 6 Fri 4.00pm": "Mike",
    "Stage 6 Mon 5.00pm": "Abner",
    "Stage 6 Mon 6.00pm": "Natalie",
    "Stage 6 Nat 17.00pm": "Natalie",
    "Stage 6 Sat 11.00am": "Aimee",
    "Stage 6 Sat 2.00pm": "Mike",
    "Stage 6 Thu 6.00pm": "Natalie",
    "Stage 6 Tue 5.30pm": "Mike",
    "Stage 7 15.00pm Mike Sat": "Mike",
    "Stage 7 6.00pm Wed": "Lola",
    "Stage 7 Fri 6.00pm": "Jordan",
    "Stage 7 Thu 6.30pm": "Natalie",
    "Stage 7 Tue 5.00pm": "Mike",
    "Stage 7 Wed 5.00pm": "Mike",
}

# ── Nye Bevan: (class_name, day, time) → teacher (from nye_bevan_dashboard.html) ──
_NYE_BEVAN_MAP: dict[tuple[str, str, str], str] = {
    ("Stage 1 Mon",          "Mon", "16:00"): "Stuart",
    ("Stage 2 Mon",          "Mon", "16:30"): "Stuart",
    ("Stage 4 Mon",          "Mon", "16:30"): "Stuart",
    ("Stage 4 Mon",          "Mon", "17:00"): "Stuart",
    ("Stage 1 Mon",          "Mon", "17:30"): "Stuart",
    ("Stage 4 Mon",          "Mon", "18:00"): "Stuart",
    ("Stage 3 Mon",          "Mon", "18:30"): "Stuart",
    ("Stage 3 Mon",          "Mon", "16:00"): "Heather",
    ("Stage 3 Mon",          "Mon", "17:00"): "Heather",
    ("Stage 6 Mon",          "Mon", "17:30"): "Heather",
    ("Stage 5 Mon",          "Mon", "18:00"): "Heather",
    ("Advanced Academy Mon", "Mon", "18:30"): "Heather",
    ("stage 7 19.15pm",      "Mon", "19:15"): "Heather",
    ("Stage 3 Tue",          "Tue", "16:00"): "Caira",
    ("Stage 1 Tue",          "Tue", "16:30"): "Caira",
    ("Stage 2 Tue",          "Tue", "17:00"): "Caira",
    ("Stage 7 Tue",          "Tue", "17:30"): "Caira",
    ("Stage 1 Tue",          "Tue", "18:00"): "Caira",
    ("Bronze/ Silver Tue",   "Tue", "18:30"): "Caira",
    ("duckling 4",           "Tue", "16:00"): "Jade",
    ("Stage 2 Tue",          "Tue", "16:30"): "Jade",
    ("Stage 1 Tue",          "Tue", "17:00"): "Jade",
    ("Stage 6 Tue",          "Tue", "17:30"): "Jade",
    ("Stage 2 Wed",          "Wed", "16:00"): "Heather",
    ("Stage 1 Wed",          "Wed", "16:30"): "Stuart",
    ("Stage 4 Wed",          "Wed", "16:30"): "Heather",
    ("Stage 4 Wed",          "Wed", "17:00"): "Stuart",
    ("Stage 3 Wed",          "Wed", "17:00"): "Heather",
    ("Stage 2 Wed",          "Wed", "17:30"): "Stuart",
    ("stage 3 5.30pm HJ",    "Wed", "17:30"): "Heather",
    ("Stage 3 Wed",          "Wed", "18:00"): "Stuart",
    ("Stage 1 Wed",          "Wed", "18:00"): "Heather",
    ("Stage 6 Wed",          "Wed", "18:30"): "Heather",
    ("Stage 5 Wed",          "Wed", "19:00"): "Heather",
    ("Adult Beginner Wed",   "Wed", "19:30"): "Heather",
    ("Stage 5 Thu",          "Thu", "16:00"): "Heather",
    ("Stage 2 Thu",          "Thu", "16:30"): "Heather",
    ("Stage 4 Thu",          "Thu", "17:00"): "Heather",
    ("Stage 1 Thu",          "Thu", "17:30"): "Heather",
    ("Stage 4 Thu",          "Thu", "18:00"): "Heather",
    ("SEN Thu",              "Thu", "18:30"): "Heather",
    ("Stage 3 Thu",          "Thu", "16:30"): "Stuart",
    ("Stage 3 Thu",          "Thu", "17:00"): "Stuart",
    ("stage 5 17.30pm",      "Thu", "17:30"): "Stuart",
    ("stage 6 6pm sj",       "Thu", "18:00"): "Stuart",
    ("stage 1 16.00 thur",   "Thu", "16:00"): "Lola",
    ("stage 7 16.30 thur",   "Thu", "16:30"): "Lola",
    ("stage 2 17.00 thur",   "Thu", "17:00"): "Lola",
    ("bronze 17.30 thur",    "Thu", "17:30"): "Lola",
    ("stage 3 18.00 thur",   "Thu", "18:00"): "Lola",
    ("Stage 5 Fri",          "Fri", "16:00"): "Caira",
    ("Duckling 4 Fri",       "Fri", "16:30"): "Caira",
    ("stage 1 5.00pm",       "Fri", "17:00"): "Caira",
    ("Stage 2 Fri",          "Fri", "17:30"): "Caira",
    ("Stage 5 Fri",          "Fri", "18:00"): "Caira",
    ("Stage 3 Fri",          "Fri", "16:30"): "Stuart",
    ("Stage 6 Fri",          "Fri", "17:00"): "Stuart",
    ("Stage 1 Fri",          "Fri", "17:30"): "Stuart",
    ("Stage 4 Fri",          "Fri", "18:00"): "Stuart",
    ("Stage 3 Sat",              "Sat", "09:15"): "Caira",
    ("Stage 2 Sat",              "Sat", "09:45"): "Caira",
    ("Stage 1 Sat",              "Sat", "10:15"): "Caira",
    ("duckling 4 10.45am Sat",   "Sat", "10:45"): "Caira",
}


def _infer_teacher(class_name: str, pool: str, day: str, time: str) -> str:
    if pool == "Park Pool" and class_name in _PARK_POOL_MAP:
        return _PARK_POOL_MAP[class_name]
    if pool == "Nye Bevan":
        key = (class_name, day, time)
        if key in _NYE_BEVAN_MAP:
            return _NYE_BEVAN_MAP[key]
    # keyword fallback for any class names not yet in the override maps
    name = class_name.lower()
    if "jordan" in name or "jord" in name or "rookie" in name:
        return "Jordan"
    if "aimee" in name:
        return "Aimee"
    if "natalie" in name or "nat " in name:
        return "Natalie"
    if "abner" in name:
        return "Abner"
    if "carlos" in name or "lola" in name:
        return "Lola"
    if (
        "mike" in name
        or "duckling 3" in name
        or "pre school" in name
        or "adult & baby" in name
        or "adult & toddler" in name
        or "bronze & silver" in name
        or "gold & honours" in name
    ):
        return "Mike"
    if "heather" in name or "sen" in name:
        return "Heather"
    if "caira" in name:
        return "Caira"
    if "jade" in name:
        return "Jade"
    if "stuart" in name:
        return "Stuart"
    return "Unknown"


def _infer_stage(class_name: str) -> str:
    name = class_name.lower()
    if "adult & baby" in name:
        return "Adult & Baby"
    if "adult & toddler" in name:
        return "Adult & Toddler"
    if "gold" in name and "honour" in name:
        return "Gold/Honours"
    if "bronze" in name and "silver" in name:
        return "Bronze/Silver"
    if "adult" in name and ("advanced" in name or "improver" in name or "beginner" in name):
        return "Adult"
    if "duckling" in name or "duck" in name:
        return "Ducklings"
    if "bronze" in name:
        return "Bronze"
    if "silver" in name:
        return "Silver"
    if "rookie" in name:
        return "Rookie"
    if "pre school" in name or "preschool" in name:
        return "Pre-School"
    if "advanced" in name:
        return "Advanced Academy"
    if "sen" in name:
        return "SEN"
    for i in range(1, 11):
        if f"stage {i}" in name:
            return f"Stage {i}"
    return "Other"


def _parse_uptake(value) -> float:
    try:
        return float(str(value).replace("%", "").strip())
    except (ValueError, TypeError):
        return 0.0


def process_csv(filepath: str) -> dict:
    path = Path(filepath)
    df = pd.read_csv(filepath, dtype=str)

    df.columns = [c.strip() for c in df.columns]

    required = {"Description", "Class Name", "Class Date Time", "Bookings", "Class Size", "% Uptake", "Income"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")

    df = df[df["Description"].isin(ALLOWED_POOLS)].copy()

    mask = df["Class Name"].apply(
        lambda n: not any(kw in str(n) for kw in PRIVATE_LESSON_KEYWORDS)
    )
    df = df[mask].copy()

    df["Class Date Time"] = pd.to_datetime(df["Class Date Time"], dayfirst=True, errors="coerce")
    df = df[df["Class Date Time"].notna()].copy()

    df["day"] = df["Class Date Time"].dt.strftime("%a")
    df["time"] = df["Class Date Time"].dt.strftime("%H:%M")
    df["bookings"] = pd.to_numeric(df["Bookings"], errors="coerce").fillna(0).astype(int)
    df["class_size"] = pd.to_numeric(df["Class Size"], errors="coerce").fillna(0).astype(int)
    df["uptake"] = df["% Uptake"].apply(_parse_uptake)
    df["teacher"] = df.apply(
        lambda row: _infer_teacher(
            str(row["Class Name"]).strip(),
            str(row["Description"]).strip(),
            row["day"],
            row["time"],
        ),
        axis=1,
    )
    df["stage"] = df["Class Name"].apply(_infer_stage)

    def row_to_lesson(row) -> dict:
        return {
            "class_name": str(row["Class Name"]).strip(),
            "pool": str(row["Description"]).strip(),
            "day": row["day"],
            "time": row["time"],
            "stage": row["stage"],
            "teacher": row["teacher"],
            "bookings": int(row["bookings"]),
            "class_size": int(row["class_size"]),
            "uptake": round(float(row["uptake"]), 1),
        }

    all_lessons = [row_to_lesson(row) for _, row in df.iterrows()]

    park_lessons = [l for l in all_lessons if l["pool"] == "Park Pool"]
    nye_lessons = [l for l in all_lessons if l["pool"] == "Nye Bevan"]

    def pool_stats(lessons: list) -> dict:
        if not lessons:
            return {"total_lessons": 0, "total_booked": 0, "total_capacity": 0, "avg_fill_rate": 0.0}
        total_booked = sum(l["bookings"] for l in lessons)
        total_capacity = sum(l["class_size"] for l in lessons)
        avg_fill = round(
            (total_booked / total_capacity * 100) if total_capacity > 0 else 0.0, 1
        )
        return {
            "total_lessons": len(lessons),
            "total_booked": total_booked,
            "total_capacity": total_capacity,
            "avg_fill_rate": avg_fill,
        }

    park_stats = pool_stats(park_lessons)
    nye_stats = pool_stats(nye_lessons)

    total_booked = park_stats["total_booked"] + nye_stats["total_booked"]
    total_capacity = park_stats["total_capacity"] + nye_stats["total_capacity"]
    total_lessons = park_stats["total_lessons"] + nye_stats["total_lessons"]
    avg_fill = round((total_booked / total_capacity * 100) if total_capacity > 0 else 0.0, 1)

    stage_map: dict[str, dict] = {}
    for lesson in all_lessons:
        s = lesson["stage"]
        if s not in stage_map:
            stage_map[s] = {"stage": s, "lessons": 0, "booked": 0, "capacity": 0}
        stage_map[s]["lessons"] += 1
        stage_map[s]["booked"] += lesson["bookings"]
        stage_map[s]["capacity"] += lesson["class_size"]

    stage_breakdown = []
    for s in stage_map.values():
        cap = s["capacity"]
        s["avg_fill_rate"] = round((s["booked"] / cap * 100) if cap > 0 else 0.0, 1)
        stage_breakdown.append(s)
    stage_breakdown.sort(key=lambda x: x["avg_fill_rate"], reverse=True)

    teacher_map: dict[str, dict] = {}
    for lesson in all_lessons:
        t = lesson["teacher"]
        if t not in teacher_map:
            teacher_map[t] = {"teacher": t, "lessons": 0, "booked": 0, "capacity": 0}
        teacher_map[t]["lessons"] += 1
        teacher_map[t]["booked"] += lesson["bookings"]
        teacher_map[t]["capacity"] += lesson["class_size"]

    teacher_breakdown = []
    for t in teacher_map.values():
        cap = t["capacity"]
        t["avg_fill_rate"] = round((t["booked"] / cap * 100) if cap > 0 else 0.0, 1)
        teacher_breakdown.append(t)
    teacher_breakdown.sort(key=lambda x: x["teacher"])

    under_utilised = sorted(
        [l for l in all_lessons if l["uptake"] < 50],
        key=lambda x: x["uptake"],
    )

    week_range = {
        "from": df["Class Date Time"].min().strftime("%d %b %Y"),
        "to": df["Class Date Time"].max().strftime("%d %b %Y"),
    }

    return {
        "last_updated": datetime.now().isoformat(),
        "filename": path.name,
        "week_range": week_range,
        "park_pool": park_lessons,
        "nye_bevan": nye_lessons,
        "summary": {
            "total_lessons": total_lessons,
            "total_booked": total_booked,
            "total_capacity": total_capacity,
            "avg_fill_rate": avg_fill,
        },
        "pool_comparison": {
            "park_pool": park_stats,
            "nye_bevan": nye_stats,
        },
        "stage_breakdown": stage_breakdown,
        "under_utilised": under_utilised,
        "teacher_breakdown": teacher_breakdown,
    }
