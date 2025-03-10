import flet as ft

def containers(page):
    # Define color scheme (placeholders, assuming these are defined in page)
    navy_blue = page.navy_blue if hasattr(page, 'navy_blue') else "#003087"
    yellow = page.yellow if hasattr(page, 'yellow') else "#FFC107"
    grey = page.grey if hasattr(page, 'grey') else "#E0E0E0"
    white = page.white if hasattr(page, 'white') else "#FFFFFF"
    darkgrey = page.darkgrey if hasattr(page, 'darkgrey') else "#616161"

    # Constants for text size and field height
    txt_size = 13
    field_height = 40

    return ft.Column(
        controls=[
            # Course Selection Container
            ft.Container(
                border_radius=15,
                margin=ft.margin.only(10, 0, 10, 0),
                content=ft.Column(
                    spacing=0,
                    controls=[
                        # Header
                        ft.Container(
                            height=40,
                            padding=ft.padding.only(10, 10, 10, 10),
                            bgcolor=navy_blue,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Row(
                                        [ft.Text(":::  เลือกคอร์ส  :::", color=yellow, size=18)],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ]
                            )
                        ),
                        # Course Selection Body
                        ft.Container(
                            bgcolor=grey,
                            padding=ft.padding.only(10, 10, 10, 10),
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text("รหัสนักเรียน :", color=navy_blue, size=txt_size),
                                            ft.Text("", color=navy_blue, size=txt_size)  # Placeholder for student ID
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    ),
                                    ft.Row(
                                        [
                                            ft.Dropdown(
                                                options=[],
                                                bgcolor=white,
                                                expand=True,
                                                label="ห้องเรียน",
                                                value="ทั้งหมด"
                                            ),
                                            ft.Dropdown(
                                                options=[],
                                                bgcolor=white,
                                                expand=True,
                                                label="วันเรียน",
                                                value="ทั้งหมด"
                                            )
                                        ]
                                    ),
                                    ft.Column(
                                        scroll="auto",
                                        height=240,
                                        controls=[]  # Placeholder for course table
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                label="ข้อมูลสรุปการเลือก",
                                                text_size=txt_size,
                                                height=field_height,
                                                expand=True
                                            ),
                                            ft.TextField(
                                                text_size=txt_size,
                                                height=field_height,
                                                visible=False,
                                                expand=True
                                            )  # Hidden field for selected course IDs
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            # Payment Information Container
            ft.Container(
                border_radius=15,
                margin=ft.margin.only(10, 0, 10, 0),
                bgcolor=grey,
                content=ft.Column(
                    controls=[
                        # Header
                        ft.Container(
                            bgcolor=yellow,
                            height=40,
                            padding=ft.padding.only(10, 0, 10, 10),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text(
                                                ":::: ข้อมูลการชำระเงิน ::::",
                                                expand=True,
                                                size=18,
                                                text_align="center"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                        # Payment Info Body
                        ft.Container(
                            padding=ft.padding.only(10, 0, 10, 10),
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                label="Total Cost",
                                                text_size=txt_size,
                                                height=field_height,
                                                expand=False,
                                                width=250
                                            ),
                                            ft.RadioGroup(
                                                content=ft.Row(
                                                    [
                                                        ft.Radio(value="5", label="5%"),
                                                        ft.Radio(value="10", label="10%"),
                                                        ft.Radio(value="15", label="15%"),
                                                        ft.Radio(value="other", label="อื่น")
                                                    ],
                                                    spacing=0
                                                )
                                            ),
                                            ft.TextField(
                                                expand=1,
                                                label="ระบุส่วนลด (บาท)",
                                                text_size=txt_size,
                                                height=field_height,
                                                visible=False
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextField(
                                                label="Discounted Total Cost",
                                                text_size=txt_size,
                                                height=field_height,
                                                width=250
                                            ),
                                            ft.TextField(
                                                expand=True,
                                                label="บันทึกเพิ่มเติม",
                                                text_size=txt_size,
                                                height=field_height
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        ]
    )

# Example usage (for testing purposes)
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(containers(page))
    ft.app(target=main)