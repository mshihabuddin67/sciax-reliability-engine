import json
import time

REPORT_PATH = "backend/reports/benchmark_results.json"


def load_data():
    try:
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def show():
    while True:
        data = load_data()

        print("\n" + "=" * 60)
        print("      S-CIAX BENCHMARK LIVE REPORT")
        print("=" * 60)

        pass_count = 0
        fail_count = 0

        for item in data:
            status = item.get("status", "UNKNOWN")

            if status == "PASS":
                pass_count += 1
            else:
                fail_count += 1

            print(f"""
Input     : {item['input']}
Expected  : {item['expected']}
Predicted : {item['predicted']}
Status    : {status}
------------------------------
""")

        total = pass_count + fail_count

        print("\nSUMMARY:")
        print(f"Total : {total}")
        print(f"PASS  : {pass_count}")
        print(f"FAIL  : {fail_count}")

        if total > 0:
            print(f"Accuracy: {(pass_count/total)*100:.2f}%")

        print("\nRefreshing in 5 seconds...\n")

        time.sleep(5)


if __name__ == "__main__":
    show()
