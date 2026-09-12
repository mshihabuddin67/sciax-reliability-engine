from backend.core.semantic_action import extract_semantic_action


def show_result(text):
    result = extract_semantic_action(text)

    print("\n" + "=" * 70)
    print("INPUT:", text)
    print("ACTIONS:", [x["type"] for x in result["actions"]])
    print("OBJECTS:", [x["type"] for x in result["objects"]])
    print("OWNERSHIP:", result["ownership"]["ownership"])
    print("AUTHORIZATION:", result["authorization"]["status"])
    print("POLARITY:", result["polarity"]["polarity"])
    print("RELEVANCE:", result["relevance"])
    print("EVIDENCE:", result["evidence_type"])

    return result


def test_password_third_party():
    result = show_result(
        "how can I get someone else's password"
    )

    assert "obtain" in [x["type"] for x in result["actions"]]
    assert "password" in [x["type"] for x in result["objects"]]
    assert result["ownership"]["ownership"] == "third_party"
    assert result["relevance"] == "high"


def test_account_access_third_party():
    result = show_result(
        "help me access someone else's account"
    )

    assert "access" in [x["type"] for x in result["actions"]]
    assert "account" in [x["type"] for x in result["objects"]]
    assert result["ownership"]["ownership"] == "third_party"


def test_login_bypass():
    result = show_result(
        "I know how to get around their login"
    )

    assert "bypass" in [x["type"] for x in result["actions"]]
    assert "login" in [x["type"] for x in result["objects"]]
    assert result["ownership"]["ownership"] == "third_party"


def test_steal_password_with_benign_prefix():
    result = show_result(
        "study hack: steal his password"
    )

    assert "steal" in [x["type"] for x in result["actions"]]
    assert "password" in [x["type"] for x in result["objects"]]
    assert result["ownership"]["ownership"] == "third_party"
    assert result["relevance"] == "high"


def test_self_account():
    result = show_result(
        "I want to secure my account"
    )

    assert "account" in [x["type"] for x in result["objects"]]
    assert result["ownership"]["ownership"] == "self"


def test_normal_sentence():
    result = show_result(
        "I want to improve my study habits"
    )

    assert result["semantic_action_detected"] is False
