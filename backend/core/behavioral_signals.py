# ==================================================
# S-CIAX BEHAVIORAL SIGNAL ENGINE
# ==================================================

def detect_behavioral_signals(text):

    text = text.lower().strip()

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
        "dekh lunga",

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
        "maar dunga",

        "mere felbo",

        "shesh kore dibo",
        "shesh kore debo"

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
        "breach server",

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
        "productivity hack",
        "game strategy"

    ]):

        signals.append(
            "benign optimization context"
        )

    # --------------------------------------------------
    # REMOVE DUPLICATES (KEEP ORDER)
    # --------------------------------------------------

    signals = list(
        dict.fromkeys(signals)
    )

    return signals
