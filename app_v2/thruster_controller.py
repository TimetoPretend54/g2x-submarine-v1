from vector import Vector2D
from interpolator import Interpolator
from Adafruit_MotorHAT import Adafruit_MotorHAT


PRECISION = 3


class ThrusterController:
    def __init__(self):
        # setup motor controller
        self.motor_controller = Adafruit_MotorHAT(addr=0x60)

        # setup left joystick
        self.j1 = Vector2D()
        self.left_thruster = Interpolator()
        self.left_thruster.addIndexValue(0.0, -1.0)
        self.left_thruster.addIndexValue(90.0, 1.0)
        self.left_thruster.addIndexValue(180.0, 1.0)
        self.left_thruster.addIndexValue(270.0, -1.0)
        self.left_thruster.addIndexValue(360.0, -1.0)
        self.right_thruster = Interpolator()
        self.right_thruster.addIndexValue(0.0, 1.0)
        self.right_thruster.addIndexValue(90.0, 1.0)
        self.right_thruster.addIndexValue(180.0, -1.0)
        self.right_thruster.addIndexValue(270.0, -1.0)
        self.right_thruster.addIndexValue(360.0, 1.0)

        # setup right joystick
        self.j2 = Vector2D()
        self.v_front_thruster = Interpolator()
        self.v_front_thruster.addIndexValue(0.0, 0.0)
        self.v_front_thruster.addIndexValue(90.0, -1.0)
        self.v_front_thruster.addIndexValue(180.0, 0.0)
        self.v_front_thruster.addIndexValue(270.0, 1.0)
        self.v_front_thruster.addIndexValue(360.0, 0.0)
        self.v_back_left_thruster = Interpolator()
        self.v_back_left_thruster.addIndexValue(0.0, 1.0)
        self.v_back_left_thruster.addIndexValue(90.0, 1.0)
        self.v_back_left_thruster.addIndexValue(180.0, -1.0)
        self.v_back_left_thruster.addIndexValue(270.0, -1.0)
        self.v_back_left_thruster.addIndexValue(360.0, 1.0)
        self.v_back_right_thruster = Interpolator()
        self.v_back_right_thruster.addIndexValue(0.0, -1.0)
        self.v_back_right_thruster.addIndexValue(90.0, 1.0)
        self.v_back_right_thruster.addIndexValue(180.0, 1.0)
        self.v_back_right_thruster.addIndexValue(270.0, -1.0)
        self.v_back_right_thruster.addIndexValue(360.0, -1.0)

        # setup ascent/descent controllers
        self.ascent = -1.0
        self.descent = -1.0

    def __del__(self):
        print("releasing motors")
        self.motor_controller.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.motor_controller.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.motor_controller.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.motor_controller.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def update_axis(self, axis, value):
        update_horizontal_thrusters = False
        update_vertical_thrusters = False
        value = round(value, PRECISION)

        if axis == 0:
            if self.j1.x != value:
                self.j1.x = value
                update_horizontal_thrusters = True
        elif axis == 1:
            if self.j1.y != value:
                self.j1.y = value
                update_horizontal_thrusters = True
        elif axis == 2:
            if self.j2.x != value:
                self.j2.x = value
                update_vertical_thrusters = True
        elif axis == 5:
            if self.j2.y != value:
                self.j2.y = value
                update_vertical_thrusters = True
        elif axis == 3:
            if self.descent != value:
                self.descent = value
                update_vertical_thrusters = True
        elif axis == 4:
            if self.ascent != value:
                self.ascent = value
                update_vertical_thrusters = True
        else:
            pass
            # print("unknown axis ", event.axis)

        if update_horizontal_thrusters:
            left_value = self.left_thruster.valueAtIndex(self.j1.angle)
            right_value = self.right_thruster.valueAtIndex(self.j1.angle)
            power = min(1.0, self.j1.length)
            self.setMotor(1, left_value * power)
            self.setMotor(3, right_value * power)

        if update_vertical_thrusters:
            power = min(1.0, self.j2.length)
            front_value = self.v_front_thruster.valueAtIndex(self.j2.angle) * power
            back_left_value = self.v_back_left_thruster.valueAtIndex(self.j2.angle) * power
            back_right_value = self.v_back_right_thruster.valueAtIndex(self.j2.angle) * power
            if self.ascent != -1.0:
                percent = (1.0 + self.ascent) / 2.0
                max_thrust = max(front_value, back_left_value, back_right_value)
                max_adjust = (1.0 - max_thrust) * percent
                front_value += max_adjust
                back_left_value += max_adjust
                back_right_value += max_adjust
            elif self.descent != -1.0:
                percent = (1.0 + self.descent) / 2.0
                min_thrust = min(front_value, back_left_value, back_right_value)
                max_adjust = (min_thrust - -1.0) * percent
                front_value -= max_adjust
                back_left_value -= max_adjust
                back_right_value -= max_adjust
            self.set_motor(2, front_value)
            self.set_motor(1, back_left_value)
            self.set_motor(3, back_right_value)

        def set_motor(self, motor_number, value):
            motor = self.motor_controller.getMotor(motor_number)
            value *= 255.0

            if value < 0:
                motor.run(Adafruit_MotorHAT.BACKWARD)
                motor.setSpeed(-int(value))
            else:
                motor.run(Adafruit_MotorHAT.FORWARD)
                motor.setSpeed(int(value))


if __name__ == "__main__":
    pass
