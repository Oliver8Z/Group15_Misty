from mistyPy.Robot import Robot
import time

# --------------------------------------
# CONFIG
# --------------------------------------
ROBOT_IP = "192.168.1.237"


# --------------------------------------
# HELPER FUNCTIONS (AUTHORITATIVE STYLE)
# --------------------------------------

def set_neutral_eyes(misty):
    """
    Use a neutral / default eye image.
    Make sure this filename exists on your Misty.
    """
    misty.display_image("e_DefaultContent.jpg", 1)


def reset_posture_authoritative(misty):
    """Neutral, straight posture before starting."""
    misty.move_head(0, 0, 0, 50)
    misty.move_arm("left", 10, 60)
    misty.move_arm("right", 10, 60)


def head_pan_left_right_authoritative(misty, duration=2.0):
    """
    Big, controlled left-right look.
    """
    # Look far left
    misty.move_head(0, 0, 70, 90)
    time.sleep(duration / 3)
    # Look far right
    misty.move_head(0, 0, -70, 90)
    time.sleep(duration / 3)
    # Back to center
    misty.move_head(0, 0, 0, 90)
    time.sleep(duration / 3)


def little_arm_demo_neutral(misty):
    """
    More controlled, less playful arm movement.
    Still large enough to be clearly visible.
    """
    # Raise both arms
    misty.move_arm("left", 70, 70)
    misty.move_arm("right", 70, 70)
    time.sleep(0.8)
    # Lower to a mid position
    misty.move_arm("left", 25, 70)
    misty.move_arm("right", 25, 70)
    time.sleep(0.8)


# --------------------------------------
# LOWER-PITCH SPEAKER WRAPPER
# --------------------------------------

def speak_authoritative(misty, text):
    """
    Speak with a lower pitch for the authoritative style.

    pitch:
      0 = deep
      1 = default
      2 = high
    """
    misty.speak(text, 0)  # lower pitch


# --------------------------------------
# AUTHORITATIVE / STRAIGHTFORWARD INTRO
# --------------------------------------

def play_authoritative_intro(misty):
    """
    Authoritative / straightforward style.
    - Neutral face
    - Controlled, minimal but large movements
    - Lower voice pitch
    """

    reset_posture_authoritative(misty)
    set_neutral_eyes(misty)
    time.sleep(0.5)

    # Line 1
    set_neutral_eyes(misty)
    speak_authoritative(misty, "Hello. My name is Misty")
    time.sleep(3)

    # Line 2
    speak_authoritative(misty, "I am a robot developed by Misty Robotics")
    time.sleep(3)

    # Line 3 – arms, controlled
    set_neutral_eyes(misty)
    speak_authoritative(
        misty,
        "I am capable of performing a variety of actions. I can move my arms"
    )
    little_arm_demo_neutral(misty)
    time.sleep(2)

    # Line 4 – head movement, only left and right
    set_neutral_eyes(misty)
    speak_authoritative(misty, "I can also rotate my head")
    head_pan_left_right_authoritative(misty, duration=3.0)
    time.sleep(1.5)

    # Line 5 – supervision / task focus
    set_neutral_eyes(misty)
    speak_authoritative(
        misty,
        "When I interact with humans, I provide clear guidance and ensure tasks are performed correctly"
    )
    time.sleep(5)

    # Line 6 – competence / decision framing
    set_neutral_eyes(misty)
    speak_authoritative(
        misty,
        "These abilities make me reliable when important decisions or supervision are required"
    )
    time.sleep(4)

    # End pose: neutral, facing forward
    set_neutral_eyes(misty)
    misty.move_head(0, 0, 0, 40)
    time.sleep(1)


# --------------------------------------
# MAIN
# --------------------------------------

if __name__ == "__main__":
    misty = Robot(ROBOT_IP)
    play_authoritative_intro(misty)
