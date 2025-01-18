from kivy.utils import get_color_from_hex

# Theme Colors - Main application colors
THEME_BACKGROUND_DARK = get_color_from_hex("#1E1E1E")    # Dark background for main app
BACKGROUND_LIGHT = get_color_from_hex("#2A2A2A")   # Light background for neutral buttons

# Action Button Colors
# BUTTON_BLUE = get_color_from_hex("#4A90E2")      # Blue for primary actions (edit, select)
BUTTON_GREEN = get_color_from_hex("#5CB85C")    # Green for positive actions (add, save)
BUTTON_RED = get_color_from_hex("#D9534F")      # Red for negative actions (delete, exit)
BUTTON_ORANGE = get_color_from_hex("#F0AD4E")    # Orange for warning actions (cancel)
BUTTON_LIGHT_BLUE = get_color_from_hex("#5BC0DE")   # Light blue for info actions

# Text Colors
TEXT_WHITE = get_color_from_hex("#FFFFFF")         # Primary white text
TEXT_GRAY = get_color_from_hex("#CCCCCC")         # Secondary gray text 