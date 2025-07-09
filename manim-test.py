from manim import *





class IndigoGraphScene(MovingCameraScene):


    def construct(self):
        self.edges_created = []
        self.camera.background_color = "#7A00E6"
        central_node = self.create_node("Iñigo Sanz", "Data analyst SGP", "icon", BLUE_C, scale = 1)
        self.wait(3)
        self.create_education(central_node)
        self.wait(1)
        self.play(
            self.camera.frame.animate.move_to(central_node.get_center()).scale(.6),
            run_time=.5
        )
        self.wait(.5)
        self.create_interests(central_node)
        self.wait(.5)
        self.create_sanofi(central_node)
        self.wait(.5)
        self.create_next_steps(central_node)
        self.wait(.5)
        self.play(
            self.camera.frame.animate.move_to(central_node.get_center()).scale(2),
            run_time=.5
        )
        self.animate_circles_along_edges()
        self.wait(2)
        self.animate_circles_along_edges()
        self.wait(2)
        self.animate_circles_along_edges()
        self.wait(2)
        self.play(
            self.camera.frame.animate.move_to(central_node.get_center()).scale(2.5),
            run_time=.5
        )
        self.wait(4)







    def create_edge(self, origin, end, clr):
        line = Line(origin, end, color=WHITE).set_z_index(-1)
        self.edges_created += [(origin, end, clr)]
        return line



    def create_node(self, iconName, description, image, color, position=ORIGIN, scale = 1):
        image = ImageMobject("manim-images/" + image + ".png").scale(0.5 * scale)
        image.height = scale

        circle = Circle(
            radius=image.width * .9,
            color=color,
            fill_opacity=1,
            fill_color=WHITE,
            stroke_width=4,
        ).move_to(position)  # Move circle to position

        image.move_to(circle.get_center())

        name_text = Text(iconName, color=WHITE).scale(0.5).next_to(circle, DOWN, buff=0.3)
        title_text = Text(description, color=WHITE).scale(0.4).next_to(name_text, DOWN, buff=0.1)

        central_node = Group(circle, image, name_text, title_text).move_to(position)
        central_node.set_z_index(10)

        # Create pulse effect starting at the node's center
        pulse_circle = Circle(
            radius=0.1,
            color=color,
            stroke_width=4
        ).move_to(position + UP * .1)

        # Animate pulse: grow and fade out
        self.add(pulse_circle)  # Start with it visible
        self.play(
            GrowFromCenter(central_node),
            pulse_circle.animate.scale(20).set_opacity(0),
            run_time=.4,
        )
        self.remove(pulse_circle)  # Clean up after effect

        return central_node


    def animate_circles_along_edges(self, radius=0.05, run_time=1):
        pulses = []
        animations = []

        for origin, end, clr in self.edges_created:
            pulse = Circle(radius=radius, color=clr, fill_opacity=.4).move_to(end)
            pulses.append(pulse)
            animations.append(pulse.animate.move_to(origin))

        self.add(*pulses)              # Add all pulses first
        self.play(*animations, run_time=run_time)  # Animate them all at once
        self.remove(*pulses)           # Remove all pulses after animation




    def create_growing_box(self, text_str, position, box_color=WHITE, text_color=BLACK, width=3, height=0.7):
        rect = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=BLUE_D,
            stroke_width=2,
            fill_color=box_color,
            fill_opacity=1,
        ).move_to(position)
        rect.set_z_index(10)
        text = Text(text_str, color=text_color).scale(0.4).move_to(position)
        text.set_z_index(11)
        group = VGroup(rect, text)
        self.play(GrowFromCenter(rect), Write(text), run_time = .5)
        return group
    

    def create_text_block(self, text_str, position, text_color=BLACK, anchor= "none", weight = NORMAL):
        text = Text(text_str, color=text_color, weight = weight).scale(0.4)
        text.set_z_index(11)
        if anchor == "left":
            text.shift(position - text.get_left())  # Align the left edge of the text to `position`
        self.play(Write(text), run_time=0.25)
        return text


    def create_spain(self, spain_node, center_pos, sub_texts):
        # Spain sub-boxes positioned to the RIGHT
        spain_sub_texts = sub_texts

        spain_pos= spain_node.get_center()

        spain_sub_boxes = VGroup()
        n = len(spain_sub_texts)
        spacing = 0.8  # distance between boxes vertically
        total_height = (n - 1) * spacing
        start_offset = total_height / 2 + 0.4  # center the boxes vertically + extra offset

        for i, text in enumerate(spain_sub_texts):
            pos = spain_pos + RIGHT * 5 + UP * (start_offset - i * spacing)
            weight = "BOLD" if i == 0 else "NORMAL"
            box = self.create_text_block(text, pos, text_color=WHITE, anchor="left", weight=weight)
            spain_sub_boxes.add(box)

        # Spain connecting lines (main box right edge to sub-box left edge)
        spain_lines = VGroup()
        for box in spain_sub_boxes:
            line = self.create_edge(spain_node.get_center() + UP * .35, box.get_left() + LEFT, YELLOW)
            spain_lines.add(line)

        self.play(
            *[Create(line) for line in spain_lines],
            run_time=.3
        )



    def create_education(self, central_node):
        center = central_node.get_center()
        v_spacing = 1.0
        zoom_scale = 0.8

        self.play(
            self.camera.frame.animate.move_to(center + RIGHT * 4).scale(1.1),
            run_time=.5
        )

        education_pos = center + RIGHT * 4 + UP * .5

        education_box = self.create_growing_box("Education", education_pos, width=3, height=0.9, box_color=YELLOW)

        lines = []

        lines.append(self.create_edge(central_node.get_center() + UP * 0.45, education_box.get_left(), YELLOW))

        schoolNode = self.create_node("Madrid, ES", "Lycée Français", "spain-flag", YELLOW, education_pos + RIGHT * 4 + UP * 2.7, scale=0.7)
        lines.append(self.create_edge(education_pos, schoolNode.get_left(), YELLOW))

        spainNode = self.create_node("Madrid, ES", "Bachelor on CompSci", "spain-flag", YELLOW, education_pos + RIGHT * 4, scale=0.7)
        lines.append(self.create_edge(education_pos, spainNode.get_left(), YELLOW))

        denmarkNode = self.create_node("Aalborg, DK", "Master on CompSci", "denmark-flag", YELLOW, education_pos + RIGHT * 4 + DOWN * 2.7, scale=0.7)
        lines.append(self.create_edge(education_pos, denmarkNode.get_left(), YELLOW))

        self.play(*[Create(line) for line in lines], run_time=1)


        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(center + RIGHT * 10).scale(1.5),
            run_time=.5
        )

        # school
        sub_texts = [
            "4 languages",
        ]
        self.create_spain(schoolNode, center, sub_texts)
        # spain
        sub_texts = [
            "Universidad Complutense de Madrid",
            "Project Manager Jr.",
            "Thesis on Alzheimer's disease clustering"
        ]
        self.create_spain(spainNode, center, sub_texts)

        # denmark
        sub_texts = [
            "Aalborg University",
            "Backend developer",
            "Thesis on Renal cell Carcinoma & Autoencoders"
        ]
        self.create_spain(denmarkNode, center, sub_texts)

        self.animate_circles_along_edges()
        self.wait(2.5)




    def create_interests(self, central_node):
        center = central_node.get_center()
        v_spacing = 1.0
        zoom_scale = 0.8

        self.play(
            self.camera.frame.animate.move_to(center + LEFT * 7).scale(1.4),
            run_time=.5
        )

        interests_pos = center + LEFT * 4 + UP * .5

        interests_box = self.create_growing_box("Interests", interests_pos, width=3, height=0.9, box_color=RED)

        lines = []

        lines.append(self.create_edge(central_node.get_center() + UP * 0.4, interests_box.get_left(), RED))

        aiNode = self.create_node("Applied AI", "Help people on day-to-day", "appliedai", RED, interests_pos + LEFT * 5 + UP * 3.8, scale=0.7)
        lines.append(self.create_edge(interests_pos, aiNode.get_right(), RED))

        roboticsNode = self.create_node("Robotics", "Mix automation with AI", "robotics", RED, interests_pos + LEFT * 6.4 + UP * 1.4, scale=0.7)
        lines.append(self.create_edge(interests_pos, roboticsNode.get_right(), RED))

        gameDevNode = self.create_node("Game Dev", "Personal family project", "gamedev", RED, interests_pos + LEFT * 6.4 + DOWN * 1.4, scale=0.7)
        lines.append(self.create_edge(interests_pos, gameDevNode.get_right(), RED))

        runningNode = self.create_node("AI in sports & health", "Data analytics during runs", "sports", RED, interests_pos + LEFT * 5 + DOWN * 3.8, scale=0.7)
        lines.append(self.create_edge(interests_pos, runningNode.get_right(), RED))

        self.play(*[Create(line) for line in lines], run_time=1)


        self.wait(2.5)

        self.animate_circles_along_edges()


    
    def create_sanofi(self, central_node):
        center = central_node.get_center()
        v_spacing = 1.0
        zoom_scale = 0.8

        self.play(
            self.camera.frame.animate.move_to(center + UP * 7).scale(1.1),
            run_time=.5
        )

        sanofi_pos = center + UP * 4

        sanofi_box = self.create_growing_box("Sanofi", sanofi_pos, width=3, height=0.9, box_color=PURPLE)

        lines = []

        lines.append(self.create_edge(central_node.get_center() + UP * 0.45, sanofi_box.get_bottom(), PURPLE))

        icdNode = self.create_node("ICD, R&D", "Integrative Clinical Data", "icd", PURPLE, sanofi_pos + UP * 5 + LEFT * 4, scale=0.7)
        lines.append(self.create_edge(sanofi_pos, icdNode.get_bottom(), PURPLE))

        sgpNode = self.create_node("SGP", "Sanofi Graduate Program", "sgp", PURPLE, sanofi_pos + UP * 5 + RIGHT * 4, scale=0.7)
        lines.append(self.create_edge(sanofi_pos, sgpNode.get_bottom(), PURPLE))

        self.play(*[Create(line) for line in lines], run_time=1)

        lines = []

        self.play(
            self.camera.frame.animate.move_to(icdNode.get_center() + UP * 3.5 + LEFT).scale(1.4),
            run_time=.5
        )

        # icdNode

        teamBox = self.create_growing_box("Some of my very talented team", icdNode.get_center() + UP * 3, width=4.5, height=0.8, box_color=PURPLE)
        lines.append(self.create_edge(icdNode.get_center(), teamBox.get_bottom(), PURPLE))


        ajNode = self.create_node("Amhar JABEER", "Computational Scientist", "amhar", BLUE, teamBox.get_center() + UP * 3 + LEFT * 2, scale=0.7)
        lines.append(self.create_edge(teamBox.get_top(), ajNode.get_bottom(), PURPLE))

        brNode = self.create_node("Brandon RUFINO", "Director of AI for Clinical Trial design", "brandon", BLUE, teamBox.get_center() + UP * 3 + RIGHT * 2, scale=0.7)
        lines.append(self.create_edge(teamBox.get_top(), brNode.get_bottom(), PURPLE))

        top_left = ajNode.get_center() + UP * 2 + LEFT * 2.75
        top_right = brNode.get_center() + UP * 2 + RIGHT * 2.75
        bottom_left = ajNode.get_center() + UP * 3
        bottom_right = brNode.get_center() + UP * 3

        self.create_node("Maksim KRIUKOV", "Computational Scientist Lead", "maksim", BLUE, top_left, scale=0.6)
        self.create_node("Greg PADIASEK", "Computational Scientist Lead", "greg", BLUE, top_right, scale=0.6)
        self.create_node("Utkarsh VASHISTH", "MLOps Engineering Analyst", "utkarsh", BLUE, bottom_left, scale=0.6)
        self.create_node("Rahavi SELVARAJAN", "Data Engineer", "rahavi", BLUE, bottom_right, scale=0.6)

        self.play(*[Create(line) for line in lines], run_time=1)

        self.wait(1.5)

        lines = []

        indFinNode = self.create_node("Indication Finding", "Discover new indications + prioritize", "indicationfinding", PURPLE, icdNode.get_center() + UP * 2.5 + LEFT * 4, scale=0.7)
        lines.append(self.create_edge(icdNode.get_center() + UP*.5, indFinNode.get_center() + UP * .5, PURPLE))

        plmNode = self.create_node("Patient Like Me", "Leverage precision medicine in AI", "plm", PURPLE, icdNode.get_center() + UP * -2.5 + LEFT * 4, scale=0.7)
        lines.append(self.create_edge(icdNode.get_center()+ UP*.5, plmNode.get_center() + UP * .5, PURPLE))

        hackNode = self.create_node("Hackathon", "BioMedX - annotate graphs", "hackathon", PURPLE, icdNode.get_center() + LEFT * 4, scale=0.7)
        lines.append(self.create_edge(icdNode.get_center()+ UP*.5, hackNode.get_center() + UP * .5, PURPLE))

        innovationNode = self.create_node("LT Innovation Program", "Development Award", "innovation", PURPLE, indFinNode.get_center() + LEFT * 6, scale=0.6)
        lines.append(self.create_edge(indFinNode.get_center() + UP*.5, innovationNode.get_center() + UP * .5, PURPLE))

        self.play(*[Create(line) for line in lines], run_time=1)

        self.wait(3.5)

        lines = []

        # sgpNode

        self.play(
            self.camera.frame.animate.move_to(sgpNode.get_center()).scale(.7),
            run_time=.5
        )

        milestoneNode = self.create_node("Milestone III - Dupiflow", "Presenting to MCO Council", "dupiflow", PURPLE, sgpNode.get_center() + UP * 1.5 + RIGHT * 4, scale=0.7)
        lines.append(self.create_edge(sgpNode.get_center() + UP * .5, milestoneNode.get_center() + UP * .5, PURPLE))

        depLearnNode = self.create_node("Department learning", "Learned about other areas in Sanofi", "recycle", PURPLE, sgpNode.get_center() + UP * -1.5 + RIGHT * 4, scale=0.7)
        lines.append(self.create_edge(sgpNode.get_center() + UP * .5, depLearnNode.get_center() + UP * .25, PURPLE))


        self.play(*[Create(line) for line in lines], run_time=1)

        self.wait(4)




    def create_next_steps(self, central_node):
        center = central_node.get_center()
        v_spacing = 1.0
        zoom_scale = 0.8

        self.play(
            self.camera.frame.animate.move_to(center + DOWN * 7).scale(1.1),
            run_time=.5
        )

        lines = []

        steps_pos = center + DOWN * 4

        steps_box = self.create_growing_box("Next steps?", steps_pos, width=3, height=0.9, box_color=GREEN)
        lines.append(self.create_edge(central_node.get_center(), steps_box.get_center(), GREEN))

        versNode = self.create_node("Versatility", "Work in all kinds of areas", "appliedai", GREEN, steps_box.get_center() + DOWN * 4 + LEFT * 4, scale=0.5)
        lines.append(self.create_edge(steps_box.get_bottom(), versNode.get_center(), GREEN))

        focusNode = self.create_node("Focus on AI in Pharma", "R&D in ICD team", "icd", GREEN, steps_box.get_center() + DOWN * 4 + LEFT * 0, scale=0.5)
        lines.append(self.create_edge(steps_box.get_bottom(), focusNode.get_center(), GREEN))

        doorsNode = self.create_node("No closed doors", "This is the chapter where to grow", "sgp", GREEN, steps_box.get_center() + DOWN * 4 + LEFT * -4, scale=0.5)
        lines.append(self.create_edge(steps_box.get_bottom(), doorsNode.get_center(), GREEN))

        self.play(*[Create(line) for line in lines], run_time=1)

        self.wait(1)

        self.play(
            self.camera.frame.animate.move_to(steps_pos + DOWN * 3).scale(1.3),
            run_time=.5
        )

        lines = []

        versNode2 = self.create_node("???", "???", "appliedai", GREEN, steps_box.get_center() + DOWN * 6 + LEFT * 7, scale=0.7)
        lines.append(self.create_edge(versNode.get_bottom(), versNode2.get_center(), GREEN))

        versNode2 = self.create_node("???", "???", "appliedai", GREEN, steps_box.get_center() + DOWN * 7.5 + LEFT * 3.5, scale=0.7)
        lines.append(self.create_edge(focusNode.get_bottom(), versNode2.get_center(), GREEN))

        versNode2 = self.create_node("???", "???", "appliedai", GREEN, steps_box.get_center() + DOWN * 9, scale=0.7)
        lines.append(self.create_edge(doorsNode.get_bottom(), versNode2.get_center(), GREEN))

        versNode2 = self.create_node("???", "???", "appliedai", GREEN, steps_box.get_center() + DOWN * 7.5 + LEFT * -3.5, scale=0.7)
        lines.append(self.create_edge(versNode.get_bottom(), versNode2.get_center(), GREEN))

        versNode2 = self.create_node("???", "???", "appliedai", GREEN, steps_box.get_center() + DOWN * 6 + LEFT * -7, scale=0.7)
        lines.append(self.create_edge(focusNode.get_bottom(), versNode2.get_center(), GREEN))

        self.play(*[Create(line) for line in lines], run_time=1)
