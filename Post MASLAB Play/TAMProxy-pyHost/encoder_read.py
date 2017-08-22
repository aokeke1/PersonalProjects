from tamproxy import Sketch, SyncedSketch, Timer
from tamproxy.devices import Encoder

# Prints a quadrature encoder's position
class EncoderRead(SyncedSketch):

    pins = 6, 7

#    #motor pins
#    left_motor_dir_pin, left_motor_pwm_pin = 4,5#2,3
#    right_motor_dir_pin, right_motor_pwm_pin = 2,3#4,5
#    #encoder pins
#    left_motor_encoder_pins = 16,15#6, 7
#    right_motor_encoder_pins = 6,7#8, 9

    def setup(self):
        self.encoder = Encoder(self.tamp, *self.pins, continuous=True)
        self.timer = Timer()

    def loop(self):
        if self.timer.millis() > 100:
            self.timer.reset()
            print self.encoder.val

if __name__ == "__main__":
    sketch = EncoderRead(1, -0.00001, 100)
    sketch.run()