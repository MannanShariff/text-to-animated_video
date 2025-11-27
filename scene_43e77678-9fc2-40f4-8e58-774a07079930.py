
from manim import *

class GenScene(Scene):
    def construct(self):
        square_left = Square().scale(0.5).move_to(LEFT)
        text_left = Text("3").move_to(square_left.get_center())
        group_left = VGroup(square_left, text_left)
        self.play(Create(square_left), Write(text_left))

        square_right = Square().scale(0.7).move_to(RIGHT)
        text_right = Text("1").move_to(square_right.get_center())
        group_right = VGroup(square_right, text_right)
        self.play(Create(square_right), Write(text_right))

        text_compare = Text("Compare 3 and 1").next_to(group_left, UP)
        self.play(Write(text_compare))

        self.wait()

        self.play(group_left.animate.move_to(RIGHT))
        self.play(group_right.animate.move_to(LEFT))

        text_swap = Text("Swap!").next_to(group_left, UP)
        self.play(Write(text_swap))

        self.wait()

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()

        square_left = Square().scale(0.7).move_to(LEFT)
        text_left = Text("1").move_to(square_left.get_center())
        group_left = VGroup(square_left, text_left)
        self.play(Create(square_left), Write(text_left))

        square_right = Square().scale(0.5).move_to(RIGHT)
        text_right = Text("3").move_to(square_right.get_center())
        group_right = VGroup(square_right, text_right)
        self.play(Create(square_right), Write(text_right))

        square_down = Square().scale(0.9).move_to(DOWN)
        text_down = Text("5").move_to(square_down.get_center())
        group_down = VGroup(square_down, text_down)
        self.play(Create(square_down), Write(text_down))

        text_next = Text("Next comparison...").next_to(group_left, UP)
        self.play(Write(text_next))
