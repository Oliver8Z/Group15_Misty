from mistyPy.Robot import Robot
import time

# --------------------------------------
# CONFIG
# --------------------------------------
ROBOT_IP = "192.168.1.237"


# --------------------------------------
# HELPER FUNCTIONS (SUPPORTIVE STYLE)
# --------------------------------------

def set_supportive_eyes(misty):
    """
    Use a warm / happy eye image.
    Make sure this filename exists on your Misty.
    """
    misty.display_image("e_Joy.jpg", 1)

def set_admiration_eyes(misty):
    """
    Use a warm / happy eye image.
    Make sure this filename exists on your Misty.
    """
    misty.display_image("e_Admiration.jpg", 1)

def set_heart_eyes(misty):
    """
    Use a warm / happy eye image.
    Make sure this filename exists on your Misty.
    """
    misty.display_image("e_Love.jpg", 1)


def reset_posture_supportive(misty):
    """Neutral-ish posture before starting."""
    misty.move_head(0, 0, 0, 50)          # pitch, roll, yaw, velocity
    misty.move_arm("left", 10, 60)
    misty.move_arm("right", 10, 60)


def head_pan_left_right_supportive(misty, duration=2.0):
    """
    Big, noticeable left-right look.
    Supportive version can be a bit smoother/faster.
    """
    # Look far left
    misty.move_head(0, 0, 70, 70)
    time.sleep(duration / 3)
    # Look far right
    misty.move_head(0, 0, -70, 70)
    time.sleep(duration / 3)
    # Back to center
    misty.move_head(0, 0, 0, 70)
    time.sleep(duration / 3)


def little_arm_demo_supportive(misty):
    """
    Soft but noticeable arm movement.
    Larger positions so it's easy to see.
    """
    # Raise both arms quite a bit
    misty.move_arm("left", 80, 80)
    misty.move_arm("right", 80, 80)
    time.sleep(0.8)
    # Lower them again, but not all the way down
    misty.move_arm("left", 30, 80)
    misty.move_arm("right", 30, 80)
    time.sleep(0.8)


# --------------------------------------
# SUPPORTIVE INTRO BEHAVIOUR
# --------------------------------------

def play_supportive_intro(misty):
    """
    Supportive, warm, expressive style.
    Uses:
      - display_image
      - move_head / move_arm
      - speak
    """

    reset_posture_supportive(misty)
    set_supportive_eyes(misty)
    time.sleep(0.5)

    # Line 1
    set_supportive_eyes(misty)
    misty.speak("Hi! My name is Misty")
    time.sleep(3)

    # Line 2
    misty.speak("I'm a robot developed by Misty Robotics")
    time.sleep(3)

    # Line 3 – arms + happy eyes
    set_supportive_eyes(misty)
    misty.speak("I can do many things. Look, I can move my arms")
    little_arm_demo_supportive(misty)
    time.sleep(2)

    # Line 4 – head moves, playful but only left/right
    set_admiration_eyes(misty)
    misty.speak("And I can move my head too")
    head_pan_left_right_supportive(misty, duration=2.0)
    time.sleep(1.5)

    # Line 5 – supportive / guidance framing

    misty.speak(
        "When I interact with people, I try to be supportive "
        "and make tasks feel comfortable for you"
    )
    time.sleep(5)
    set_heart_eyes(misty)
    # Line 6 – warm goal
    misty.speak(
        "My goal is to help you and make our interaction enjoyable"
    )
    head_pan_left_right_supportive(misty, duration=2.0)
    time.sleep(3)

    # End pose: centered, warm eyes
    set_supportive_eyes(misty)
    misty.move_head(0, 0, 0, 40)
    time.sleep(1)


# --------------------------------------
# MAIN
# --------------------------------------

if __name__ == "__main__":
    misty = Robot(ROBOT_IP)
    play_supportive_intro(misty)
