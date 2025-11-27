
from manim import *

class GenScene(Scene):
    def construct(self):
        square_left = Square().scale(0.5).to_edge(LEFT)
        text_left = Text("5").move_to(square_left.get_center())
        self.play(Create(square_left), Write(text_left))

        square_right = Square().scale(0.7).to_edge(RIGHT)
        text_right = Text("1").move_to(square_right.get_center())
        self.play(Create(square_right), Write(text_right))

        square_center = Square().scale(0.3).move_to(ORIGIN)
        text_center = Text("4").move_to(square_center.get_center())
        self.play(Create(square_center), Write(text_center))

        compare_text1 = Text("Compare first two bars").to_edge(DOWN)
        self.play(Write(compare_text1))
        self.wait()
        self.play(FadeOut(compare_text1))

        self.play(square_left.animate.move_to(square_right.get_center()), text_left.animate.move_to(square_right.get_center()))
        self.play(square_right.animate.move_to(square_left.get_center()), text_right.animate.move_to(square_left.get_center()))

        swap_text1 = Text("Swap them as 5 > 1").to_edge(DOWN)
        self.play(Write(swap_text1))
        self.wait()
        self.play(FadeOut(swap_text1))

        compare_text2 = Text("Compare second and third bars").to_edge(DOWN)
        self.play(Write(compare_text2))
        self.wait()
        self.play(FadeOut(compare_text2))

        self.play(square_center.animate.move_to(square_right.get_center()), text_center.animate.move_to(square_right.get_center()))
        self.play(square_right.animate.move_to(square_center.get_center()), text_right.animate.move_to(square_center.get_center()))

        swap_text2 = Text("Swap them as 5 > 4").to_edge(DOWN)
        self.play(Write(swap_text2))
        self.wait()
        self.play(FadeOut(swap_text2))

        bubble_text = Text("Largest value is bubbled to the end").to_edge(DOWN)
        self.play(Write(bubble_text))
        self.wait()
        self.play(FadeOut(bubble_text))

        repeat_text = Text("Repeat for the remaining unsorted portion").to_edge(DOWN)
        self.play(Write(repeat_text))
        self.wait()
        self.play(FadeOut(repeat_text))

        self.wait()
