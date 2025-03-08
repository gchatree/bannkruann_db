import flet as ft
import os
import student_page
import course_page

def main(page: ft.Page):
    # Set page properties
    page.title = "Student Information and Financial Management"
    page.padding = 0
    page.bgcolor = "#f5f5f5"

    # Font definitions - register Thai fonts from assets/fonts folder
    page.fonts = {
        "THNiramit": "fonts/TH Niramit AS.ttf",
        "THFahkwang": "fonts/TH Fahkwang.ttf",
        "THK2DJuly8": "fonts/TH K2D July8.ttf",
        "THMaliGrade6": "fonts/TH Mali Grade6.ttf",
        "THSarabun": "fonts/THSarabun.ttf",
        "Charmonman": "fonts/Charmonman-Regular.ttf"
    }
    
    # Choose which font to use for Thai text - you can change this to any font from the list above
    menu_font = "THFahkwang"
    btn_font = "THSarabun"
    # Local image path
    path = os.path.abspath('')
    logo_path = "/images/bannAnn.png"
    
    # Thai title texts for different pages
    thai_titles = {
        "Home": "ระบบจัดการข้อมูลและการเงิน : Home",
        "Students": "ระบบจัดการข้อมูลและการเงิน : Students",
        "Courses": "ระบบจัดการข้อมูลและการเงิน : Courses",
        "Payment": "ระบบจัดการข้อมูลและการเงิน : Payment",
        "Receipt": "ระบบจัดการข้อมูลและการเงิน : Receipt",
    }
    
    # Current page tracker
    current_page = "Home"
    
    # Function to create content for different pages
    def create_page_content(page_name):
        english_subtitle = f"{page_name} Information and Financial Management" if page_name == "Home" else f"{page_name} Page"
        if page_name == "Home":
            return ft.Container(
                expand=True,
                padding=ft.padding.all(40),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            thai_titles[page_name],
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            english_subtitle,
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=40),  # Spacer
                        ft.Container(
                            content=ft.Image(
                                src=logo_path,  # Use the local image file
                                width=300,
                                height=300,
                            ),
                            alignment=ft.alignment.center,
                        )
                    ]
                )
            )
        elif page_name == "Students":
            # return ft.Column([
            #     ft.Container(content=ft.Text("Student Info 1"), expand=True, bgcolor="#d9d9d9"),
            #     ft.Container(content=ft.Text("Student Info 2"), expand=True, bgcolor="#b3b3b3"),
            # ])
            return student_page.containers(page)
        
        elif page_name == "Courses":
            # return ft.Column([
            #     ft.Row([
            #         ft.Container(ft.TextField(label="Course 1"), expand=True),
            #         ft.Container(ft.ElevatedButton(text="Submit"), expand=False)
            #     ]),
            #     ft.Row([
            #         ft.Container(ft.TextField(label="Course 2"), expand=True),
            #         ft.Container(ft.ElevatedButton(text="Submit"), expand=False)
            #     ]),
            #     ft.Row([
            #         ft.Container(ft.TextField(label="Course 3"), expand=True),
            #         ft.Container(ft.ElevatedButton(text="Submit"), expand=False)
            #     ]),
            # ])
            return course_page.containers(page)
        
        elif page_name == "Payment":
            return ft.Column([
                ft.Container(content=ft.Text("Payment Section 1"), expand=True, bgcolor="black"),
                ft.Container(content=ft.Text("Payment Section 2"), expand=True, bgcolor="yellow"),
            ])
        
        elif page_name == "Receipt":
            return ft.Container(content=ft.Text("Receipt", size=20, text_align="center"), alignment=ft.alignment.center)
        
        return ft.Container()




    
    # Create content containers for each page
    home_content = create_page_content("Home")
    students_content = create_page_content("Students")
    courses_content = create_page_content("Courses")
    payment_content = create_page_content("Payment")
    receipt_content = create_page_content("Receipt")
    
    # Container to hold the current page content
    content_container = ft.Container(
        expand=True,
        content=home_content  # Default to home content
    )
    
    # Function to change the current page
    def change_page(e, page_name):
        nonlocal current_page
        
        # Update the current page
        current_page = page_name
        
        # Update the content container
        if page_name == "Home":
            content_container.content = home_content
        elif page_name == "Students":
            content_container.content = students_content
        elif page_name == "Courses":
            content_container.content = courses_content
        elif page_name == "Payment":
            content_container.content = payment_content
        elif page_name == "Receipt":
            content_container.content = receipt_content
        
        # Update all menu buttons' selected state
        for button in sidebar.content.controls[1:]:  # Skip the logo container
            text = button.content.controls[1].value
            is_selected = text == page_name
            button.bgcolor = "#f0ca64" if is_selected else "transparent"
            button.content.controls[0].color = "#0f172a" if is_selected else "#f0ca64"
            button.content.controls[1].color = "#0f172a" if is_selected else "#f0ca64"
        
        # Update the page
        page.update()
    
    # Create menu button factory function
    def create_menu_button(icon, text, is_selected=False):
        bg_color = "#f0ca64" if is_selected else "transparent"
        text_color = "#0f172a" if is_selected else "#f0ca64"
        icon_color = "#0f172a" if is_selected else "#f0ca64"
        
        return ft.Container(
            bgcolor=bg_color,
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.only(left=20, right=20, top=15, bottom=15),
            margin=ft.margin.only(left=10, right=10),
            content=ft.Row([
                ft.Icon(icon, color=icon_color),
                ft.Text(text, 
                        color=text_color, 
                        #weight=ft.FontWeight.BOLD,
                        #font_family = btn_font,

                ),
            ]),
            on_click=lambda e: change_page(e, text),
            ink=True,  # Add ripple effect on click
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )

    # Create the sidebar
    sidebar = ft.Container(
        width=320,
        height=page.height,
        bgcolor="#0f172a",
        padding=ft.padding.only(top=20),
        content=ft.Column(
            spacing=10,
            controls=[
                # School logo and name
                ft.Container(
                    padding=ft.padding.only(left=20, bottom=20),
                    content=ft.Row([
                        ft.Image(
                            src=logo_path,  # Use the same logo image here
                            width=40,
                            height=40,
                            border_radius=ft.border_radius.all(20),
                        ),
                        ft.Text(
                            "โรงเรียนกวดวิชาบ้านครูแอน",
                            color="white",
                            size=20,
                            font_family=menu_font,
                        )
                    ])
                ),
                
                # Menu buttons - using ft.Icons
                create_menu_button(ft.Icons.HOME, "Home", is_selected=True),
                create_menu_button(ft.Icons.PERSON, "Students"),
                create_menu_button(ft.Icons.SCHOOL, "Courses"),
                create_menu_button(ft.Icons.CREDIT_CARD, "Payment"),
                create_menu_button(ft.Icons.RECEIPT, "Receipt"),
            ]
        )
    )
    
    # Create the overall layout
    page.add(
        ft.Row(
            spacing=0,
            controls=[
                sidebar,
                ft.VerticalDivider(width=1, color="#e0e0e0"),
                content_container,
            ],
            expand=True,
        )
    )

ft.app(target=main,assets_dir='assets')
# ft.app(target=main,assets_dir='assets',view = 'flet_app_web', port=8888)