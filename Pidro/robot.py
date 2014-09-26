__author__ = 'walter'
from webserver import app
import logging

log = logging.getLogger(app.config.get("LOGGER_NAME"))


class FakeGPIO(object):
    HIGH = "HIGH"
    LOW = "LOW"
    BCM = "BCM"
    IN = "IN"
    OUT = "OUT"

    @classmethod
    def output(cls, pin, state):
        log.debug("FAKE GPIO pin %s status %s" % (pin, state))

    @classmethod
    def setmode(cls, mode):
        log.debug("FAKE GPIO set mode %s" % mode)

    @classmethod
    def setup(cls, pin, mode):
        log.debug("FAKE GPIO pin %s mode %s" % (pin, mode))

    @classmethod
    def cleanup(cls):
        log.debug("FAKE GPIO cleanup")

try:
    import RPi.GPIO as GPIO
except ImportError:
    log.warning("FAKE GPIO Initialized, be sure you're not working on a real Raspberry.")
    GPIO = FakeGPIO


class GPIOHandler(object):
    class PinGroup(object):
        def __init__(self, pins):
            self.pins = pins

        def start(self):
            for pin in self.pins:
                log.info("GPIO pin %s status HIGH" % pin)
                GPIO.output(pin, GPIO.HIGH)

        def stop(self):
            for pin in self.pins:
                log.info("GPIO pin %s status LOW" % pin)
                GPIO.output(pin, GPIO.LOW)

    class Motor(PinGroup):
        def __init__(self, pins):
            if len(pins) != 2:
                raise ValueError('A Motor can only be managed by two pins')
            super(GPIOHandler.Motor, self).__init__(pins)

        def start(self):
            raise Exception('A Motor cannot have all his pins set to HIGH')

        def forward(self):
            log.info("GPIO pin %s status HIGH" % self.pins[0])
            GPIO.output(self.pins[0], GPIO.HIGH)
            log.info("GPIO pin %s status LOW" % self.pins[1])
            GPIO.output(self.pins[1], GPIO.LOW)

        def backward(self):
            log.info("GPIO pin %s status LOW" % self.pins[0])
            GPIO.output(self.pins[0], GPIO.LOW)
            log.info("GPIO pin %s status HIGH" % self.pins[1])
            GPIO.output(self.pins[1], GPIO.HIGH)

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.pins = {"PWMA": 17,
                     "PWMB": 23,
                     "AIN1": 27,
                     "AIN2": 4,
                     "BIN1": 24,
                     "BIN2": 25,
                     "STBY": 22}
        self.motor1 = None
        self.motor2 = None
        self.pwm = None
        self.setup_pins()

    def setup_pins(self):
        for name, pin in self.pins.items():
            log.info("Pin %s set up" % name)
            GPIO.setup(pin, GPIO.OUT)
        self.motor1 = GPIOHandler.Motor([self.pins["AIN1"], self.pins["AIN2"]])
        self.motor2 = GPIOHandler.Motor([self.pins["BIN1"], self.pins["BIN2"]])
        self.pwm = GPIOHandler.PinGroup([self.pins["PWMA"], self.pins["PWMB"], self.pins["STBY"]])

    def close(self):
        GPIO.cleanup()


class Robot(object):
    def __init__(self):
        log.warning("Robot is on!")
        self.handler = GPIOHandler()

    def off(self):
        log.warning("Robot is off.")
        self.handler.motor1.stop()
        self.handler.motor2.stop()
        self.handler.pwm.stop()
        self.handler.close()

    def standby(self):
        self.handler.motor1.stop()
        self.handler.motor2.stop()
        self.handler.pwm.start()

    def move_forward(self):
        self.handler.motor1.forward()
        self.handler.motor2.forward()
        self.handler.pwm.start()

    def move_backward(self):
        self.handler.motor1.backward()
        self.handler.motor2.backward()
        self.handler.pwm.start()

    def move_left(self):
        self.handler.motor1.forward()
        self.handler.motor2.backward()
        self.handler.pwm.start()

    def move_right(self):
        self.handler.motor1.backward()
        self.handler.motor2.forward()
        self.handler.pwm.start()

