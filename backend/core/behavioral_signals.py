# ==================================================
# S-CIAX BEHAVIORAL SIGNAL ENGINE
# ==================================================

from backend.patterns.registry import PATTERN_REGISTRY
from backend.core.contextual_safety import summarize_context


# ==================================================
# CONTEXT-AWARE HELPERS
# ==================================================

def _has_explicit_malicious_action(text):
    malicious_actions = [
        "steal data",
        "steal password",
        "steal credentials",
        "get password",
        "breach",
        "exploit",
        "bypass security",
        "use their password",
        "take their password",
        "capture password",
        "send otp",
        "steal otp",
        "hack the system",
        "system hack",
        "data churi",
        "password churi",
    ]

    return any(phrase in text for phrase in malicious_actions)


def _has_strong_defensive_context(text):
    try:
        context = summarize_context(text)
    except Exception:
        return False

    if not isinstance(context, dict):
        return False

    if not context.get("matched"):
        return False

    for evidence in context.get("evidence", []):
        if not isinstance(evidence, dict):
            continue

        if (
            evidence.get("context_type") == "defensive_security"
            and evidence.get("intent") == "non-malicious"
            and float(evidence.get("strength", 0.0)) >= 0.80
        ):
            return True

    return False


# ==================================================
# REGISTRY HELPERS
# ==================================================

def _extract_pattern_value(pattern):
    """
    Supports registry entries in common formats:

    1. "pattern text"

    2. {
        "pattern": "pattern text",
        ...
    }

    3. {
        "text": "pattern text",
        ...
    }
    """

    if isinstance(pattern, str):
        return pattern

    if isinstance(pattern, dict):
        value = pattern.get("pattern")

        if value is None:
            value = pattern.get("text")

        if isinstance(value, str):
            return value

    return None


def _registry_matches(text, patterns):
    """
    Return True if at least one registered pattern matches.

    Matching is intentionally conservative at this stage.
    Semantic/structural matching will be added later.
    """

    for pattern in patterns or []:

        pattern_text = _extract_pattern_value(pattern)

        if not pattern_text:
            continue

        pattern_text = pattern_text.lower().strip()

        if pattern_text and pattern_text in text:
            return True

    return False


def _add_registry_signal(
    text,
    signals,
    category,
    signal_name,
):
    """
    Connect one Pattern Registry category to a behavioral signal.

    Existing signals are preserved.
    Registry matches only add evidence.
    """

    patterns = PATTERN_REGISTRY.get(category, [])

    if _registry_matches(text, patterns):

        if signal_name not in signals:
            signals.append(signal_name)


# ==================================================
# MAIN SIGNAL DETECTOR
# ==================================================

def detect_behavioral_signals(text):

    if not isinstance(text, str):
        return []

    text = text.lower().strip()

    if not text:
        return []

    signals = []

    # --------------------------------------------------
    # TARGET-DIRECTED AGGRESSION
    # --------------------------------------------------

    if any(p in text for p in [

        "toke",
        "tomake",
        "tore",

        "tujhe",
        "tumhe",

        "kill you",
        "i will kill you",
        "destroy you"

    ]):

        signals.append("target-directed aggression")

    # --------------------------------------------------
    # IMPLICIT THREAT ESCALATION
    # --------------------------------------------------

    if any(p in text for p in [

        "dekhe nibo",

        "shesh kore dibo",
        "shesh kore debo",

        "khatam kar dunga",
        "dekh lunga",

        "শেষ করে দিব",
        "শেষ করে দেব"

    ]):

        signals.append("implicit threat escalation")

    # --------------------------------------------------
    # DIRECT VIOLENT AGGRESSION
    # --------------------------------------------------

    if any(p in text for p in [

        "kill you",
        "i will kill",
        "murder",
        "destroy you",

        "mar dunga",
        "maar dunga",
        "tujhe mar dunga",
        "tujhe maar dunga",

        "mere felbo",
        "khun korbo",

        "মেরে ফেলবো",
        "খুন করবো"

    ]):

        signals.append("violent aggression")

    # --------------------------------------------------
    # FIRST-PERSON THREAT LANGUAGE
    # --------------------------------------------------

    if any(p in text for p in [

        "ami",
        "i will",

        "mar dunga",
        "maar dunga",

        "mere felbo",

        "shesh kore dibo",
        "shesh kore debo"

    ]):

        signals.append("first-person threat language")

    # --------------------------------------------------
    # CYBER INTRUSION
    # --------------------------------------------------

    if any(p in text for p in [

        "hack the system",
        "bypass security",
        "exploit vulnerability",
        "steal data",
        "breach server",

        "system hack korbo",
        "data churi korbo"

    ]):

        signals.append("cyber intrusion intent")

    # --------------------------------------------------
    # SAFE / BENIGN CONTEXT
    # --------------------------------------------------

    if any(p in text for p in [

        "hack my sleep schedule",
        "study hack",
        "life hack",
        "productivity hack",
        "game strategy"

    ]):

        signals.append("benign optimization context")

    # --------------------------------------------------
    # FRAUD INTENT
    # --------------------------------------------------

    if any(p in text for p in [

        "otp dao",
        "send otp",
        "bank password",
        "credit card pin",
        "verification code"

    ]):

        signals.append("fraud intent")

    # --------------------------------------------------
    # SOCIAL ENGINEERING
    # --------------------------------------------------

    if any(p in text for p in [

        "pretend to be",
        "impersonate",
        "fake identity",
        "act as support",
        "pose as"

    ]):

        signals.append("social engineering")

    # --------------------------------------------------
    # CREDENTIAL THEFT
    # --------------------------------------------------

    defensive_context = _has_strong_defensive_context(text)
    explicit_malicious_action = _has_explicit_malicious_action(text)

    if any(p in text for p in [
        "steal password",
        "get password",
        "steal credentials",
        "login credentials",
        "account password",
    ]):
        if not (
            defensive_context
            and not explicit_malicious_action
        ):
            signals.append("credential theft")
            
    # --------------------------------------------------
    # HARASSMENT
    # --------------------------------------------------

    if any(p in text for p in [

        "harass",
        "bully",
        "keep bothering",
        "insult repeatedly",
        "target repeatedly"

    ]):

        signals.append("harassment")

    # --------------------------------------------------
    # COERCION
    # --------------------------------------------------

    if any(p in text for p in [

        "force you",
        "make you do",
        "threaten until",
        "pressure you",
        "compel you"

    ]):

        signals.append("coercion")

    # ==================================================
    # PATTERN REGISTRY INTEGRATION
    # ==================================================

    # --------------------------------------------------
    # VIOLENCE PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "violence",
        "violent aggression",
    )

    # --------------------------------------------------
    # CYBER PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "cyber",
        "cyber intrusion intent",
    )

    # --------------------------------------------------
    # FRAUD PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "fraud",
        "fraud intent",
    )

    # --------------------------------------------------
    # SOCIAL ENGINEERING PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "social_engineering",
        "social engineering",
    )

    # --------------------------------------------------
    # CONTEXTUAL THREAT PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "contextual_threats",
        "implicit threat escalation",
    )

    # --------------------------------------------------
    # CROSS-SCRIPT PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "cross_script",
        "cross-script behavioral pattern",
    )

    # --------------------------------------------------
    # OBFUSCATION PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "obfuscation",
        "obfuscation pattern",
    )

    # --------------------------------------------------
    # SARCASM PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "sarcasm",
        "sarcasm pattern",
    )

    # --------------------------------------------------
    # AMBIGUITY PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "ambiguity",
        "ambiguity pattern",
    )

    # --------------------------------------------------
    # MULTI-INTENT PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "multi_intent",
        "multi-intent pattern",
    )

    # --------------------------------------------------
    # BENIGN PATTERNS
    # --------------------------------------------------

    _add_registry_signal(
        text,
        signals,
        "benign",
        "benign optimization context",
    )

    # --------------------------------------------------
    # REMOVE DUPLICATES (KEEP ORDER)
    # --------------------------------------------------

    signals = list(dict.fromkeys(signals))

    return signals
