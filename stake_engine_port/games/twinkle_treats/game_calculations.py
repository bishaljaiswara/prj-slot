"""SDK calculation adapter: maps SDK Symbol objects to the Twinkle rules resolver."""
from src.executables.executables import Executables
from cluster_rules import resolve_clusters, SYMBOL_PRIORITY

class GameCalculations(Executables):
    def get_clusters_update_wins(self):
        # SDK board layout is [reel][row]; resolver consumes row-major [row][reel].
        row_major = [[self.board[reel][row].name for reel in range(self.config.num_reels)]
                     for row in range(self.config.num_rows[0])]
        resolved = resolve_clusters(row_major)
        win_data = {"totalWin": 0, "wins": []}
        for symbol, flat_cells in resolved:
            size = len(flat_cells)
            payout = self.config.paytable.get((size, symbol), 0)
            positions = [{"reel": cell % self.config.num_reels, "row": cell // self.config.num_reels}
                         for cell in flat_cells]
            if payout <= 0:
                continue
            win_data["totalWin"] += payout
            for pos in positions:
                self.board[pos["reel"]][pos["row"]].explode = True
            win_data["wins"].append({
                "symbol": symbol, "clusterSize": size, "win": payout,
                "positions": positions,
                "meta": {"globalMult": 1, "clusterMult": 1, "winWithoutMult": payout,
                         "overlay": {"reel": positions[0]["reel"], "row": positions[0]["row"]}},
            })
            self.record({"kind": size, "symbol": symbol, "mult": 1, "gametype": self.gametype})
        self.win_data = win_data
        self.win_manager.update_spinwin(win_data["totalWin"])
        self.win_manager.tumble_win = win_data["totalWin"]
