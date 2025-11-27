
from manim import *

class GenScene(Scene):
    def construct(self):
        original_square = Square().scale(1.0).move_to(ORIGIN)
        self.play(Create(original_square))
        self.wait(1)
        self.play(Rotate(original_square, angle=PI/4))
        self.wait(1)
        self.play(Rotate(original_square, angle=PI/2))
        self.wait(1)
        self.play(Rotate(original_square, angle=3*PI/4))
        self.wait(1)
        self.play(Rotate(original_square, angle=PI))
        self.wait(1)
        self.play(Rotate(original_square, angle=5*PI/4))
        self.wait(1)
        self.play(Rotate(original_square, angle=3*PI/2))
        self.wait(1)
        self.play(Rotate(original_square, angle=7*PI/4))
        self.wait(1)
        self.play(Rotate(original_square, angle=2*PI))
