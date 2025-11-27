
from manim import *

class GenScene(Scene):
    def construct(self):
        square_left = Square().scale(0.5).to_edge(LEFT)
        text_5 = Text("5")
        text_5.move_to(square_left.get_center())
        self.play(Create(square_left), Write(text_5))

        square_right = Square().scale(0.7).to_edge(RIGHT)
        text_2 = Text("2")
        text_2.move_to(square_right.get_center())
        self.play(Create(square_right), Write(text_2))

        compare_text = Text("Compare the first two bars").to_edge(UP)
        self.play(Write(compare_text))
        self.wait()

        swap_text = Text("Since 5 > 2, swap them").to_edge(UP)
        self.play(Transform(compare_text, swap_text))
        self.wait()

        new_square_left = Square().scale(0.7).to_edge(LEFT)
        new_text_2 = Text("2").move_to(new_square_left.get_center())

        new_square_right = Square().scale(0.5).to_edge(RIGHT)
        new_text_5 = Text("5").move_to(new_square_right.get_center())

        self.play(Transform(square_left, new_square_left), Transform(text_5, new_text_2))
        self.play(Transform(square_right, new_square_right), Transform(text_2, new_text_5))

        self.wait()

        square_right_5 = Square().scale(0.7).to_edge(RIGHT)
        text_5_again = Text("5").move_to(square_right_5.get_center())
        self.play(Create(square_right_5), Write(text_5_again))

        square_right_1 = Square().scale(0.3).next_to(square_right_5, RIGHT)
        text_1 = Text("1").move_to(square_right_1.get_center())
        self.play(Create(square_right_1), Write(text_1))

        compare_text_2 = Text("Compare the next two bars").to_edge(UP)
        self.play(Transform(swap_text, compare_text_2))
        self.wait()

        swap_text_2 = Text("Since 5 > 1, swap them").to_edge(UP)
        self.play(Transform(compare_text_2, swap_text_2))
        self.wait()

        new_square_right_1 = Square().scale(0.7).next_to(square_left, RIGHT*2)
        new_text_1 = Text("1").move_to(new_square_right_1.get_center())

        new_square_right_5 = Square().scale(0.3).next_to(new_square_right_1, RIGHT)
        new_text_5_end = Text("5").move_to(new_square_right_5.get_center())

        self.play(Transform(square_right_1, new_square_right_5), Transform(text_1, new_text_5_end))
        self.play(Transform(square_right_5, new_square_right_1), Transform(text_5_again, new_text_1))

        self.wait()

        continue_text = Text("Continue until the largest element bubbles to the end").to_edge(UP)
        self.play(Transform(swap_text_2, continue_text))
        self.wait()

        repeat_text = Text("Repeat for the remaining unsorted elements").to_edge(UP)
        self.play(Transform(continue_text, repeat_text))
        self.wait()
