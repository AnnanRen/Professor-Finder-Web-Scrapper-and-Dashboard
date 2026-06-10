"""
Configuration for AdvisorScout.
Contains QS-ranked university lists, search keywords, and scraper settings.
"""

import os
import json

# ============================================================
# SEARCH KEYWORDS — Professors matching these will be collected
# ============================================================

DEFAULT_KEYWORDS = {
    "seismology": [
        "seismology", "earthquake", "seismic",
        "seismic signal processing", "repeating earthquake",
        "repeating signal", "seismic detection",
        "ocean bottom seismometer", "OBS", "OBST", "OBFN",
        "seismic tomography", "seismic imaging",
        "seismic inversion", "bayesian inversion",
        "transdimensional inversion", "rjMCMC",
        "reversible jump MCMC",
        "seismic interferometry", "ambient noise",
        "surface wave", "body wave",
        "earthquake location", "hypocenter",
        "phase picking", "P arrival", "S arrival",
        "seismic phase identification",
        "template matching", "matched filter",
        "cross-correlation", "signal detection",
    ],
    "geophysics": [
        "geophysics", "solid earth geophysics",
        "marine geophysics", "ocean bottom seismology",
        "crustal structure", "mantle structure",
        "subduction zone", "continental margin",
        "seafloor", "marine seismic",
        "South China Sea", "tectonics",
        "geodesy", "GPS geodesy", "InSAR",
    ],
    "signal_processing": [
        "signal processing", "time series analysis",
        "pattern recognition", "machine learning",
        "deep learning", "neural network",
        "convolutional neural network", "transformer",
        "attention mechanism", "autoencoder",
        "transfer learning", "self-supervised learning",
    ],
}

# Load keywords from local JSON if exists, otherwise use defaults
KEYWORDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keywords.json")

def load_keywords():
    if os.path.exists(KEYWORDS_FILE):
        try:
            with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_KEYWORDS
    return DEFAULT_KEYWORDS

SEARCH_KEYWORDS = load_keywords()

# ============================================================
# SCRAPER SETTINGS
# ============================================================

REQUEST_DELAY = 0.1
SCHOLAR_DELAY = 5.0
MAX_PUBLICATIONS = 5
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 5
ENABLE_SCHOLAR = True

# Minimum match score to include a professor in results
MIN_MATCH_SCORE = 1.0

# ============================================================
# SCHOLAR SEARCH QUERIES
# These are used for the primary Google Scholar keyword searches
# ============================================================

SCHOLAR_SEARCH_QUERIES = [
    "earthquake seismology",
    "seismic tomography",
    "marine geophysics",
    "ambient noise tomography",
    "ocean bottom seismometer",
    "seismic imaging",
    "subduction zone geophysics",
    "earthquake early warning",
    "seismic signal processing",
    "repeating earthquake detection",
    "crustal structure seismology",
    "geodesy InSAR earthquake",
]
