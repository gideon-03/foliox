import flet as ft
import base64
import os


def get_icon(name: str):
    icons = getattr(ft, "Icons", None) or getattr(ft, "icons")
    return getattr(icons, name)


def load_image_base64(path: str) -> str:
    # Build absolute path relative to THIS script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(base_dir, path)
    
    print(f"[DEBUG] Looking for: {abs_path}")  # ← shows in terminal
    print(f"[DEBUG] Exists: {os.path.exists(abs_path)}")
    
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    print(f"[ERROR] Image not found: {abs_path}")
    return ""


def main(page: ft.Page):
    page.clean()
    page.title = "Engineering Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0d0221"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    primary   = "#00d9ff"
    secondary = "#7b2cbf"
    card      = "#1b0a3a"
    panel     = "#12032c"
    text      = "#ffffff"
    subtext   = "#c2c2c2"

    def symmetric_padding(horizontal: int, vertical: int):
        return ft.Padding(horizontal, vertical, horizontal, vertical)

    def border_all(width: int, color: str):
        side = ft.BorderSide(width=width, color=color)
        return ft.Border(top=side, right=side, bottom=side, left=side)

    async def open_route(route: str):
        await page.push_route(route)

    def nav_link(label: str, section_key: str):
      if section_key == "github":
        return ft.Button(
            label,
            color=text,
            bgcolor=panel,
            elevation=0,
            height=36,
            on_click=lambda _: __import__('webbrowser').open("https://github.com/gideon-03"),
            style=ft.ButtonStyle(
                padding=ft.Padding(8, 6, 8, 6),
                text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
            ),
         )
      route = "/" if section_key == "home" else f"/{section_key}"
      return ft.Button(
        label,
        color=text,
        bgcolor=panel,
        elevation=0,
        height=36,
        on_click=lambda _: page.run_task(open_route, route),
        style=ft.ButtonStyle(
            padding=ft.Padding(8, 6, 8, 6),
            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
        ),
    )
    def section_title(label: str, title: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(label, size=14, color=primary, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=42, weight=ft.FontWeight.BOLD, color=text),
            ],
        )

    def feature_card(title: str, description: str, icon_name: str):
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=28,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Icon(get_icon(icon_name), size=38, color=primary),
                    ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(description, size=16, color=subtext),
                ],
            ),
        )

    def stat_card(number: str, label: str):
        return ft.Container(
            bgcolor=card,
            padding=26,
            border_radius=12,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(number, size=38, weight=ft.FontWeight.BOLD, color=primary),
                    ft.Text(label, size=17, color=subtext),
                ],
            ),
        )

    # ─────────────────────────────────────────────
    # ALL 8 CERTIFICATES
    # image_path points to the PNG file next to main.py
    # ─────────────────────────────────────────────
    certificates = [
        {
            "title": "MATLAB Onramp",
            "date": "3 April 2026",
            "description": "Completed the official MathWorks MATLAB Onramp course.",
            "image_path": "assets/matlab_onramp.png",
            "tag": "Onramp",
        },
        {
            "title": "Simulink Onramp",
            "date": "20 April 2026",
            "description": "Completed the official MathWorks Simulink Onramp course.",
            "image_path": "assets/simulink_onramp.png",
            "tag": "Onramp",
        },
        {
            "title": "Machine Learning Onramp",
            "date": "23 April 2026",
            "description": "Completed the MathWorks Machine Learning Onramp course.",
            "image_path": "assets/machine_learning.png",
            "tag": "Onramp",
        },
        {
            "title": "Core MATLAB Skills",
            "date": "23 April 2026",
            "description": "Completed the full Core MATLAB Skills learning path (4 courses).",
            "image_path": "assets/core_matlab.png",
            "tag": "Learning Path",
        },
        {
            "title": "MATLAB Desktop Tools",
            "date": "20 April 2026",
            "description": "Completed MATLAB Desktop Tools and Troubleshooting Scripts.",
            "image_path": "assets/matlab_desktop.png",
            "tag": "Course",
        },
        {
            "title": "Explore Data with MATLAB Plots",
            "date": "22 April 2026",
            "description": "Completed Explore Data with MATLAB Plots course.",
            "image_path": "assets/explore_data.png",
            "tag": "Course",
        },
        {
            "title": "Make and Manipulate Matrices",
            "date": "22 April 2026",
            "description": "Completed Make and Manipulate Matrices course.",
            "image_path": "assets/make_matrices.png",
            "tag": "Course",
        },
        {
            "title": "Calculations with Vectors and Matrices",
            "date": "23 April 2026",
            "description": "Completed Calculations with Vectors and Matrices course.",
            "image_path": "assets/calc_vectors.png",
            "tag": "Course",
        },
    ]

   # ─────────────────────────────────────────────
    # CERTIFICATE VIEWER DIALOG
    # ─────────────────────────────────────────────

    cert_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=card,
        actions=[
            ft.TextButton(
                "Close",
                style=ft.ButtonStyle(color=primary),
                on_click=lambda _: close_dialog(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_dialog():
        cert_dialog.open = False
        page.update()

    def open_cert(cert: dict):
        b64 = load_image_base64(cert["image_path"])

        cert_dialog.title = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Text(cert["title"], size=20, weight=ft.FontWeight.BOLD,
                        color=primary, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Completed: {cert['date']}", size=14,
                        color=subtext, text_align=ft.TextAlign.CENTER),
            ],
        )

        cert_dialog.content = ft.Container(
            width=700,
            height=470,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=f"data:image/png;base64,{b64}",  # ✅ data URI works in all versions
                fit=ft.BoxFit.CONTAIN,
                width=680,
                height=460,
            ) if b64 else ft.Text("Image not found", color="red"),
        )

        cert_dialog.open = True
        if cert_dialog not in page.overlay:
            page.overlay.append(cert_dialog)
        page.update()
    # ─────────────────────────────────────────────
    # TAG COLOR HELPER
    # ─────────────────────────────────────────────
    def tag_color(tag: str) -> str:
        return {
            "Onramp":        "#00d9ff",
            "Learning Path": "#7b2cbf",
            "Course":        "#00b894",
        }.get(tag, primary)

    # ─────────────────────────────────────────────
    # CERTIFICATE CARD
    # ─────────────────────────────────────────────
    def cert_card(cert: dict):
        tc = tag_color(cert["tag"])
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=22,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    # Tag badge
                    ft.Container(
                        bgcolor="#0d0221",
                        border_radius=20,
                        padding=ft.Padding(10, 4, 10, 4),
                        border=border_all(1, tc),
                        content=ft.Text(
                            cert["tag"],
                            size=11,
                            color=tc,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    ft.Icon(get_icon("VERIFIED"), size=34, color=primary),
                    ft.Text(cert["title"], size=17, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(cert["description"], size=13, color=subtext),
                    ft.Text(cert["date"], size=12, color=primary, italic=True),
                    ft.ElevatedButton(
                        "View Certificate",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, c=cert: open_cert(c),
                        style=ft.ButtonStyle(
                            padding=ft.Padding(10, 6, 10, 6),
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                ],
            ),
        )

    # ─────────────────────────────────────────────
    # NAV BAR
    # ─────────────────────────────────────────────
    nav_items = [
        ("HOME",     "home"),
        ("ABOUT",    "about"),
        ("TIMELINE", "timeline"),
        ("MATLAB",   "matlab"),
        ("BLOG",     "blog"),
        ("GITHUB",   "github"),
        ("CONTACT",  "contact"),
    ]
    page.appbar = ft.AppBar(
        title=ft.Text("FolioX", size=28, weight=ft.FontWeight.BOLD, color=primary),
        bgcolor=panel,
        toolbar_height=76,
        actions=[nav_link(label, key) for label, key in nav_items],
        actions_padding=ft.Padding(0, 0, 28, 0),
    )

    # ─────────────────────────────────────────────
    # HERO
    # ─────────────────────────────────────────────
    hero_section = ft.Container(
        key="home",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        ft.Text("WELCOME", size=18, color=secondary, weight=ft.FontWeight.BOLD),
                        ft.Text("Kandjengo Gideon", size=58, weight=ft.FontWeight.BOLD, color=text),
                        ft.Text("Python Developer | OreGuide App | Unam Engineering Student", size=24, color=subtext),
                        ft.Row(
                            spacing=16,
                            wrap=True,
                            controls=[
                                ft.Button("Hire Me", bgcolor=primary, color="#000000",
                                          on_click=lambda _: page.run_task(open_route, "/contact")),
                                ft.Button("View Projects",
                                          style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                          on_click=lambda _: page.run_task(open_route, "/timeline")),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=340, height=340, border_radius=170,
                            border=border_all(5, primary),
                            image=ft.DecorationImage(src="profile.jpg", fit=ft.BoxFit.COVER),
                        )
                    ],
                ),
            ],
        ),
    )

    features = ft.Container(
    padding=symmetric_padding(horizontal=40, vertical=30),
    content=ft.ResponsiveRow(
        run_spacing=20,
        controls=[
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Python & Flet Development",
                "Built the ore display module and portfolio web app using Python and the Flet framework.",
                "CODE"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Firebase Integration",
                "Connected the app to Firebase Storage and Firestore to fetch and display ore data dynamically.",
                "CLOUD"
            )]),
            ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                "Mining & Metallurgy Module",
                "Contributed to the ore recognition system serving Mining and Metallurgical engineering students.",
                "TERRAIN"
            )]),
        ],
    ),
)
    # ─────────────────────────────────────────────
    # ABOUT
    # ─────────────────────────────────────────────
    about_section = ft.Container(
        key="about",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.ResponsiveRow(
            run_spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    controls=[
                        ft.Image(
                            src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1000&q=80",
                            border_radius=12, fit=ft.BoxFit.COVER, height=360, width=620,
                        )
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        section_title("ABOUT ME", "A Passionate Developer Who Loves To Code"),
                        ft.Text(
                                 "I am a third year extended program Engineering student at Unam. As part of my Computer Programming I module "
                                 "I contributed to building an Ore Recognition App with a team of 17 students. My role focused "
                                 "on the ore display module, Firebase integration, and this individual web portfolio built with Python and Flet.",
                        size=18, color=subtext,
            ),
                    ],
                ),
            ],
        ),
    )

    stats = ft.Container(
        padding=symmetric_padding(horizontal=40, vertical=30),
        content=ft.ResponsiveRow(
            run_spacing=20,
            controls=[
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("1",  "Project")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("6", "Commits")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("280",  "Lines of Code")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("8",   "Certificates")]),
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # TIMELINE
    # ─────────────────────────────────────────────
    timeline_cards = [
       (
        "Week 1: Project Ideation & Team Formation",
        "Our team of 17 members met for the first time to brainstorm project ideas. We proposed multiple engineering applications and evaluated each based on feasibility, relevance, and impact. After thorough discussion we agreed on building an Ore Recognition App that uses image processing to identify and classify mineral ores — a practical tool for the Mining and Metallurgical engineering modules."
    ),
       (
        "Week 2: Software Requirements Specification",
        "The team collaborated to write the Software Requirements Specification (SRS) document. This included defining functional and non-functional requirements, system architecture, user stories, and module breakdown. My personal contribution was drafting the requirements for the ore classification module and the user interface section of the SRS."
    ),
       (
        "Week 3: Engineering Calculator Implementation",
        "I implemented the engineering calculators for the app, covering key formulas used in metallurgical and mining engineering. This included ore grade calculations, recovery rate formulas, and material cost estimations. Each calculator was built with input validation, error handling, and a results display to ensure accuracy and usability for engineering students."
    ),
       (
        "Week 4: Ore Display Module & Firebase Integration",
        "The team was divided into smaller sub-groups with each member assigned individual tasks. I was placed in a group of two and we were assigned the responsibility of building the Ore Display module for the app. Our work involved setting up Firebase as the backend storage solution to host ore images and their associated data. We configured Firebase Storage and Firestore database, connected it to the app, and built the UI to fetch and display the ores dynamically. Once our module was fully tested and working, we pushed our code to the main repository via a pull request, ensuring our changes were reviewed and successfully merged into the group project."
    ),
    ]
    timeline_section = ft.Container(
        key="timeline",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Project Timeline", size=42, weight=ft.FontWeight.BOLD, color=text),
                *[
                    ft.Container(
                        bgcolor=card, padding=24, border_radius=12, border=border_all(1, primary),
                        content=ft.Column(spacing=8, controls=[
                            ft.Text(week, size=23, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(description, color=subtext, size=16),
                        ]),
                    )
                    for week, description in timeline_cards
                ],
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # MATLAB SECTION — all 8 certificates
    # ─────────────────────────────────────────────
    matlab_section = ft.Container(
        key="matlab",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("MATLAB Achievement Hub", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "All 8 MathWorks certificates earned by Gideon Kandjengo — click any card to view the full certificate.",
                    size=16, color=subtext,
                ),
                # Row 1 — Onramps (3 cards)
                ft.Text("Onramp Certificates", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[0])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[1])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[2])]),
                    ],
                ),
                # Row 2 — Learning path + individual courses (5 cards)
                ft.Text("Core MATLAB Skills — Learning Path & Courses", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[3])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[4])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[5])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[6])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[7])]),
                    ],
                ),
            ],
        ),
    )

# ─────────────────────────────────────────────
    # BLOG
    # ─────────────────────────────────────────────
    blog_section = ft.Container(
        key="blog",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("Technical Blog", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Confidence in Concepts — written technical explanations with video inserts.",
                        size=16, color=subtext),

                # ── Post 1 ──
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("CODE"), size=38, color=primary),
                            ft.Text("Confidence in Python OOP", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Object Oriented Programming (OOP) is a programming approach that "
                                "organises code into classes and objects. A class is like a blueprint "
                                "and an object is an instance of that blueprint. For example in our "
                                "Ore Recognition App, we created a class called Ore that holds "
                                "properties like name, colour, and hardness.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "The three main pillars of OOP are inheritance, encapsulation and "
                                "polymorphism. Inheritance allows a child class to reuse code from a "
                                "parent class. Encapsulation hides internal data from outside access. "
                                "Polymorphism allows different classes to be used through the same "
                                "interface. We applied these concepts throughout our group project.",
                                size=15, color=subtext,
                            ),
                            ft.Text("Watch: Python OOP Explained", size=13,
                                    color=primary, italic=True),
                            ft.ElevatedButton(
                                "▶ Watch Video",
                                bgcolor=primary,
                                color="#000000",
                                on_click=lambda _: __import__('webbrowser').open(
                                    "https://www.youtube.com/watch?v=JeznW_7DlB0"
                                ),
                            ),
                        ],
                    ),
                ),

                # ── Post 2 ──
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("STORAGE"), size=38, color=primary),
                            ft.Text("Understanding Data Structures", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Data structures are ways of organising and storing data in a program "
                                "so that it can be accessed and modified efficiently. The most common "
                                "data structures in Python are lists, stacks, queues and linked lists. "
                                "Choosing the right data structure is important because it directly "
                                "affects the performance of your application.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "A stack follows a Last In First Out (LIFO) principle — the last item "
                                "added is the first to be removed, like a stack of plates. A queue "
                                "follows First In First Out (FIFO) — like a line of people waiting. "
                                "A linked list stores data in nodes where each node points to the next. "
                                "In our Ore Recognition App we used lists and dictionaries to store "
                                "ore data fetched from Firebase before displaying it to the user.",
                                size=15, color=subtext,
                            ),
                            ft.Text("Watch: Data Structures Explained", size=13,
                                    color=primary, italic=True),
                            ft.ElevatedButton(
                                "▶ Watch Video",
                                bgcolor=primary,
                                color="#000000",
                                on_click=lambda _: __import__('webbrowser').open(
                                    "https://www.youtube.com/watch?v=pkYVOmU3MgA"
                                ),
                            ),
                        ],
                    ),
                ),

                # ── Mathematical Notation ──
                ft.Container(
                    bgcolor=card,
                    padding=28,
                    border_radius=12,
                    border=border_all(1, primary),
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Icon(get_icon("FUNCTIONS"), size=38, color=primary),
                            ft.Text("Mathematical Notation", size=30,
                                    weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(
                                "When calculating the total material cost in mining operations, "
                                "we sum the product of quantity and price for each ore type:",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "Total Cost = Σ (Qi × Pi) + Overheads",
                                size=26, color=text, weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Where Qi is the quantity of ore i, Pi is the price per unit of ore i, "
                                "and Overheads covers fixed operational costs such as labour and equipment.",
                                size=15, color=subtext,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # GITHUB
    # ─────────────────────────────────────────────
    github_section = ft.Container(
        key="github",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("GitHub Evidence", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card("Commit History", "Screenshots and GitHub API commit tracking.", "HISTORY")]),
                        ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card("Pull Requests", "Reviews, approvals and merge evidence.", "MERGE_TYPE")]),
                        ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card("Impact Summary", "Explain engineering problems solved using your code.", "INSIGHTS")]),
                    ],
                ),
            ],
        ),
    )

    # ─────────────────────────────────────────────
    # CONTACT
    # ─────────────────────────────────────────────
    contact_section = ft.Container(
        key="contact",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Contact Me", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Available for freelance work and engineering projects.", size=18, color=subtext, text_align=ft.TextAlign.CENTER),
                ft.TextField(width=500, label="Your Name",  bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, label="Your Email", bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, min_lines=4, max_lines=6, multiline=True, label="Message", bgcolor=card, border_color=primary, color=text),
                ft.Button("Send Message", bgcolor=primary, color="#000000"),
            ],
        ),
    )

    footer = ft.Container(
        padding=30,
        alignment=ft.Alignment.CENTER,
        content=ft.Text("(c) 2026 Kandjengo Gideon Portfolio - All Rights Reserved", color=subtext),
    )

    # ─────────────────────────────────────────────
    # ROUTING
    # ─────────────────────────────────────────────
    pages = {
        "home":     [hero_section, features],
        "about":    [about_section, stats],
        "timeline": [timeline_section],
        "matlab":   [matlab_section],
        "blog":     [blog_section],
        "github":   [github_section],
        "contact":  [contact_section],
    }

    def render_route(_=None):
        section  = page.route.strip("/") or "home"
        controls = pages.get(section, pages["home"])
        page.controls.clear()
        page.add(ft.Column(spacing=0, controls=[*controls, footer]))
        page.update()

    page.on_route_change = render_route
    render_route()


if __name__ == "__main__":
    ft.run(main, web_renderer=ft.WebRenderer.CANVAS_KIT)