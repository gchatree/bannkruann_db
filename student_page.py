import flet as ft

def containers():
    # Define colors and styles
    navy_blue = "#003366"
    yellow = "#FFCC00"
    grey = "#F1F1F1"
    white = "#FFFFFF"
    darkgrey = "#A9A9A9"

    # Student Info Container
    student_info_container = ft.Container(
        margin=ft.margin.only(10, 0, 10, 0),
        padding=0,
        border_radius=15,
        bgcolor=grey,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor=navy_blue,
                    height=40,
                    content=ft.Row(
                        [ft.Text("::: ข้อมูลนักเรียน :::", color=yellow, size=18)],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(10, 0, 10, 10),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                label="รหัสนักเรียน",
                                                value="1234",
                                                read_only=True,
                                                bgcolor=white,
                                                expand=True,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.IconButton(
                                                        icon=ft.icons.SEARCH,
                                                        icon_color=navy_blue,
                                                    ),
                                                    ft.IconButton(
                                                        icon=ft.icons.ADD,
                                                        icon_color=navy_blue,
                                                    ),
                                                ],
                                                spacing=0,
                                                ),
                                        ],
                                        expand=3,
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                text="Edit",
                                                icon="EDIT",
                                                color=yellow,
                                                bgcolor=navy_blue,
                                                icon_color=yellow,
                                            )
                                        ],
                                        expand=1,
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("ชื่อนักเรียน", size=13),
                                            ft.TextField(
                                                value="John",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=2,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("นามสกุล", size=13),
                                            ft.TextField(
                                                value="Doe",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=2,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("ชื่อเล่น", size=13),
                                            ft.TextField(
                                                value="Johnny",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("โรงเรียนประจำ", size=13),
                                            ft.TextField(
                                                value="XYZ School",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=5,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("ระดับชั้น", size=13),
                                            ft.TextField(
                                                value="Grade 10",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=2,
                                        spacing=0,
                                    ),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("หมายเลขโทรศัพท์", size=13),
                                            ft.TextField(
                                                value="123-456-7890",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=True,
                                        spacing=0,
                                    ),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        text="Enroll",
                                        icon="APP_REGISTRATION",
                                        color=yellow,
                                        bgcolor=navy_blue,
                                        icon_color=yellow,
                                        width=150
                                    ),
                                    ft.ElevatedButton(
                                        text="Payment",
                                        icon="PAYMENT",
                                        color=yellow,
                                        bgcolor=navy_blue,
                                        icon_color=yellow,
                                        width = 150
                                    ),
                                ],alignment=ft.MainAxisAlignment.START

                            )
                        ]
                    ),
                ),
            ]
        ),
    )

    # Parent Info Container
    parent_info_container = ft.Container(
        margin=ft.margin.only(10, 0, 10, 0),
        padding=0,
        border_radius=15,
        bgcolor=grey,
        content=ft.Column(
            controls=[
                ft.Container(
                    bgcolor=yellow,
                    height=40,
                    content=ft.Row(
                        [ft.Text("::: ข้อมูลผู้ปกครอง :::", color=navy_blue, size=18)],
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    padding=ft.Padding(10, 0, 10, 10),
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("รหัสผู้ปกครอง: 1234"),
                                    ft.ElevatedButton(
                                        text="Edit",
                                        icon="EDIT",
                                        color=navy_blue,
                                        bgcolor=yellow,
                                        icon_color=navy_blue,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("ชื่อผู้ปกครอง", size=13),
                                            ft.TextField(
                                                value="Jane",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("นามสกุล", size=13),
                                            ft.TextField(
                                                value="Doe",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                ],
                                spacing=5,
                            ),
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text("หมายเลขโทรศัพท์", size=13),
                                            ft.TextField(
                                                value="987-654-3210",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("Line ID", size=13),
                                            ft.TextField(
                                                value="janedoe",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text("Facebook", size=13),
                                            ft.TextField(
                                                value="janedoe",
                                                read_only=True,
                                                bgcolor="#f1f1f1",
                                                height=40,
                                            ),
                                        ],
                                        expand=1,
                                        spacing=0,
                                    ),
                                ],
                                spacing=5,
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )

    # Return the containers as a Column
    return ft.Column(
        controls=[
            student_info_container,
            parent_info_container,
        ],
        spacing=10,
    )
