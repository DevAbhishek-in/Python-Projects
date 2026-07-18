import random
import time


class RandomNumberGenerator:
    def __init__(self):
        self.secret_number = None

    def generate_secret_number(self):
        self.secret_number = random.randint(1, 100)
        return self.secret_number


class GuessChecker(RandomNumberGenerator):
    def __init__(self):
        super().__init__()
        self.secret_number = self.generate_secret_number()

    def is_correct_guess(self, guessed_number):
        if self.secret_number == guessed_number:
            return False
        return True

    def show_hint(self, guessed_number):
        hint = (
            "⬇️Too Low! Guess again."
            if guessed_number < self.secret_number
            else "⬆️Too High! Guess again."
        )
        print(hint)


print("""
========================================
🎮 Welcome to the Perfect Guess Game!
========================================
I have selected a secret number between 1 and 100.
Can you guess it?

Good Luck! 🍀
""")


# Create game object
game = GuessChecker()

game_running = True
total_attempts = 0

print("Game is loading....")
time.sleep(2)

game_start_time = time.time()


while game_running:

    try:
        guessed_number = int(input("🔢 Enter your guess (1-100): "))

    except ValueError:
        print("⚠️ Invalid input! Please enter only numbers.")
        continue

    except KeyboardInterrupt:
        print("\n⚠️ Game interrupted by user.")
        break

    except EOFError:
        print("\n⚠️ Input closed unexpectedly.")
        break

    except Exception as error:
        print(f"⚠️ Unexpected error: {error}")
        continue


    if guessed_number < 1 or guessed_number > 100:
        print("⚠️ Please enter a number between 1 and 100.")
        continue

    total_attempts += 1
    game_running = game.is_correct_guess(guessed_number)

    if game_running:
        game.show_hint(guessed_number)


# Calculate game time
game_end_time = time.time()
elapsed_time = game_end_time - game_start_time


print("""
========================================
🎉 Congratulations!
🏆 You guessed the correct number.
========================================
""")


print(f"🎯 Attempts   : {total_attempts}")
print(f"⏱️ Time Taken : {elapsed_time:.2f} seconds")
print("🙏 Thanks for playing!")
