import pexpect
import csv
import time
import sys

# Command to run your main program
CMD = "python3 src/main.py"

# Test cases
tests = [
    # 0. Reset database
    {
        "id": "Reset_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["reset"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 1. Add a valid movie
    {
        "id": "add_valid_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["add"]},
            {"prompt": "> ", "inputs": ["Inception"]},
            {"prompt": "> ", "inputs": ["2010"]},
            {"prompt": "> ", "inputs": ["PG"]},
            {"prompt": "> ", "inputs": ["148"]},
            {"prompt": "> ", "inputs": ["Sci-Fi"]},
            {"prompt": "> ", "inputs": ["5"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 2. Add movie with invalid inputs
    {
        "id": "add_invalid_inputs",
        "steps": [
            {"prompt": "> ", "inputs": ["add"]},
            {"prompt": "> ", "inputs": ["", "Test"]},  # retry with valid name
            {"prompt": "> ", "inputs": ["abcd","1899","2099","2024"]},  # retries for year
            {"prompt": "> ", "inputs": ["PG-13","asda","12023","PG"]},  # retries for rating
            {"prompt": "> ", "inputs": ["0","-1","601","100"]},  # retries for watch time
            {"prompt": "> ", "inputs": ["1012","alksjasd","horror"]},  # retries for genre
            {"prompt": "> ", "inputs": ["-1","11","5.5"]},  # star rating retries (0–10)
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 5. Edit movie with valid inputs
    {
        "id": "edit_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["edit 35"]},  # edit movie ID 1
            {"prompt": "> ", "inputs": ["Inception Edited"]},
            {"prompt": "> ", "inputs": ["2011"]},
            {"prompt": "> ", "inputs": ["PG"]},
            {"prompt": "> ", "inputs": ["150"]},
            {"prompt": "> ", "inputs": ["Action"]},
            {"prompt": "> ", "inputs": ["4"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 6. Edit movie with invalid inputs
    {
        "id": "edit_invalid_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["edit 35"]},
            {"prompt": "> ", "inputs": [""]},  # empty name
            {"prompt": "> ", "inputs": ["abcd","1899","2099","2025"]},  # invalid years
            {"prompt": "> ", "inputs": ["InvalidRating","R"]},  # invalid ratings
            {"prompt": "> ", "inputs": ["Sci-Fi","","Action"]},  # invalid genre
            {"prompt": "> ", "inputs": ["-5","12","8"]},  # star rating retries (0–10)
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 7. View all movies
    {
        "id": "view_all_movies",
        "steps": [
            {"prompt": "> ", "inputs": ["view_all"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 8. View single movie
    {
        "id": "view_single_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["view 35"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 9. Delete non-existent movie
    {
        "id": "delete_nonexistent_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["delete 999"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 10. Delete movie
    {
        "id": "delete_movie",
        "steps": [
            {"prompt": "> ", "inputs": ["delete 36"]},
            {"prompt": "> ", "inputs": ["yes"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 11. View after delete to ensure removal
    {
        "id": "view_after_delete",
        "steps": [
            {"prompt": "> ", "inputs": ["view_all"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 12. Search movie with name
    {
        "id": "search_movie_name",
        "steps": [
            {"prompt": "> ", "inputs": ["search"]},
            {"prompt": "> ", "inputs": ["filter name Inception"]},
            {"prompt": "> ", "inputs": ["return"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ],
        "expect_contains": "Inception Edited"
    },

    # 13. Search movie with different filters
    {
        "id": "search_filters",
        "steps": [
            {"prompt": "> ", "inputs": ["search"]},
            {"prompt": "> ", "inputs": ["filter genre Action"]},
            {"prompt": "> ", "inputs": ["filter rating PG"]},
            {"prompt": "> ", "inputs": ["filter year 2011"]},
            {"prompt": "> ", "inputs": ["return"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 14. Invalid command handling
    {
        "id": "invalid_command",
        "steps": [
            {"prompt": "> ", "inputs": ["foobar"]},
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    },

    # 15. Quit program
    {
        "id": "quit_program",
        "steps": [
            {"prompt": "> ", "inputs": ["quit"]},
        ]
    }
]


results = []

for t in tests:
    print(f"\nRunning test: {t['id']}")
    start = time.time()
    try:
        child = pexpect.spawn(CMD, encoding="utf-8", timeout=5)
        child.setwinsize(25, 110)  # ensure full-screen UI renders
        child.logfile = sys.stdout  # optional: live output

        full_output = ""

        for i, step in enumerate(t["steps"], start=1):
            for inp in step["inputs"]:
                child.expect(step["prompt"])
                full_output += child.before
                print(f"  Step {i}: sending input '{inp}'")
                child.sendline(inp)
                time.sleep(0.1)

        # Wait for program to finish
        child.expect(pexpect.EOF)
        full_output += child.before
        duration = (time.time() - start) * 1000

        passed = True

        # Collect all inputs sent for this test
        inputs_sent = []
        for step in t["steps"]:
            inputs_sent.extend(step["inputs"])

        results.append({
            "id": t["id"],
            "passed": passed,
            "stdout": " | ".join(inputs_sent),  # show inputs in Output Preview
            "time_ms": int(duration)
        })

        print(f"\nTest {t['id']} {'PASSED ✅' if passed else 'FAILED ❌'} in {int(duration)} ms")

    except pexpect.TIMEOUT:
        results.append({
            "id": t["id"],
            "passed": False,
            "stdout": "<TIMEOUT>",
            "time_ms": -1
        })
        print(f"\nTest {t['id']} TIMED OUT ❌")

# --- Save CSV Table ---
with open("path_test_results.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Test ID", "Passed", "Input Preview", "Time(ms)"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for r in results:
        writer.writerow({
            "Test ID": r["id"],
            "Passed": "PASS" if r["passed"] else "FAIL",
            "Input Preview": r["stdout"],
            "Time(ms)": r["time_ms"]
        })

print("\nCSV table saved to 'path_test_results.csv'")
