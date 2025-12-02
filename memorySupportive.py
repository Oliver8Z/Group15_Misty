from mistyPy.Robot import Robot
import time
import random

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
# EYE HELPERS
# -----------------------------

HAPPY_EYES = [
    "e_Joy.jpg",
    "e_Joy2.jpg",
    "e_JoyGoofy.jpg",
]

NEUTRAL_EYES = [
    "e_DefaultContent.jpg",
]

def show_random_eyes(misty, eye_list):
    """Display a random eye image from the given list."""
    filename = random.choice(eye_list)
    misty.display_image(filename, 1)  # alpha=1 (fully opaque)


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
        """Plays the LED sequence for a given difficulty and round."""
        sequences = DIFFICULTY_SEQUENCES.get(difficulty)
        if not sequences:
            show_random_eyes(self.misty, NEUTRAL_EYES)
            self.misty.speak("Oops, I don't have that difficulty set up yet.")
            return

        index = round_number - 1
        if index < 0 or index >= len(sequences):
            show_random_eyes(self.misty, NEUTRAL_EYES)
            self.misty.speak("Hmm, that round doesn't exist for this difficulty.")
            return

        sequence = sequences[index]

        # Varied supportive phrasing
        templates = [
            "Okay, here comes round {round} on difficulty {difficulty}! Watch closely.",
            "Get ready for round {round} on difficulty {difficulty}. Try to remember the colors!",
            "Round {round} on difficulty {difficulty}. I'll show you the sequence now!"
        ]
        line = random.choice(templates).format(
            round=round_number, difficulty=difficulty
        )

        show_random_eyes(self.misty, HAPPY_EYES)
        self.misty.speak(line)

        time.sleep(TALK_DELAY)
        flash_sequence(self.misty, sequence)

    # ------------- SUPPORTIVE DIALOGUES -------------

    def playerStart(self):
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(
            "Hi! My name is Misty. We're going to play a memory game together. "
            "I will show you a sequence of colors with the light on my chest. "
            "Your job is to remember the order and repeat it back to me. "
            "My chest will glow white inbetween each color. "
            "Don't worry! We'll take it step by step!"
        )

    def playerWon(self):
        lines = [
            "Wow, you did it! You completed the whole sequence. I'm really impressed!",
            "Amazing work! You got the entire sequence right!",
            "You nailed it! That was perfect memory work!"
        ]
        show_random_eyes(self.misty, HAPPY_EYES)
        self.misty.speak(random.choice(lines))

    def playerCorrect(self):
        lines = [
            "Nice job! That's the correct sequence!",
            "Yes, exactly right! You're doing really well.",
            "Correct! You remembered that perfectly!"
        ]
        show_random_eyes(self.misty, HAPPY_EYES)
        self.misty.speak(random.choice(lines))

    def readyForNext(self):
        lines = [
            "Ready for the next round? You're doing great!",
            "Shall we try the next round? I believe in you!",
            "If you're ready, we can continue to the next round!"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    def playerLost(self):
        lines = [
            "That sequence was tricky, but that's okay! We can try again.",
            "No worries, that one was tough. Want to give it another go?",
            "It didn’t work this time, but I know you can get it next round!"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    def playAgainQuestion(self):
        lines = [
            "Would you like to play again?",
            "Do you want to try another round?",
            "Would you like to go again?"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    def whatDifficulty(self):
        lines = [
            "Which difficulty would you like? One to five!",
            "Pick a difficulty between one and five!",
            "Tell me a difficulty: one is easiest, five is hardest!"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    def didntHear(self):
        lines = [
            "Sorry, I didn't quite hear that. Could you repeat it?",
            "I think I missed that. Can you say it again?",
            "Oops, I didn't catch that. Could you repeat yourself?"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    # ------------- WATER BREAK -------------

    def waterBreak(self):
        lines = [
            "Hey, how about we take a little sip of water?",
            "Quick pause! This could be a good moment to have a drink of water.",
            "Before we continue, maybe take a small sip of water. It can help you stay focused!"
        ]
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak(random.choice(lines))

    def acknowledge(self):
        lines = [
            "Cool!",
            "Great!",
            "Awesome!",
            "Nice!"
        ]
        show_random_eyes(self.misty, HAPPY_EYES)
        self.misty.speak(random.choice(lines))

    def goodbye(self):
        show_random_eyes(self.misty, NEUTRAL_EYES)
        self.misty.speak("Okay! It was really fun playing with you. Have a wonderful rest of your day. Goodbye!")



# -----------------------------
# WIZARD INTERFACE
# -----------------------------

if __name__ == "__main__":
    game = SupportiveMemoryGame()

    def run_command(cmd, args):
        """Dispatch based on command + optional arguments."""
        if cmd == 1:
            game.playerStart()

        elif cmd == 2:
            if len(args) < 2:
                print("Usage: 2 <difficulty> <round>")
                return
            difficulty, round_number = args

            # Print the correct sequence for the wizard
            sequences = DIFFICULTY_SEQUENCES.get(difficulty)
            if sequences is None:
                print(f"No sequences defined for difficulty {difficulty}.")
                return

            index = round_number - 1
            if index < 0 or index >= len(sequences):
                print(f"Round {round_number} is not defined for difficulty {difficulty}.")
                return

            sequence = sequences[index]
            print(f"Difficulty {difficulty}, round {round_number}")
            print("Correct sequence:", ", ".join(sequence))

            # Then actually play the round on Misty
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

        elif cmd == 9:
            game.waterBreak()

        elif cmd == 11:
            game.acknowledge()
        
        elif cmd == 00:
            game.goodbye()


        else:
            print("Unknown command.")

    while True:
        print("\n=== Supportive Wizard Commands ===")
        print("1: Intro")
        print("2: Play round — 2 <difficulty> <round> (also prints sequence)")
        print("3: Player correct")
        print("4: Player won")
        print("5: Player lost")
        print("6: Play again question")
        print("7: Ask difficulty")
        print("8: Didn't hear")
        print("9: Suggest water break")
        print("11: Simple acknowledgement (Cool / Great / Awesome)")
        print("00: Say goodbye")
        print("0: EXIT WIZARD MODE")

        line = input("> ").strip()
        if not line:
            continue

        parts = line.split()
        cmd = int(parts[0]) if parts[0].isdigit() else -1

        if cmd == 0:
            break

        args = [int(x) for x in parts[1:] if x.isdigit()]
        run_command(cmd, args)
