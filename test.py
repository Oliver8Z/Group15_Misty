from mistyPy.Robot import Robot
from mistyPy.Events import Events
import time
import sys

# --------------------------------------
# CONFIG
# --------------------------------------
ROBOT_IP = "192.168.1.237"

FACE_TIMEOUT = 8          # s since last face before ignoring ToF
NEAR_PAT_FIRST_DELAY = 4  # s near before first pat request
NEAR_PAT_SECOND_DELAY = 6 # s after first pat request before second

# Cooldowns (seconds) to stop speech spamming
COOLDOWN_FAR_FIRST  = 6
COOLDOWN_FAR_SECOND = 10
COOLDOWN_MEDIUM     = 6
COOLDOWN_NEAR_THANK = 6

# --------------------------------------
# SETUP
# --------------------------------------
misty = Robot(ROBOT_IP)

# ---- GLOBAL STATE ----
current_zone = None    # "far", "medium", "near"
far_first_time = None
far_second_prompt_done = False

near_since = None
asked_for_pat = False
pat_received = False
pat_prompt_time = None
second_pat_prompt_done = False

last_face_time = None
neutral_mode = True    # in neutral idle?

# last time each speech line was spoken (for cooldowns)
last_far_first_time   = 0.0
last_far_second_time  = 0.0
last_medium_time      = 0.0
last_near_thank_time  = 0.0

# flag to stop everything once head pat is received
skill_done = False

# --------------------------------------
# NEUTRAL STATE
# --------------------------------------
def go_neutral():
    global current_zone, far_first_time, far_second_prompt_done
    global near_since, asked_for_pat, pat_received, pat_prompt_time, second_pat_prompt_done
    global neutral_mode

    print("Going to NEUTRAL state")
    misty.display_image("e_DefaultContent.jpg")
    misty.change_led(0, 255, 0)          # green idle
    misty.move_head(0, 0, 0)
    misty.move_arm("left", 0, 50)        # arms down
    misty.move_arm("right", 0, 50)

    current_zone = None
    far_first_time = None
    far_second_prompt_done = False

    near_since = None
    asked_for_pat = False
    pat_received = False
    pat_prompt_time = None
    second_pat_prompt_done = False

    neutral_mode = True

go_neutral()

# --------------------------------------
# PLAN: decide distance zone with hysteresis
# --------------------------------------
def get_zone_with_hysteresis(dist_meters, current_zone):
    """
    Hysteresis avoids constant zone flipping around boundaries.
    Rough idea:
      - If already NEAR, stay NEAR until distance > 1.0
      - If already FAR, stay FAR until distance < 1.3
      - Otherwise use basic thresholds.
    """
    if dist_meters is None:
        return current_zone

    # Initial classification if we don't have a zone yet
    if current_zone is None:
        if dist_meters > 1.5:
            return "far"
        elif dist_meters > 0.7:
            return "medium"
        else:
            return "near"

    # Hysteresis depending on current zone
    if current_zone == "near":
        if dist_meters > 1.0:       # must move clearly away to leave NEAR
            if dist_meters > 1.5:
                return "far"
            else:
                return "medium"
        else:
            return "near"

    if current_zone == "medium":
        if dist_meters < 0.6:
            return "near"
        elif dist_meters > 1.7:
            return "far"
        else:
            return "medium"

    if current_zone == "far":
        if dist_meters < 1.3:       # must approach clearly to leave FAR
            if dist_meters < 0.7:
                return "near"
            else:
                return "medium"
        else:
            return "far"

    return current_zone

# --------------------------------------
# ACT: distance behaviours (with cooldowns)
# --------------------------------------
def behavior_far_first(now):
    """User is far away – first friendly invitation."""
    global neutral_mode, last_far_first_time
    if now - last_far_first_time < COOLDOWN_FAR_FIRST:
        return  # cooldown: don't speak again yet
    last_far_first_time = now

    neutral_mode = False
    print("Zone: FAR (first)")
    misty.display_image("e_Amazement.jpg")    # friendly / attentive
    misty.change_led(0, 0, 255)               # blue
    misty.move_arm("left", 80, 50)            # both arms up-ish
    misty.move_arm("right", 80, 50)
    misty.speak("Come closer!", 1)

def behavior_far_second(now):
    """User stayed far – second invitation."""
    global last_far_second_time
    if now - last_far_second_time < COOLDOWN_FAR_SECOND:
        return
    last_far_second_time = now

    print("Zone: FAR (second)")
    misty.display_image("e_Admiration.jpg")   # slightly different friendly face
    misty.change_led(0, 0, 255)               # blue
    misty.move_arm("left", 70, 50)
    misty.move_arm("right", 70, 50)
    misty.speak("Come on, come closer!", 1)

def behavior_medium(now):
    """User is a bit closer – invite them to sit."""
    global neutral_mode, near_since, asked_for_pat, pat_received
    global pat_prompt_time, second_pat_prompt_done, last_medium_time

    if now - last_medium_time < COOLDOWN_MEDIUM:
        # Even if we skip speech, still update pose so it's visually right
        print("Zone: MEDIUM (cooldown, no speech)")
    else:
        last_medium_time = now
        print("Zone: MEDIUM")
        misty.speak("Hello friend, have a seat!", 1)

    neutral_mode = False
    misty.display_image("e_ContentRight.jpg") # warm / inviting
    misty.change_led(255, 255, 0)             # yellow
    misty.move_arm("left", 0, 50)             # one arm down
    misty.move_arm("right", 80, 50)           # one arm forward

    # reset pat-related state
    near_since = None
    asked_for_pat = False
    pat_received = False
    pat_prompt_time = None
    second_pat_prompt_done = False

def behavior_near(now):
    """User is closest – thank them for sitting."""
    global neutral_mode, near_since, asked_for_pat, pat_received
    global pat_prompt_time, second_pat_prompt_done, last_near_thank_time

    if now - last_near_thank_time < COOLDOWN_NEAR_THANK:
        print("Zone: NEAR (cooldown, no speech)")
    else:
        last_near_thank_time = now
        print("Zone: NEAR")
        misty.speak("Thank you for sitting down!", 1)

    neutral_mode = False
    misty.display_image("e_Joy2.jpg")         # very friendly / joyful
    misty.change_led(0, 255, 0)               # green
    misty.move_arm("left", -90, 50)           # both arms forward
    misty.move_arm("right", -90, 50)

    near_since = now
    asked_for_pat = False
    pat_received = False
    pat_prompt_time = None
    second_pat_prompt_done = False

# --------------------------------------
# ACT: head-pat requests & responses
# --------------------------------------
def ask_for_pat_first():
    global asked_for_pat, pat_prompt_time
    print("Asking for head pat (first time)")
    misty.display_image("e_Admiration.jpg")
    misty.change_led(0, 128, 255)             # soft blue
    misty.move_arm("left", 40, 50)
    misty.move_arm("right", 40, 50)
    misty.speak("If you would like to begin, please give me a gentle pat on my head.", 1)
    asked_for_pat = True
    pat_prompt_time = time.time()

def ask_for_pat_second():
    global second_pat_prompt_done, pat_prompt_time
    print("Asking for head pat (second time)")
    misty.display_image("e_Joy.jpg")
    misty.change_led(255, 192, 203)           # pinkish, extra friendly
    misty.move_arm("left", 50, 50)
    misty.move_arm("right", 50, 50)
    misty.speak("Pretty please, could you pat my head?", 1)
    second_pat_prompt_done = True
    pat_prompt_time = time.time()

def behavior_pat_thank_you():
    global pat_received, skill_done
    print("Head pat received – thanking user")
    misty.display_image("e_JoyGoofy2.jpg")
    misty.change_led(0, 255, 0)               # happy green
    misty.move_arm("left", -80, 50)
    misty.move_arm("right", -80, 50)
    misty.speak("Thank you for patting my head! Let's begin the tasks.", 1)
    pat_received = True

    # ---- FINISH THE SKILL HERE ----
    skill_done = True

    # Stop face recognition & unregister events
    try:
        misty.stop_face_recognition()
    except Exception as e:
        print("Could not stop face recognition:", e)

    for evt in ["distance_event", "face_event", "touch_event"]:
        try:
            misty.unregister_event(evt)
        except Exception as e:
            print(f"Could not unregister {evt}:", e)

    print("Skill finished after head pat.")
    # Optional hard exit (only if running from your own machine script):
    # sys.exit(0)

# --------------------------------------
# SENSE + PLAN + ACT: Time-of-Flight callback
# --------------------------------------
def tof_callback(data):
    """
    SENSE: read distance from center TOF.
    PLAN: only act if a face was seen recently; decide zone with hysteresis.
    ACT: trigger behaviours + pat prompts.
    """
    global current_zone, far_first_time, far_second_prompt_done
    global near_since, asked_for_pat, pat_received, pat_prompt_time, second_pat_prompt_done
    global last_face_time, neutral_mode, skill_done

    if skill_done:
        return

    # Only center sensor
    if data["message"]["sensorPosition"] != "Center":
        return

    dist = data["message"]["distanceInMeters"]
    now = time.time()
    print("Distance (m):", dist)

    # --- Face gate: ignore ToF if no recent face ---
    if last_face_time is None:
        return
    if now - last_face_time > FACE_TIMEOUT:
        if not neutral_mode:
            go_neutral()
        return

    neutral_mode = False

    # PLAN: zone with hysteresis
    new_zone = get_zone_with_hysteresis(dist, current_zone)

    # Zone changed → call appropriate behaviour
    if new_zone != current_zone:
        current_zone = new_zone

        if new_zone == "far":
            far_first_time = now
            far_second_prompt_done = False
            behavior_far_first(now)

        elif new_zone == "medium":
            far_first_time = None
            far_second_prompt_done = False
            behavior_medium(now)

        elif new_zone == "near":
            far_first_time = None
            far_second_prompt_done = False
            behavior_near(now)

    # --- Extra logic while staying in same zone ---

    # FAR: after some time far, second prompt
    if current_zone == "far" and far_first_time is not None and not far_second_prompt_done:
        if now - far_first_time > 5:
            behavior_far_second(now)
            far_second_prompt_done = True

    # NEAR: ask for head pat over time
    if current_zone == "near" and near_since is not None and not pat_received:
        if not asked_for_pat and (now - near_since > NEAR_PAT_FIRST_DELAY):
            ask_for_pat_first()
        elif asked_for_pat and not second_pat_prompt_done and pat_prompt_time is not None:
            if now - pat_prompt_time > NEAR_PAT_SECOND_DELAY:
                ask_for_pat_second()

# --------------------------------------
# SENSE: Face recognition
# --------------------------------------
def face_callback(data):
    global last_face_time, neutral_mode, skill_done
    if skill_done:
        return

    last_face_time = time.time()
    if neutral_mode:
        print("Face seen – ready to react to distance now.")
    print("Face label:", data["message"].get("label", "unknown"))

# --------------------------------------
# SENSE: Touch sensors (for head pat)
# --------------------------------------
def touch_callback(data):
    global current_zone, pat_received, skill_done
    if skill_done:
        return

    sensor_pos = data["message"]["sensorPosition"]
    is_contacted = data["message"]["isContacted"]

    if not is_contacted or current_zone != "near" or pat_received:
        return

    head_sensors = ["HeadFront", "HeadBack", "HeadLeft", "HeadRight", "Scruff", "Chin"]
    if sensor_pos in head_sensors:
        behavior_pat_thank_you()

# --------------------------------------
# EVENT REGISTRATION
# --------------------------------------
misty.register_event(
    event_name='distance_event',
    event_type=Events.TimeOfFlight,
    callback_function=tof_callback,
    keep_alive=True,
    debounce=200
)

misty.start_face_recognition()
misty.register_event(
    event_name='face_event',
    event_type=Events.FaceRecognition,
    callback_function=face_callback,
    keep_alive=True,
    debounce=1000
)

misty.register_event(
    event_name='touch_event',
    event_type=Events.TouchSensor,
    callback_function=touch_callback,
    keep_alive=True,
    debounce=250
)

misty.keep_alive()
