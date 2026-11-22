"""Initial SDK simulation entry point. Debug-only; no optimization or production output."""
from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    create_books(
        gamestate,
        config,
        {"base": 100},
        100,
        1,
        False,
        False,
    )
    generate_configs(gamestate)
