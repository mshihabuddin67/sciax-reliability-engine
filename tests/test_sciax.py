import requests

API_URL = "https://sciax-reliability-engine.onrender.com/analyze"

API_KEY = "sciax-demo-key-123"

test_cases = [

    # ==================================================
    # LOW RISK TESTS
    # ==================================================

    {
        "text": "আজকের আবহাওয়া অনেক সুন্দর",
        "expected": "Low"
    },

    {
        "text": "The weather is nice today",
        "expected": "Low"
    },

    {
        "text": "आज मौसम बहुत अच्छा है",
        "expected": "Low"
    },

    {
        "text": "আমি নতুন একটি প্রজেক্ট বানাচ্ছি",
        "expected": "Low"
    },

    # ==================================================
    # MEDIUM RISK TESTS
    # ==================================================

    {
        "text": "I have a serious problem with this service",
        "expected": "Medium"
    },

    {
        "text": "This platform is broken",
        "expected": "Medium"
    },

    {
        "text": "আমি অভিযোগ করতে চাই",
        "expected": "Medium"
    },

    {
        "text": "আমার অনেক সমস্যা হচ্ছে",
        "expected": "Medium"
    },

    {
        "text": "मुझे इस सिस्टम में समस्या आ रही है",
        "expected": "Medium"
    },

    # ==================================================
    # HIGH RISK TESTS
    # ==================================================

    {
        "text": "I will hack the system",
        "expected": "High"
    },

    {
        "text": "I want to destroy everything",
        "expected": "High"
    },

    {
        "text": "সিস্টেম হ্যাক করবো",
        "expected": "High"
    },

    {
        "text": "আমি তোমাকে শেষ করে দেব",
        "expected": "High"
    },

    {
        "text": "তোমার বাড়ি জ্বালিয়ে দেব",
        "expected": "High"
    },

    {
        "text": "मैं सिस्टम तोड़ दूंगा",
        "expected": "High"
    },

    {
        "text": "तुम्हें बर्बाद कर दूंगा",
        "expected": "High"
    },

    {
        "text": "सिस्टम में घुसना है",
        "expected": "High"
    },

    # ==================================================
    # EDGE CASE TESTS
    # ==================================================

    {
        "text": "I want to hack my sleep schedule",
        "expected": "High"
    },

    {
        "text": "আমি একটু রেগে আছি",
        "expected": "Low"
    }
]

print("=" * 70)
print("S-CIAX MULTILINGUAL API TEST SUITE")
print("=" * 70)

passed = 0
failed = 0

for i, case in enumerate(test_cases):

    try:

        response = requests.post(

            API_URL,

            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY
            },

            json={
                "text": case["text"]
            },

            timeout=10
        )

        if response.status_code != 200:

            print(
                f"\n[{i+1}] HTTP ERROR "
                f"{response.status_code}"
            )

            failed += 1

            continue

        result = response.json()

        risk = result.get("risk_level")

        stability = result.get("stability_score")

        conflict = result.get("conflict_score")

        reason = result.get("reason")

        print(f"\n[{i+1}] INPUT      : {case['text']}")

        print(f"     EXPECTED   : {case['expected']}")

        print(f"     ACTUAL     : {risk}")

        print(
            f"     SCORES     : "
            f"stability={stability}, "
            f"conflict={conflict}"
        )

        print(f"     REASON     : {reason}")

        # ==================================================
        # RESULT CHECK
        # ==================================================

        if case["expected"] == risk:

            print("     TEST RESULT: PASS")

            passed += 1

        else:

            print("     TEST RESULT: FAIL")

            failed += 1

    except Exception as e:

        print(f"\n[{i+1}] EXCEPTION: {e}")

        failed += 1

print("\n" + "=" * 70)

print(f"TOTAL TESTS : {len(test_cases)}")

print(f"PASSED      : {passed}")

print(f"FAILED      : {failed}")

accuracy = (passed / len(test_cases)) * 100

print(f"ACCURACY    : {round(accuracy, 2)}%")

print("=" * 70)
