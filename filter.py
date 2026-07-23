from config import (
    NEGATIVE_WORDS,
    POSITIVE_WORDS,
    PROJECTS
)


def _clean_str(val) -> str:
    """Pomocná funkce: Převede hodnotu na řetězec bez ohledu na to, zda jde o dict nebo None."""
    if not val:
        return ""
    if isinstance(val, dict):
        return str(val.get("title") or val.get("value") or "")
    return str(val)


# =====================================================
# KONTROLA RELEVANCE
# =====================================================

def is_relevant(article):
    """
    Vrátí True, pokud článek pravděpodobně souvisí
    se sledovanými projekty.
    """
    title = _clean_str(article.get("title", ""))
    source = _clean_str(article.get("source", ""))

    text = f"{title} {source}".lower()

    for project in PROJECTS:
        if project.lower() in text:
            return True

    return False


# =====================================================
# SENTIMENT
# =====================================================

def analyze_sentiment(article):
    """
    Jednoduchá analýza nálady článku
    """
    text = _clean_str(article.get("title", "")).lower()

    positive = 0
    negative = 0

    for word in POSITIVE_WORDS:
        if word.lower() in text:
            positive += 1

    for word in NEGATIVE_WORDS:
        if word.lower() in text:
            negative += 1

    if negative > positive:
        return "🔴 Negativní"
    elif positive > negative:
        return "🟢 Pozitivní"
    else:
        return "🟡 Neutrální"


# =====================================================
# DŮLEŽITOST
# =====================================================

def calculate_importance(article):
    """
    Určuje prioritu 1-5
    """
    score = 1
    title = _clean_str(article.get("title", "")).lower()

    # Pokud je přímo v titulku Cresco
    if "cresco" in title:
        score += 2

    # Negativní témata mají vyšší prioritu
    for word in NEGATIVE_WORDS:
        if word.lower() in title:
            score += 2
            break

    # Pozitivní významná témata
    for word in POSITIVE_WORDS:
        if word.lower() in title:
            score += 1
            break

    if score > 5:
        score = 5

    return score


# =====================================================
# HLAVNÍ FILTR
# =====================================================

def process_articles(articles):
    """
    Vstup:
    seznam článků

    Výstup:
    pouze relevantní články s hodnocením a garancí existujících klíčů
    """
    result = []

    for article in articles:
        if not is_relevant(article):
            continue

        # Zabezpečení, že povinné klíče budou vždy přítomny jako text
        article["title"] = _clean_str(article.get("title", ""))
        article["summary"] = _clean_str(article.get("summary") or article.get("description") or "")
        article["link"] = str(article.get("link", ""))

        article["sentiment"] = analyze_sentiment(article)
        article["importance"] = calculate_importance(article)

        result.append(article)

    return result
