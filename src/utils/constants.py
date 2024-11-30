# Color schemes
PLATFORM_COLORS = {
    "PC": "#1f77b4",
    "Console": "#ff7f0e",
    "Mobile": "#2ca02c",
    "Other": "#7f7f7f",
}

ANXIETY_COLORS = {"low": "#2ecc71", "medium": "#f1c40f", "high": "#e74c3c"}

# Age group definitions
AGE_GROUPS = {
    "18-22": (18, 22),
    "22-26": (22, 26),
    "26-30": (26, 30),
    "30-35": (30, 35),
    "35+": (35, float("inf")),
}

# Score ranges
ANXIETY_RANGES = {"low": (0, 20), "medium": (21, 40), "high": (41, 100)}

# Chart configurations
CHART_HEIGHT = 600
MAP_HEIGHT = 500
RADAR_HEIGHT = 400

# Default values
DEFAULT_PLATFORM = "All"
DEFAULT_ANXIETY_TYPE = "general"
DEFAULT_AGE_RANGE = (18, 35)

# Column names mapping
COLUMN_NAMES = {
    "GAD_T": "General Anxiety Score",
    "SPIN_T": "Social Anxiety Score",
    "SWL_T": "Life Satisfaction Score",
    "Hours": "Gaming Hours per Week",
}

# Playstyle descriptions
PLAYSTYLE_DESCRIPTIONS = {
    "Singleplayer": "Solo gaming experience",
    "Multiplayer - Offline": "Local multiplayer with friends",
    "Multiplayer - Online (strangers)": "Online gaming with random players",
    "Multiplayer - Online (friends)": "Online gaming with friends",
    "Multiplayer - Online (both)": "Mixed online gaming",
}
