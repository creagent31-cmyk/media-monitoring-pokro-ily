from dataclasses import dataclass


@dataclass
class Article:

    title: str
    link: str
    source: str
    date: str

    summary: str = ""
    sentiment: str = ""
    relevance: int = 0
