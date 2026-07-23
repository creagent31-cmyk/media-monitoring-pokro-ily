import os


# =====================================================
# SLEDOVANÉ PROJEKTY A FIRMY
# =====================================================

PROJECTS = [

    "Cresco Real Estate",
    "Cresco Group",

    "SO-HO Residence",
    "SO-HO Rezidencie",

    "Slnečnice Bratislava",
    "Rezidencia Slnečnice",

    "River Park Bratislava",

    "Yards Žižkov"

]


# =====================================================
# KONKURENCE (pro budoucí rozšíření)
# =====================================================

COMPETITORS = [

    "Central Group",
    "Skanska Reality",
    "Penta Real Estate",
    "Crestyl",
    "Finep",
    "Sekyra Group",
    "YIT"

]


# =====================================================
# JAK STARÉ ČLÁNKY HLEDAT
# =====================================================

MAX_DAYS = 2


# =====================================================
# KAM CHODÍ REPORTY
# =====================================================

EMAIL_TO = [

    "jindra@cresco.cz",
    "petrjindr31@gmail.com"

]


# =====================================================
# ODESÍLACÍ GMAIL ÚČET
# (bere se z GitHub Secrets)
# =====================================================

EMAIL_USER = os.getenv(
    "EMAIL_USER"
)


EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)


# =====================================================
# BLACKLIST ZDROJŮ
# =====================================================

BLACKLIST_DOMAINS = [

    "vietnam.vn",

    "spam",

]


# =====================================================
# KLÍČOVÁ SLOVA PRO RIZIKOVÉ ČLÁNKY
# =====================================================

NEGATIVE_WORDS = [

    "žaloba",
    "spor",
    "pokuta",
    "kritika",
    "problém",
    "skandál",
    "zastaveno",
    "odpor",
    "petice",
    "kauza"

]


# =====================================================
# KLÍČOVÁ SLOVA PRO POZITIVNÍ ČLÁNKY
# =====================================================

POSITIVE_WORDS = [

    "ocenění",
    "zahájení",
    "výstavba",
    "kolaudace",
    "otevření",
    "úspěch",
    "prodej",
    "investice",
    "nový projekt"

]
