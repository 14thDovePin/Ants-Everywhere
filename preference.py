"""Game preference."""

class GameSettings:  # ++++++++++++++++++++++++++++++++ GAME SETTINGS ++++++++++++++++++++++++++++++++
    """Main class to modify presets of the game."""

    # ================================ MAIN GAME SETTINGS ================================
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.game_window_caption = "Ants Everywhere!"
        self.target_fps = 60

        self.bg_color = (0, 51, 153)
        self.bg_color = (77, 77, 77)


class Stats:  # ++++++++++++++++++++++++++++++++ GAME STATISTICS ++++++++++++++++++++++++++++++++
    """Main class to define, modify, track, and record in game statistics."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset()
        self.GAME_ACTIVE = True  # Game status flag. 

    def reset(self):
        """Initialize game stats for game. Can also be called to reset game stats to presets in the settings."""
        # Insert game statistical values here. ################
        pass
