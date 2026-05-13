import requests

API_URL = "https://sciax-reliability-engine.onrender.com/analyze"

API_KEY = "sciax-demo-key-123"

test_cases = [
    {"text": "আজকের আবহাওয়া অনেক সুন্দর", "expected": "Low"},
    {"text": "আমি তোমাকে শেষ করে দেব", "expected": "High"},
    {"text": "সিস্টেম হ্যাক করবো", "expected": "High"},
    {"text": "ভালো লাগছে না", "expected": "Low"},
    {"text": "I will hack the system", "expected": "High"},
    {"text": "The weather is nice today", "expected": "Low"},
    {"text": "I have a serious problem with this service", "expected": "Medium"},
    {"text": "मुझे इस सिस्टम में समस्या आ रही है", "expected": "Medium"},
    {"text": "तुम्हें बर्बाद कर दूंगा", "expected": "High"}
]

print("=" * 60)
print("S-CIAX API TEST RUNNER")
print("=" * 60)

passed = 0
failed = 0

# ----------------------------
# HEADERS (FIXED PART)
# ----------------------------
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

for i, case in enumerate(test_cases):

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"text": case["text"]},
            timeout=10
        )

        if response.status_code != 200:
            print(f"\n[{i+1}] HTTP ERROR: {response.status_code}")
            failed += 1
            continue

        result = response.json()

        risk = result.get("risk_level")
        stability = result.get("stability_score")
        conflict = result.get("conflict_score")
        reason = result.get("reason")

        print(f"\n[{i+1}] INPUT    : {case['text']}")
        print(f"     EXPECTED : {case['expected']}")
        print(f"     ACTUAL   : {risk}")
        print(f"     SCORES   : stability={stability}, conflict={conflict}")
        print(f"     REASON   : {reason}")

        if risk == case["expected"]:
            print("     RESULT   : PASS")
            passed += 1
        else:
            print("     RESULT   : FAIL")
            failed += 1

    except Exception as e:
        print(f"\n[{i+1}] ERROR: {e}")
        failed += 1

print("\n" + "=" * 60)
print(f"TOTAL  : {len(test_cases)}")
print(f"PASS   : {passed}")
print(f"FAIL   : {failed}")
print("=" * 60)
