"""Twinkle Treats Stake Engine Math SDK configuration (initial integration scaffold)."""
import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode

SYMBOLS = ("GEM", "BERRY", "BLUE", "LOLLI", "ORANGE", "HEART", "LEMON")
PAY_PER_SYMBOL = {
    "GEM": 0.05528, "BERRY": 0.06219, "BLUE": 0.06910,
    "LOLLI": 0.093285, "ORANGE": 0.10365, "HEART": 0.13129,
    "LEMON": 0.17275,
}

class GameConfig(Config):
    def __init__(self):
        super().__init__()
        self.game_id = "twinkle_treats"
        self.provider_number = 0  # Replace with assigned provider number in Studio.
        self.working_name = "Twinkle Treats"
        self.wincap = 25000.0
        self.win_type = "cluster"
        self.rtp = 0.965  # Target only; not calibrated or verified.
        self.construct_paths()

        self.num_reels = 6
        self.num_rows = [5] * self.num_reels
        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"]}
        self.freespin_triggers = {
            self.basegame_type: {3: 5, 4: 10, **{n: 15 for n in range(5, 31)}},
            self.freegame_type: {3: 5, 4: 10, **{n: 15 for n in range(5, 31)}},
        }
        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 2,
        }

        pay_group = {}
        for symbol in SYMBOLS:
            for size in range(5, 31):
                pay_group[((size, size), symbol)] = round(PAY_PER_SYMBOL[symbol] * size, 8)
        self.paytable = self.convert_range_table(pay_group)

        self.reels = {
            "BR0": self.read_reels_csv(os.path.join(self.reels_path, "BR0.csv")),
            "FR0": self.read_reels_csv(os.path.join(self.reels_path, "FR0.csv")),
        }
        distributions = [
            Distribution(
                criteria="wincap", quota=0.001, win_criteria=self.wincap,
                conditions={
                    "reel_weights": {self.basegame_type: {"BR0": 1}, self.freegame_type: {"FR0": 1}},
                    "scatter_triggers": {3: 1, 4: 1, 5: 1},
                    "force_wincap": True, "force_freegame": True,
                },
            ),
            Distribution(
                criteria="freegame", quota=0.10,
                conditions={
                    "reel_weights": {self.basegame_type: {"BR0": 1}, self.freegame_type: {"FR0": 1}},
                    "scatter_triggers": {3: 1, 4: 1, 5: 1},
                    "force_wincap": False, "force_freegame": True,
                },
            ),
            Distribution(
                criteria="0", quota=0.40, win_criteria=0.0,
                conditions={
                    "reel_weights": {self.basegame_type: {"BR0": 1}},
                    "force_wincap": False, "force_freegame": False,
                },
            ),
            Distribution(
                criteria="basegame", quota=0.499,
                conditions={
                    "reel_weights": {self.basegame_type: {"BR0": 1}},
                    "force_wincap": False, "force_freegame": False,
                },
            ),
        ]
        self.bet_modes = [
            BetMode(
                name="base", cost=1.0, rtp=self.rtp, max_win=self.wincap,
                auto_close_disabled=False, is_feature=True, is_buybonus=False,
                distributions=distributions,
            )
        ]
