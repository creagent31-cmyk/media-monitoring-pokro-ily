# =====================================================
# GENEROVÁNÍ REPORTU
# =====================================================

def create(articles):
    """
    Vytvoří HTML zprávu ze seznamu článků.
    """
    if not articles:
        return "<p>Žádné nové články k zobrazení.</p>"

    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; }
            .article { border-bottom: 1px solid #ccc; padding-bottom: 10px; margin-bottom: 15px; }
            .title { font-size: 18px; color: #1a0dab; text-decoration: none; font-weight: bold; }
            .meta { font-size: 13px; color: #555; margin-top: 4px; }
            .summary { color: #333; margin-top: 8px; }
        </style>
    </head>
    <body>
        <h2>📰 Media Monitor Report</h2>
    """

    for i in articles:
        title = i.get('title', 'Bez názvu')
        link = i.get('link', '#')
        summary = i.get('summary') or i.get('description', '')
        if isinstance(summary, dict):
            summary = summary.get('value', '')
        
        sentiment = i.get('sentiment', '🟡 Neutrální')
        importance = i.get('importance') or i.get('relevance', 1)

        html += f"""
        <div class="article">
            <a class="title" href="{link}" target="_blank">{title}</a>
            <div class="meta">
                <span>Sentiment: {sentiment}</span> | 
                <span>Priorita: {importance}/5</span>
            </div>
            <div class="summary">{summary}</div>
        </div>
        """

    html += """
    </body>
    </html>
    """

    return html
