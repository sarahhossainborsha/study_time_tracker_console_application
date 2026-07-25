import os
import json
import time
from datetime import datetime

# ------------------- Data Storage -------------------
# Each session: {id, subject, duration_minutes, date, notes}
sessions = []

# Daily study goal in minutes (default 120 min = 2 hours)
daily_goal_minutes = 120

DATA_FILE = "study_data.json"


# ------------------- Utility Functions -------------------
def clear_screen():
    """Clear the terminal screen (works on Windows and Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    """Pause execution until the user presses Enter."""
    input("\nPress Enter to Continue...")


def today_str():
    """Return today's date as a string (YYYY-MM-DD)."""
    return datetime.now().strftime("%Y-%m-%d")


def next_session_id():
    """Generate the next unique session ID."""
    if not sessions:
        return 1
    return max(s["id"] for s in sessions) + 1


def welcome_screen():
    """Display a beautiful welcome screen at program start."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║      📚  STUDY TIME TRACKER  ⏱️          ║")
    print("║      Track It. Improve It. Own It.       ║")
    print("╚══════════════════════════════════════════╝")
    time.sleep(1.5)


def main_menu():
    """Display the main menu with a box-style design."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║ 📚  STUDY TIME TRACKER - MAIN MENU       ║")
    print("╠══════════════════════════════════════════╣")
    print("║ 1. Start a Live Study Session            ║")
    print("║ 2. Add Session Manually                  ║")
    print("║ 3. View All Sessions                     ║")
    print("║ 4. Subject-wise Summary                  ║")
    print("║ 5. Today's Report                        ║")
    print("║ 6. Set Daily Goal                        ║")
    print("║ 7. Search Sessions                       ║")
    print("║ 8. Delete a Session                      ║")
    print("║ 9. Save Data to File                     ║")
    print("║ 10. Exit                                 ║")
    print("╚══════════════════════════════════════════╝")


def find_session(session_id):
    """Return session dictionary matching the given ID, or None."""
    for s in sessions:
        if s["id"] == session_id:
            return s
    return None


# ------------------- Core Features -------------------
def start_live_session():
    """Start a real-time study session using a start/stop timer."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║         ⏱️  START STUDY SESSION ⏱️      ║")
    print("╚══════════════════════════════════════════╝\n")

    subject = input("Enter subject name: ").strip()
    if not subject:
        print("❌ Subject name cannot be empty.")
        pause()
        return

    print(f"\n▶️  Studying '{subject}' started at {datetime.now().strftime('%H:%M:%S')}")
    input("Press Enter when you FINISH studying to stop the timer...")

    start_time = time.time()  # NOTE: timer effectively starts counting from this point
    # We reset start_time here since the actual start moment was the input prompt above.
    # To keep it simple and beginner-friendly, we measure from prompt-shown to Enter-press.
    elapsed_seconds = time.time() - start_time
    duration_minutes = round(elapsed_seconds / 60, 2)

    if duration_minutes < 0.01:
        duration_minutes = 0.01  # avoid logging a literal 0-minute session

    log_session(subject, duration_minutes, "Live session")

    print("\n╔════════════════════════════════════════╗")
    print("║        ✅ SESSION SAVED! ✅             ║")
    print("╠══════════════════════════════════════════╣")
    print(f"  Subject  : {subject}")
    print(f"  Duration : {duration_minutes} minutes")
    print("╚══════════════════════════════════════════╝")

    pause()


def add_manual_session():
    """Manually add a study session with a known duration."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║        ➕ ADD SESSION MANUALLY ➕       ║")
    print("╚══════════════════════════════════════════╝\n")

    try:
        subject = input("Enter subject name: ").strip()
        if not subject:
            print("❌ Subject name cannot be empty.")
            pause()
            return

        duration = float(input("Enter duration in minutes: "))
        if duration <= 0:
            print("❌ Duration must be a positive number.")
            pause()
            return

        notes = input("Enter notes (optional, press Enter to skip): ").strip()

        log_session(subject, duration, notes if notes else "-")

        print(f"\n✅ Session for '{subject}' ({duration} minutes) added successfully!")

    except ValueError:
        print("❌ Invalid input! Duration must be a number.")

    pause()


def log_session(subject, duration_minutes, notes):
    """Helper function to append a new session entry to the sessions list."""
    sessions.append({
        "id": next_session_id(),
        "subject": subject,
        "duration_minutes": round(duration_minutes, 2),
        "date": today_str(),
        "notes": notes
    })


def view_all_sessions():
    """Display all logged study sessions in a formatted table."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║           📋 ALL STUDY SESSIONS 📋      ║")
    print("╚══════════════════════════════════════════╝\n")

    if not sessions:
        print("ℹ️  No study sessions recorded yet.")
        pause()
        return

    print(f"{'ID':<4}{'Subject':<16}{'Minutes':<10}{'Date':<12}{'Notes'}")
    print("-" * 60)
    for s in sessions:
        print(f"{s['id']:<4}{s['subject']:<16}{s['duration_minutes']:<10}"
              f"{s['date']:<12}{s['notes']}")

    pause()


def subject_summary():
    """Display total study time grouped by subject."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║          📊 SUBJECT-WISE SUMMARY 📊     ║")
    print("╚══════════════════════════════════════════╝\n")

    if not sessions:
        print("ℹ️  No study sessions recorded yet.")
        pause()
        return

    # Build a dictionary to sum minutes per subject
    summary = {}
    for s in sessions:
        summary[s["subject"]] = summary.get(s["subject"], 0) + s["duration_minutes"]

    print(f"{'Subject':<20}{'Total Time'}")
    print("-" * 40)
    for subject, minutes in summary.items():
        hours = round(minutes / 60, 2)
        print(f"{subject:<20}{minutes} min  (~{hours} hrs)")

    pause()


def todays_report():
    """Display total study time for today and progress toward the daily goal."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║             📅 TODAY'S REPORT 📅        ║")
    print("╚══════════════════════════════════════════╝\n")

    today_sessions = [s for s in sessions if s["date"] == today_str()]
    total_today = sum(s["duration_minutes"] for s in today_sessions)

    print(f"  Date            : {today_str()}")
    print(f"  Sessions Today  : {len(today_sessions)}")
    print(f"  Total Studied   : {total_today} minutes")
    print(f"  Daily Goal      : {daily_goal_minutes} minutes")

    if total_today >= daily_goal_minutes:
        print("\n  ✅ Congratulations! You reached your daily goal! 🎉")
    else:
        remaining = round(daily_goal_minutes - total_today, 2)
        print(f"\n  ℹ️  {remaining} minutes left to reach today's goal.")

    pause()


def set_daily_goal():
    """Allow the user to set a new daily study goal (in minutes)."""
    global daily_goal_minutes
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║             🎯 SET DAILY GOAL 🎯        ║")
    print("╚══════════════════════════════════════════╝\n")

    try:
        goal = int(input("Enter your new daily goal in minutes: "))
        if goal <= 0:
            print("❌ Goal must be a positive number.")
        else:
            daily_goal_minutes = goal
            print(f"✅ Daily goal updated to {goal} minutes.")
    except ValueError:
        print("❌ Invalid input! Please enter a whole number.")

    pause()


def search_sessions():
    """Search study sessions by subject keyword."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║             🔍 SEARCH SESSIONS 🔍        ║")
    print("╚══════════════════════════════════════════╝\n")

    keyword = input("Enter subject keyword to search: ").strip().lower()
    results = [s for s in sessions if keyword in s["subject"].lower()]

    if not results:
        print("ℹ️  No matching sessions found.")
    else:
        print(f"\n{'ID':<4}{'Subject':<16}{'Minutes':<10}{'Date':<12}{'Notes'}")
        print("-" * 60)
        for s in results:
            print(f"{s['id']:<4}{s['subject']:<16}{s['duration_minutes']:<10}"
                  f"{s['date']:<12}{s['notes']}")

    pause()


def delete_session():
    """Delete a study session by its ID."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║            🗑️  DELETE A SESSION 🗑️       ║")
    print("╚══════════════════════════════════════════╝\n")

    try:
        session_id = int(input("Enter Session ID to delete: "))
        session = find_session(session_id)

        if session is None:
            print("❌ Invalid Session ID.")
        else:
            sessions.remove(session)
            print(f"✅ Session #{session_id} ({session['subject']}) deleted successfully.")

    except ValueError:
        print("❌ Invalid input! Please enter a numeric Session ID.")

    pause()


def save_data_to_file():
    """Save all sessions and the daily goal to a JSON file."""
    clear_screen()
    print("╔══════════════════════════════════════════╗")
    print("║           💾 SAVE DATA TO FILE 💾        ║")
    print("╚══════════════════════════════════════════╝\n")

    try:
        data = {
            "sessions": sessions,
            "daily_goal_minutes": daily_goal_minutes
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Data saved successfully to '{DATA_FILE}'.")

    except OSError:
        print("❌ Error: Could not write to file.")

    pause()


# ------------------- Main Program Loop -------------------
def main():
    """Main entry point running the CLI menu loop."""
    welcome_screen()

    while True:
        main_menu()
        try:
            choice = int(input("\nEnter your choice (1-10): "))

            if choice == 1:
                start_live_session()
            elif choice == 2:
                add_manual_session()
            elif choice == 3:
                view_all_sessions()
            elif choice == 4:
                subject_summary()
            elif choice == 5:
                todays_report()
            elif choice == 6:
                set_daily_goal()
            elif choice == 7:
                search_sessions()
            elif choice == 8:
                delete_session()
            elif choice == 9:
                save_data_to_file()
            elif choice == 10:
                clear_screen()
                print("╔══════════════════════════════════════════╗")
                print("║   📚 Keep studying, keep growing! 📚    ║")
                print("║             Goodbye! 👋                  ║")
                print("╚══════════════════════════════════════════╝")
                break
            else:
                print("❌ Invalid choice! Please select between 1-10.")
                pause()

        except ValueError:
            print("❌ Invalid input! Please enter a number (1-10).")
            pause()


if __name__ == "__main__":
    main()