from mistyPy.Robot import Robot
import time
import random

ROBOT_IP = "192.168.1.237"

# Delay after Misty speaks before starting LED sequence (seconds)
TALK_DELAY = 4.5

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
    "cyan":   (0, 255, 255), # Authoritative idle color
}

def set_led(misty, color_name):
    r, g, b = COLOR_MAP.get(color_name, COLOR_MAP["white"])
    misty.change_led(r, g, b)

def set_neutral_led(misty):
    """Sets LED to a neutral, authoritative color (Cyan) for standby."""
    misty.change_led(255, 255, 255)

def flash_sequence(misty, sequence, on_time=1.0, white_time=0.5):
    """
    sequence: list of color names, e.g. ["green", "blue", "blue"]
    Between each color Misty goes back to white (*).
    After sequence, returns to Cyan (Neutral).
    """
    for color in sequence:
        set_led(misty, color)
        time.sleep(on_time)
        set_led(misty, "white")
        time.sleep(white_time)
    
    # Return to authoritative neutral state
    set_neutral_led(misty)


# -----------------------------
# EYE HELPERS
# -----------------------------

# Authoritative eyes: Neutral, Focused, Unimpressed
# NO happy eyes in this version.
NEUTRAL_EYES = [
    "e_DefaultContent.jpg",
    "e_Contempt.jpg",     # Slightly stricter/evaluative look
    "e_SystemBlack.jpg",  # Very robotic/cold look
]

def show_neutral_eyes(misty):
    """Display a random neutral/serious eye image."""
    filename = random.choice(NEUTRAL_EYES)
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
# AUTHORITATIVE GAME CLASS
# -----------------------------

class AuthoritativeMemoryGame:
    def __init__(self, ip=ROBOT_IP):
        self.misty = Robot(ip)
        # Initialize with neutral state
        set_neutral_led(self.misty)
        show_neutral_eyes(self.misty)

    # ------------- GAME LOGIC -------------

    def doRound(self, difficulty, round_number):
        """Plays the LED sequence for a given difficulty and round."""
        sequences = DIFFICULTY_SEQUENCES.get(difficulty)
        if not sequences:
            show_neutral_eyes(self.misty)
            self.misty.speak("Error. Difficulty level not found.")
            return

        index = round_number - 1
        if index < 0 or index >= len(sequences):
            show_neutral_eyes(self.misty)
            self.misty.speak("Error. Round index out of bounds.")
            return

        sequence = sequences[index]

        # Concise, directive phrasing
        templates = [
            "Initiating round {round}. Difficulty {difficulty}. Observe.",
            "Round {round}. Difficulty level {difficulty}. Sequence starting.",
            "Attention. Round {round}, difficulty {difficulty}. Execute observation."
        ]
        line = random.choice(templates).format(
            round=round_number, difficulty=difficulty
        )

        show_neutral_eyes(self.misty)
        set_neutral_led(self.misty) # Ensure we are in neutral state before speaking
        self.misty.speak(line)

        time.sleep(TALK_DELAY)
        flash_sequence(self.misty, sequence)

    # ------------- AUTHORITATIVE DIALOGUES -------------

    def playerStart(self):
        show_neutral_eyes(self.misty)
        set_neutral_led(self.misty)
        self.misty.speak(
            "Memory Assessment Protocol initiated. "
            "I will display a color sequence with the light on my chest. "
            "It will glow white inbetween each color."
            "You are required to memorize and after the sequence is done repeat back to me. "
            "Prepare for the first trial."
        )

    def playerWon(self):
        lines = [
            "Sequence verified. All inputs correct. Protocol complete.",
            "Performance adequate. Task finished. Final result: Success.",
            "Objective achieved. All sequences replicated."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def playerCorrect(self):
        lines = [
            "Correct.",
            "Sequence matched.",
            "Input accepted.",
            "Accurate."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def readyForNext(self):
        lines = [
            "Proceeding to next round.",
            "Loading next sequence.",
            "Next trial initiating."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def playerLost(self):
        lines = [
            "Incorrect sequence.",
            "Error detected in playback.",
            "Sequence mismatch. Task failed.",
            "Input invalid."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def playAgainQuestion(self):
        lines = [
            "Shall I proceed with a new game?",
            "Acknowledge to start new task.",
            "Should I reset system for a new game?"
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def whatDifficulty(self):
        lines = [
            "Select difficulty level: 1 to 5.",
            "State desired challenge level, 1 to 5.",
            "What difficulty level? Choose 1 to 5."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    def didntHear(self):
        lines = [
            "Input unclear. Repeat.",
            "Audio not detected. State command again.",
            "Transmission failed. Repeat."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    # ------------- MODIFIED WATER BREAK -------------

    def waterBreak(self):
        # Mandatory maintenance style
        lines = [
            "Hydration break initiated. Consume water now to maintain cognitive efficiency.",
            "Performance check. Hydration required. Drink water immediately.",
            "Mandatory interval. Water consumption required for optimal function."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    # ------------- NEW: ACKNOWLEDGE (Cmd 11) -------------
    
    def acknowledge(self):
        # Replaces "Cool!", "Awesome!" with neutral confirmations
        lines = [
            "Acknowledged.",
            "Noted.",
            "Input received.",
            "Ok."
        ]
        show_neutral_eyes(self.misty)
        self.misty.speak(random.choice(lines))

    # ------------- NEW: GOODBYE (Cmd 00) -------------

    def goodbye(self):
        # Replaces "Have a wonderful day!" with protocol termination
        show_neutral_eyes(self.misty)
        self.misty.speak("Session terminated. Powering down interaction protocol.")


# -----------------------------
# WIZARD INTERFACE
# -----------------------------

if __name__ == "__main__":
    game = AuthoritativeMemoryGame()

    def run_command(cmd, args):
        """Dispatch based on command + optional arguments."""
        if cmd == 1:
            game.playerStart()

        elif cmd == 2:
            if len(args) < 2:
                print("Usage: 2 <difficulty> <round>")
                return
            difficulty, round_number = args

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
        
        elif cmd == 99:
            game.goodbye()

        else:
            print("Unknown command.")

    while True:
        print("\n=== AUTHORITATIVE Wizard Commands ===")
        print("1: Intro (Protocol Start)")
        print("2: Play round — 2 <difficulty> <round> (also prints sequence)")
        print("3: Player correct (Verified)")
        print("4: Player won (Protocol Complete)")
        print("5: Player lost (Error)")
        print("6: Restart question")
        print("7: Ask difficulty")
        print("8: Input unclear")
        print("9: MANDATORY WATER BREAK")
        print("11: Acknowledge (Noted/Proceed)")
        print("99: Terminate Session")
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