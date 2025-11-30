# Supportive.py
from mistyPy.Robot import Robot
import time

ROBOT_IP = "192.168.1.237"

# Delay after Misty speaks before starting LED sequence (seconds)
TALK_DELAY = 6

# -----------------------------
# COLOR HELPERS
# -----------------------------

COLOR_MAP = {
    "white":  (255, 255, 255),
    "green":  (0, 255, 0),
    "blue":   (0, 0, 255),
    "red":    (255, 0, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
}

def set_led(misty, color_name):
    r, g, b = COLOR_MAP.get(color_name, COLOR_MAP["white"])
    misty.change_led(r, g, b)


def flash_sequence(misty, sequence, on_time=1.0, white_time=0.5):
    """
    sequence: list of color names, e.g. ["green", "blue", "blue"]
    Between each color Misty goes back to white (*).
    """
    for color in sequence:
        set_led(misty, color)
        time.sleep(on_time)
        set_led(misty, "white")
        time.sleep(white_time)


# -----------------------------
# PREDEFINED SEQUENCES
# -----------------------------

DIFFICULTY_SEQUENCES = {
    1: [
        ["green"],
        ["green", "blue"],
        ["green", "blue", "blue"],
        ["green", "blue", "blue", "blue"],
        ["green", "blue", "blue", "blue", "green"],
        ["green", "blue", "blue", "blue", "green", "blue"],
    ],
    2: [
        ["green", "blue"],
        ["green", "blue", "yellow"],
        ["green", "yellow", "blue", "yellow"],
        ["blue", "blue", "green", "yellow"],
        ["yellow", "green", "blue", "blue", "green"],
        ["yellow", "blue", "green", "yellow", "blue", "green"],
    ],
    3: [
        ["red", "green"],
        ["red", "green", "blue"],
        ["red", "blue", "green", "yellow"],
        ["green", "yellow", "red", "blue"],
        ["blue", "red", "yellow", "green", "blue"],
        ["yellow", "blue", "red", "green", "yellow", "blue"],
    ],
    4: [
        ["purple", "green"],
        ["purple", "green", "blue"],
        ["purple", "blue", "yellow", "green"],
        ["yellow", "purple", "green", "blue"],
        ["green", "purple", "blue", "yellow", "purple"],
        ["yellow", "green", "purple", "blue", "yellow", "green"],
    ],
    5: [
        ["red", "blue", "green"],
        ["red", "blue", "green", "yellow"],
        ["yellow", "red", "blue", "green", "purple"],
        ["green", "purple", "yellow", "red", "blue"],
        ["purple", "yellow", "green", "blue", "red", "yellow"],
        ["blue", "green", "purple", "yellow", "red", "green"],
    ],
}


# -----------------------------
# SUPPORTIVE GAME CLASS
# -----------------------------

class SupportiveMemoryGame:
    def __init__(self, ip=ROBOT_IP):
        self.misty = Robot(ip)

    # ------------- GAME LOGIC -------------

    def doRound(self, difficulty, round_number):
        """
        Plays the LED sequence for a given difficulty and round.
        round_number is 1-based.
        """
        sequences = DIFFICULTY_SEQUENCES.get(difficulty)
        if not sequences:
            self.misty.speak("Oops, I don't have that difficulty set up yet.")
            return

        index = round_number - 1
        if index < 0 or index >= len(sequences):
            self.misty.speak("Hmm, that round does not exist for this difficulty.")
            return

        sequence = sequences[index]
        self.misty.speak(
            f"Okay, here comes round {round_number} on difficulty {difficulty}. "
            "Watch the colors carefully!"
        )

        # 🔹 NEW: wait a bit so she finishes speaking before LEDs start
        time.sleep(TALK_DELAY)

        flash_sequence(self.misty, sequence)

    # ------------- SUPPORTIVE DIALOGUES -------------

    def playerStart(self):
        self.misty.speak(
            "Hi! My name is Misty. "
            "We're going to play a memory game together. "
            "I will show you a sequence of colors with my lights. "
            "Your job is to remember the order and repeat it. "
            "Between each color, I go back to white so you know it's a new color. "
            "Don't worry if it feels tricky, we'll take it step by step!"
        )

    def playerWon(self):
        self.misty.speak(
            "Wow, you did it! You completed the whole sequence. "
            "I'm really impressed with your memory. "
            "Thank you for playing with me!"
        )

    def playerCorrect(self):
        self.misty.speak(
            "Nice job! That was the correct sequence. "
            "You're doing great, keep it up!"
        )

    def readyForNext(self):
        self.misty.speak(
            "Are you ready for the next round? "
            "It will be a little bit more challenging, "
            "but I believe in you!"
        )

    def playerLost(self):
        self.misty.speak(
            "That wasn't quite the right sequence this time, "
            "but that's okay! This game is meant to be challenging. "
            "If you want, we can try again and see how far you get."
        )

    def playAgainQuestion(self):
        self.misty.speak(
            "Would you like to play again? "
            "We can try the same difficulty or pick a new one together."
        )

    def whatDifficulty(self):
        self.misty.speak(
            "Which difficulty would you like to play? "
            "You can choose a number from one to five. "
            "One is easiest and five is the most challenging."
        )

    # 🔹 NEW: “Sorry I didn’t quite hear what you said”
    def didntHear(self):
        self.misty.speak(
            "Sorry, I didn't quite hear what you said. "
            "Could you please repeat that for me?"
        )


# -----------------------------
# WIZARD INTERFACE
# -----------------------------

if __name__ == "__main__":
    game = SupportiveMemoryGame()

    # Command list:
    # 1 -> Intro / explain game
    # 2 -> Play a round (requires: difficulty, round)
    # 3 -> Player was correct
    # 4 -> Player won
    # 5 -> Player lost
    # 6 -> Ask to play again
    # 7 -> Ask for difficulty
    # 8 -> "Sorry, I didn't quite hear what you said"

    def run_command(cmd, args):
        """Dispatch based on command + optional arguments."""
        if cmd == 1:
            game.playerStart()

        elif cmd == 2:
            # Expect: args[0] = difficulty, args[1] = round_number
            if len(args) < 2:
                print("Command 2 needs: difficulty round_number, e.g. '2 1 4'")
                return
            difficulty = args[0]
            round_number = args[1]
            print(f"Running round {round_number} on difficulty {difficulty}")
            game.doRound(difficulty, round_number)

        elif cmd == 3:
            game.playerCorrect()

        elif cmd == 4:
            game.playerWon()

        elif cmd == 5:
            game.playerLost()

        elif cmd == 6:
            game.playAgainQuestion()

        elif cmd == 7:
            game.whatDifficulty()

        elif cmd == 8:
            game.didntHear()

        else:
            print("Unknown command.")

    while True:
        print("\n=== Supportive Mode – Wizard Commands ===")
        print("1: Intro / explain the game")
        print("2: Play a round – usage: 2 <difficulty 1-5> <round>")
        print("3: Player was correct")
        print("4: Player won")
        print("5: Player lost")
        print("6: Ask to play again")
        print("7: Ask for difficulty")
        print("8: Say 'Sorry, I didn't quite hear what you said'")
        print("0: Quit")

        line = input("Type command and optional args (e.g. '2 1 4'): ").strip()
        if not line:
            continue

        parts = line.split()
        try:
            cmd = int(parts[0])
        except ValueError:
            print("First value must be a number.")
            continue

        if cmd == 0:
            print("Exiting wizard.")
            break

        # Parse remaining parts as integers (for difficulty, round, etc.)
        args = []
        for p in parts[1:]:
            try:
                args.append(int(p))
            except ValueError:
                print(f"Ignoring non-integer argument: {p}")

        run_command(cmd, args)
