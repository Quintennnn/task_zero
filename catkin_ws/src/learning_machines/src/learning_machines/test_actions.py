import cv2

from data_files import FIGRURES_DIR
from robobo_interface import (
    IRobobo,
    Emotion,
    LedId,
    LedColor,
    SoundEmotion,
    SimulationRobobo,
    HardwareRobobo,
)


def test_emotions(rob: IRobobo):
    rob.set_emotion(Emotion.HAPPY)
    rob.talk("Hello")
    rob.play_emotion_sound(SoundEmotion.PURR)
    rob.set_led(LedId.FRONTCENTER, LedColor.GREEN)


def test_move_and_wheel_reset(rob: IRobobo):
    rob.move_blocking(100, 100, 1000)
    print("before reset: ", rob.read_wheels())
    rob.reset_wheels()
    rob.sleep(1)
    print("after reset: ", rob.read_wheels())


def test_move_manual(rob: IRobobo):
    rob.move(50, 100, 1000)
    print("before reset: ", rob.read_wheels())
    rob.reset_wheels()
    rob.sleep(1)
    print("after reset: ", rob.read_wheels())


def test_sensors(rob: IRobobo):
    print("IRS data: ", rob.read_irs())
    image = rob.get_image_front()
    cv2.imwrite(str(FIGRURES_DIR / "photo.png"), image)
    print("Phone pan: ", rob.read_phone_pan())
    print("Phone tilt: ", rob.read_phone_tilt())
    print("Current acceleration: ", rob.read_accel())
    print("Current orientation: ", rob.read_orientation())


def test_phone_movement(rob: IRobobo):
    rob.set_phone_pan_blocking(20, 100)
    print("Phone pan after move to 20: ", rob.read_phone_pan())
    rob.set_phone_tilt_blocking(50, 100)
    print("Phone tilt after move to 50: ", rob.read_phone_tilt())


def test_sim(rob: SimulationRobobo):
    print(rob.get_sim_time())
    print(rob.is_running())
    rob.stop_simulation()
    print(rob.get_sim_time())
    print(rob.is_running())
    rob.play_simulation()
    print(rob.get_sim_time())
    print(rob.get_position())


def test_hardware(rob: HardwareRobobo):
    print("Phone battery level: ", rob.read_phone_battery())
    print("Robot battery level: ", rob.read_robot_battery())


def move_back(rob: IRobobo):
    print("We've hit a wall, lets move backwards")
    rob.move_blocking(-30,-30,2000)
    
def turn_right(rob: IRobobo):
    print("We're making a 90 degree turn to the right")
    rob.move_blocking(28,-28 ,1000)
def turn_right(rob: IRobobo):
    print("We're making a 90 degree turn to the left")
    rob.move_blocking(-32,32,1000)
    




def ride_untill_collision(rob: IRobobo):
    """Rides in paces until it hits a wall,
    
    RETURNS: List of lists: Front Left values, Front Right sensor values and front center values
    """
    collision = False
    frontLvals = []
    frontRvals = []
    frontCvals = []

    while not collision:
        rob.move_blocking(30,30,1000)
        rob.sleep(0.3)
        backL, backR, frontL, frontR, frontC, frontRR, backC, frontLL = rob.read_irs()
        print("FrontL", frontL)
        print("FrontR", frontR)
        print("FrontC", frontC)
        frontLvals.append(frontL)
        frontRvals.append(frontR)
        frontCvals.append(frontC)
        if frontC > 10000:
              move_back(rob)
              turn_right(rob)
              collision = True
    return frontLvals, frontRvals, frontCvals



def task_zero(rob: IRobobo):
    if isinstance(rob, SimulationRobobo):
            rob.play_simulation()
    walls_hit = 0
    frontLvals = []
    frontRvals = []
    frontCvals = []

    while walls_hit < 4:
    

        front_l_temp, front_r_temp, front_c_temp = ride_untill_collision(rob)
        frontLvals.extend(front_l_temp)
        frontRvals.extend(front_r_temp)
        frontCvals.extend(front_c_temp)
        print("WALLS HIT BEFORE PLUS 1", walls_hit)
        walls_hit +=1
        print("WALLS HIT AFTER PLUS 1", walls_hit)

    
    if isinstance(rob, SimulationRobobo):
            rob.stop_simulation()

    return frontLvals, frontRvals, frontCvals

def run_all_actions(rob: IRobobo):
    pass
    """def run_all_actions(rob: IRobobo):
    if isinstance(rob, SimulationRobobo):
            rob.play_simulation()
        test_emotions(rob)
        test_sensors(rob)
        test_move_manual(rob)
        if isinstance(rob, SimulationRobobo):
            test_sim(rob)

        if isinstance(rob, HardwareRobobo):
            test_hardware(rob)

        test_phone_movement(rob)

        if isinstance(rob, SimulationRobobo):
            rob.stop_simulation() """
