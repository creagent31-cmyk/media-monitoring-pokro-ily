import os


PROJECTS = [

    "Cresco Real Estate",
    "Cresco Group",
    "SO-HO Residence",
    "SO-HO Rezidencie",
    "Slnečnice Bratislava",
    "River Park Bratislava",
    "Yards Žižkov"

]


MAX_DAYS = 2


EMAIL_TO = [

    "jindra@cresco.cz",
    "petrjindr31@gmail.com"

]


OPENAI_KEY = os.getenv(
    "OPENAI_API_KEY"
)


EMAIL_USER = os.getenv(
    "EMAIL_USER"
)


EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)
