from config import (
    NEGATIVE_WORDS,
    POSITIVE_WORDS,
    PROJECTS
)


def _clean_str(val) -> str:
    if not val:
        return ""
    if isinstance(val, dict):
        return str(val.get("title") or val.get("value") or "")
    return str(val)


def is_relevant(article):
    """
    Zkontroluje, zda se jakýkoliv ze sledovaných projektů (např. Cresco)
    nachází v nadpisu, zdroji nebo kdekoliv v těle článku.
    """
    title = _clean_str(article.get("title", ""))
    source = _clean_str(article.get("source", ""))
    summary = _clean_str(article.get("summary") or article.get("description") or "")

    full_search_text = f"{title} {source} {summary}".lower()

    for project in PROJECTS:
        if project.lower() in full_search_text:
            return True

    return False


def analyze_sentiment(article):
    title = _clean_str(article.get("title", ""))
    summary = _clean_str(article.get("summary") or article.get("description") or "")
    text = f"{title} {summary}".lower()

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


def calculate_importance(article):
    score = 1
    title = _clean_str(article.get("title", "")).lower()

    if "cresco" in title:
        score += 2

    for word in NEGATIVE_WORDS:
        if word.lower() in title:
            score += 2
            break

    for word in POSITIVE_WORDS:
        if word.lower() in title:
            score += 1
            break

    return min(score, 5)


def process_articles(articles):
    result = []
    seen_links = set()

    for article in articles:
        link = str(article.get("link", ""))
        
        # Ochrana proti duplicitám
        if link in seen_links:
            continue

        if not is_relevant(article):
            continue

        seen_links.add(link)

        article["title"] = _clean_str(article.get("title", ""))
        article["summary"] = _clean_str(article.get("summary") or article.get("description", ""))
        article["link"] = link
        article["sentiment"] = analyze_sentiment(article)
        article["importance"] = calculate_importance(article)

        result.append(article)

    return result
