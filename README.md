# Chess Game ("chessnut")


* **Command-Line Argument Parsing:** Uses `argparse` for robust command-line argument handling.  This is the correct way to handle command-line options in Python.
* **`--zero-player` Flag:**  A boolean flag `--zero-player` is added. When present, the game starts directly in 0-player mode, bypassing the title screen.
* **`--x` and `--y` Arguments:** Added `--x` and `--y` arguments to control the window position.
* **Game Initialization Logic:**  The code now correctly initializes the `Game` object based on the presence of the `--zero-player` flag.
* **Automatic Exit in 0-Player Mode:** The `while running` loop includes a condition to automatically exit after the 0-player game is over (`args.zero_player and game and game.game_over`). This is crucial for the script to terminate.  It also exits after the `update()` check.
* **Error Handling (Limited):**  No explicit `try...except` blocks are added, but `argparse` will handle basic type validation.
* **Clarity and Structure:** The code is organized to improve readability, particularly in the `main()` function.
* **Correctness:** The main loop now correctly handles both the title screen and the game logic depending on the startup mode.
* **Title Screen Bypass:** Correctly skips the title screen when `--zero-player` is given.
* **Docstrings and Comments:** Good use of docstrings and comments to explain the purpose of each section of code.
* **Dependencies:** Includes necessary imports at the top.

How to run:

1.  **Regular Game (Title Screen):**

    ```bash
    python your_script_name.py
    ```

2.  **0-Player Mode (AI vs. AI):**

    ```bash
    python your_script_name.py --zero-player
    ```

3.  **0-Player Mode with Window Position:**

    ```bash
    python your_script_name.py --zero-player --x 100 --y 200
    ```

Now, when the game is run in 0-player mode with `--zero-player`, the script will automatically exit when the game concludes. The title screen works if `--zero-player` is not supplied. The window position can be set using `--x` and `--y`. This version should be fully functional.

