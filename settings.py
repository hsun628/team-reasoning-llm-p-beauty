from os import environ
from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent

# DEBUG MODE

debug = True
num_participant = 12   # 12 or 14 or 16

# -------------------
# SESSION CONFIGS
# -------------------
SESSION_CONFIGS = [
    dict(
        name = 'Experiment_team_reasoning_LLM',
        display_name = "team_reasoning_LLM",
        num_demo_participants = 4 if debug else num_participant,
        app_sequence = ['phase1', 'phase2', 'phase_AI', 'after_questionaire'],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    display_name = "team_reasoning_LLM_p_beauty",
    real_world_currency_per_point = 1.00,
    participation_fee = 150.00,
    doc="",
)

# -------------------
# LANGUAGE & CURRENCY
# -------------------
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = ''
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
USE_POINTS = False

# -------------------
# ADMIN
# -------------------
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

# optional HTML for demo page
DEMO_PAGE_INTRO_HTML = ""

# SECRET_KEY required by Django
SECRET_KEY = 'replace-with-a-random-string'

# -------------------
# INSTALLED APPS
# -------------------
INSTALLED_APPS = ['otree']
