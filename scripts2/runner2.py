import pygame
import subprocess
import sys

# --- Constants ---
WIDTH, HEIGHT = 600, 400
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# --- Fonts ---
pygame.font.init()
FONT = pygame.font.Font(None, 36)

class GameRunner:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess AI Game Runner")
        self.clock = pygame.time.Clock()

        self.num_games = 10  # Always run 10 games
        self.white_wins = 0
        self.black_wins = 0
        self.running = True
        self.game_processes = []  # Store subprocess.Popen objects
        self.exit_codes = [] # Store the exit codes for all the games.

        # Remove input box and related variables
        # self.input_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 4, 100, 30)
        # self.input_text = str(self.num_games)
        # self.input_active = False

        self.run_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3, 100, 40)
        self.stop_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3 + 50, 100, 40)
        self.status_text = ""


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()

            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Removed input box handling

                if self.run_button.collidepoint(event.pos) and not self.game_processes:
                    self.start_games()
                elif self.stop_button.collidepoint(event.pos) and self.game_processes:
                    self.stop_games()


            # Removed input box keydown handling
            # if event.type == pygame.KEYDOWN:
            #     if self.input_active:
            #         if event.key == pygame.K_RETURN:
            #             try:
            #                 num_games = int(self.input_text)
            #                 if 1 <= num_games <= 20:
            #                     self.num_games = num_games
            #                 else:
            #                     self.status_text = "Enter a number between 1 and 20."
            #                     self.input_text = str(self.num_games) # reset input text
            #             except ValueError:
            #                 self.status_text = "Invalid input. Please enter a number."
            #                 self.input_text = str(self.num_games) # reset input text
            #             self.input_active = False

            #         elif event.key == pygame.K_BACKSPACE:
            #             self.input_text = self.input_text[:-1]
            #         elif len(self.input_text) < 2 and event.unicode.isdigit():
            #             self.input_text += event.unicode

    def draw(self):
        self.screen.fill(GRAY)

        # Removed Input Box
        # pygame.draw.rect(self.screen, WHITE, self.input_rect, 2)
        # text_surface = FONT.render(self.input_text, True, BLACK)
        # self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        # pygame.draw.rect(self.screen, LIGHT_BLUE if self.input_active else WHITE, self.input_rect)
        # text_surface = FONT.render(self.input_text, True, BLACK)
        # self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # Run Button
        pygame.draw.rect(self.screen, GREEN if not self.game_processes else GRAY, self.run_button)
        run_text = FONT.render("Run", True, BLACK)
        run_text_rect = run_text.get_rect(center=self.run_button.center)
        self.screen.blit(run_text, run_text_rect)

        # Stop Button
        pygame.draw.rect(self.screen, RED if self.game_processes else GRAY, self.stop_button)
        stop_text = FONT.render("Stop", True, BLACK)
        stop_text_rect = stop_text.get_rect(center=self.stop_button.center)
        self.screen.blit(stop_text, stop_text_rect)


        # Status Text
        status_surface = FONT.render(self.status_text, True, BLACK)
        self.screen.blit(status_surface, (20, HEIGHT - 50))

        # Display Wins
        white_wins_text = FONT.render(f"White Wins: {self.white_wins}", True, BLACK)
        black_wins_text = FONT.render(f"Black Wins: {self.black_wins}", True, BLACK)
        self.screen.blit(white_wins_text, (20, 20))
        self.screen.blit(black_wins_text, (20, 60))

        # Display Number of Games to Run (fixed at 10)
        num_games_text = FONT.render(f"Number of Games: {self.num_games}", True, BLACK)
        self.screen.blit(num_games_text, (WIDTH - 250, 20))



    def start_games(self):
        self.white_wins = 0
        self.black_wins = 0
        self.status_text = "Running Games..."
        self.game_processes = []  # Clear previous processes
        self.exit_codes = [] # clear previous exit codes.

        for _ in range(self.num_games):
            process = subprocess.Popen(["python", "game.py", "--zero-player"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.game_processes.append(process)

        # Monitor the game processes and update wins
        self.monitor_games()



    def stop_games(self):
        self.status_text = "Stopping Games..."
        for process in self.game_processes:
            process.terminate()
            process.wait() # Wait for the process to terminate.

        self.game_processes = [] # clear the game processes after they are terminated.
        self.status_text = "Games Stopped."

    def monitor_games(self):
        """Monitors the games and updates the wins when the games end."""
        while self.game_processes:
            for i, process in enumerate(self.game_processes):
                return_code = process.poll()
                if return_code is not None:
                    # Game has finished
                    self.exit_codes.append(return_code)

                    if return_code == 1:
                        self.white_wins += 1
                    elif return_code == 2:
                        self.black_wins += 1

                    # Remove the process from the list
                    self.game_processes.pop(i)
                    break  # Important to break to avoid index errors when modifying the list

            # Update the display and handle events
            self.draw()
            pygame.display.flip()
            pygame.time.delay(10)  # Avoid busy-waiting

        self.status_text = "All games finished."
        print(f"White Wins: {self.white_wins}, Black Wins: {self.black_wins}")


if __name__ == "__main__":
    game_runner = GameRunner()
    game_runner.run()

