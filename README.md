# Chess Game ("chessnut")

This project includes a command-line chess game implemented in Python, along with a game runner for automated AI vs. AI matches.

## Game Features

*   **Command-Line Arguments:** The game utilizes `argparse` for flexible command-line options.
*   **AI vs AI mode:** A zero player mode where AI plays against AI.
*   **Window Positioning:** Control the game window's position on your screen.

## Dependencies

Before running the game or runner, make sure you have Pygame installed:

```bash
pip install pygame
```

## Running the Game

The `game.py` script provides several command-line options:

1.  **Regular Game (Title Screen):**

    ```bash
    python game.py
    ```

2.  **0-Player Mode (AI vs. AI):**

    ```bash
    python game.py --zero-player
    ```

    This will start a game where the AI plays against itself. The script will automatically exit after the game concludes.

3.  **0-Player Mode with Window Position:**

    ```bash
    python game.py --zero-player --x 100 --y 200
    ```

    Starts an AI vs. AI game with the window positioned at x=100, y=200 on your screen.

## Running Multiple Games with the Runner

The `runner.py` script automates running multiple AI vs. AI games and tracks the win counts for each side.

To run the game runner:

```bash
python runner.py
```

The runner will launch 10 chess games, position them on the screen, and then display the statistics of which color won in the runner window. A "Run" and "Stop" button are available to start and stop the games.
```

