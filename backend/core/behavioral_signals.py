# ==================================================
# S-CIAX BEHAVIORAL SIGNAL ENGINE
# ==================================================

def detect_behavioral_signals(text):

    text = text.lower().strip()

    signals = []

    # --------------------------------------------------
    # TARGET-DIRECTED HOSTILITY
    # --------------------------------------------------

    if any(p in text for p in [

        "dekhe nibo",
        "toke",
        "tomake",
        "tujhe",
        "you"

    ]):

        signals.append(
            "target-directed aggression"
        )

    # --------------------------------------------------
    # IMPLICIT THREAT ESCALATION
    # --------------------------------------------------

    if any(p in text for p in [

        "dekhe nibo",
        "shesh kore dibo",
        "shesh kore debo",
        "khatam kar dunga",

        "শেষ করে দিব",
        "শেষ করে দেব"

    ]):

        signals.append(
            "implicit threat escalation"
        )

    # --------------------------------------------------
    # DIRECT VIOLENT AGGRESSION
    # --------------------------------------------------

    if any(p in text for p in [

        "kill",
        "murder",
        "mar dunga",
        "maar dunga",

        "mere felbo",
        "khun korbo",

        "মেরে ফেলবো",
        "খুন করবো"

    ]):

        signals.append(
            "violent aggression"
        )

    # --------------------------------------------------
    # FIRST-PERSON THREAT LANGUAGE
    # --------------------------------------------------

    if any(p in text for p in [

        "ami",
        "i will",
        "mar dunga",
        "mere felbo",
        "shesh kore dibo"

    ]):

        signals.append(
            "first-person threat language"
        )

    # --------------------------------------------------
    # CYBER INTRUSION
    # --------------------------------------------------

    if any(p in text for p in [

        "hack the system",
        "bypass security",
        "exploit vulnerability",
        "steal data",

        "system hack korbo",
        "data churi korbo"

    ]):

        signals.append(
            "cyber intrusion intent"
        )

    # --------------------------------------------------
    # SAFE / BENIGN CONTEXT
    # --------------------------------------------------

    if any(p in text for p in [

        "hack my sleep schedule",
        "study hack",
        "life hack",
        "productivity hack"

    ]):

        signals.append(
            "benign optimization context"
        )

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    signals = list(set(signals))

    return signals
