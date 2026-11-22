"""Initial SDK simulation entry point. Small debug batch only; no optimization yet."""
from gamestate import GameState
from game_config import GameConfig
from src.state.run_sims import create_books
from src.write_data.write_configs import generate_configs

if __name__ == "__main__":
    config = GameConfig()
    gamestate = GameState(config)
    create_books(
        gamestate=gamestate,
        config=config,
        num_sim_args={"base": 100, "bonus": 100},
        batching_size=100,
        num_threads=1,
        compression=False,
        profiling=False,
    )
    generate_configs(gamestate)
