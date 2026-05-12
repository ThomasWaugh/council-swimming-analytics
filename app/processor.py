import pandas as pd
from datetime import datetime
from pathlib import Path


ALLOWED_POOLS = {"Park Pool", "Nye Bevan"}
PRIVATE_LESSON_KEYWORDS = ["1-2-1", "2-2-1"]


def _infer_teacher(class_name: str) -> str:
    name = class_name.lower()
    if "jordan" in name or "jord" in name or "rookie" in name:
        return "Teacher A"
    if "aimee" in name:
        return "Teacher B"
    if "natalie" in name or "nat " in name:
        return "Teacher C"
    if "abner" in name:
        return "Teacher D"
    if "carlos" in name or "lola" in name:
        return "Teacher E"
    if (
        "mike" in name
        or "duckling 3" in name
        or "pre school" in name
        or "adult & baby" in name
        or "adult & toddler" in name
        or "bronze & silver" in name
        or "gold & honours" in name
    ):
        return "Teacher F"
    if "heather" in name or "sen" in name:
        return "Teacher H"
    if "caira" in name:
        return "Teacher I"
    if "jade" in name:
        return "Teacher J"
    if "stuart" in name:
        return "Teacher G"
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
    df["teacher"] = df["Class Name"].apply(_infer_teacher)
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
