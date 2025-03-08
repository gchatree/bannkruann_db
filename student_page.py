import flet as ft
import sqlite3
import json

def Exec_Sql(sql):
    conn = sqlite3.connect("Bannkruann.db")
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    if len(result) > 0:
        attb = [d[0] for d in c.description]
        jsonlist = [dict(zip(attb, item)) for item in result]
    else:
        jsonlist = result
    conn.commit()
    conn.close()
    return jsonlist

def containers(page):
    # Define colors and styles
    navy_blue = "#003366"
    yellow = "#FFCC00"
    grey = "#F1F1F1"
    white = "#FFFFFF"
    darkgrey = "#A9A9A9"

    # Fetch initial data from the database
    student_sql = "SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID ORDER BY S.S_ID DESC"
    parent_sql = "SELECT * FROM Parent ORDER BY P_ID DESC"
    student_data = Exec_Sql(student_sql)
    parent_data = Exec_Sql(parent_sql)

    # Use the first student record as the default display (or handle empty case)
    current_student = student_data[0] if student_data else None

    # Student ID input field with on_submit event
    student_id_input = ft.TextField(
        label="รหัสนักเรียน",
        value=str(current_student["S_ID"]) if current_student else "",
        bgcolor=white,
        expand=True,
        on_submit=lambda e: search_student(e),
    )

    # Search input field
    search_input = ft.TextField(
        label="ค้นหา: ชื่อ นามสกุล หรือ ชื่อเล่น",
        bgcolor=white,
        on_change=lambda e: update_search_results(e.control.value)
    )

    # Container for search results
    search_results = ft.Column(expand=True, scroll="auto")

    # Containers to hold dynamic content
    student_info_content = ft.Container()
    parent_info_content = ft.Container()

    # Function to display student info dynamically
    def display_student_info(student):
        if student:
            student_info_content.content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                [
                                    student_id_input,
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.icons.SEARCH,
                                                icon_color=navy_blue,
                                                on_click=lambda e: toggle_search_panel()
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.ADD,
                                                icon_color=navy_blue,
                                                on_click=lambda e: add_student_dialog(e)
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
                    search_input,  # Inline search field
                    search_results,  # Inline search results
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("ชื่อนักเรียน", size=13),
                                    ft.TextField(
                                        value=student["Name"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["SurName"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["Nick"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["School"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["Class"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["S_Tel"],
                                        read_only=True,
                                        bgcolor=white,
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
                                width=150
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )
                ]
            )
            parent_info_content.content = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"รหัสผู้ปกครอง: {student['P_ID']}"),
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
                                        value=student["M_Name"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["M_SurName"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["M_Tel"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["line"],
                                        read_only=True,
                                        bgcolor=white,
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
                                        value=student["facebook"],
                                        read_only=True,
                                        bgcolor=white,
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
                                    ft.Text("บ้านเลขที่", size=13),
                                    ft.TextField(
                                        value=student["H_Adr"],
                                        read_only=True,
                                        bgcolor=white,
                                        height=40,
                                    ),
                                ],
                                expand=1,
                                spacing=0,
                            ),
                            ft.Column(
                                [
                                    ft.Text("หมู่", size=13),
                                    ft.TextField(
                                        value=student["H_Mu"],
                                        read_only=True,
                                        bgcolor=white,
                                        height=40,
                                    ),
                                ],
                                expand=1,
                                spacing=0,
                            ),
                            ft.Column(
                                [
                                    ft.Text("ตำบล", size=13),
                                    ft.TextField(
                                        value=student["H_Tum"],
                                        read_only=True,
                                        bgcolor=white,
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
                                    ft.Text("อำเภอ", size=13),
                                    ft.TextField(
                                        value=student["H_Amp"],
                                        read_only=True,
                                        bgcolor=white,
                                        height=40,
                                    ),
                                ],
                                expand=1,
                                spacing=0,
                            ),
                            ft.Column(
                                [
                                    ft.Text("จังหวัด", size=13),
                                    ft.TextField(
                                        value=student["H_Prov"],
                                        read_only=True,
                                        bgcolor=white,
                                        height=40,
                                    ),
                                ],
                                expand=1,
                                spacing=0,
                            ),
                            ft.Column(
                                [
                                    ft.Text("รหัสไปรษณีย์", size=13),
                                    ft.TextField(
                                        value=student["H_Post"],
                                        read_only=True,
                                        bgcolor=white,
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
            )
            page.update()

    # Search student by ID when Enter is pressed
    def search_student(e):
        student_id = student_id_input.value.strip()
        if not student_id:
            student_info_content.content = ft.Text("กรุณากรอกรหัสนักเรียน")
            parent_info_content.content = ft.Text("")
            page.update()
            return

        sql = f"SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID AND S.S_ID = {student_id}"
        result = Exec_Sql(sql)
        student = result[0] if result else None

        if student:
            display_student_info(student)
        else:
            student_info_content.content = ft.Text("ไม่พบข้อมูลนักเรียน")
            parent_info_content.content = ft.Text("")
            page.update()

    # Toggle search panel visibility
    def toggle_search_panel():
        search_input.visible = not search_input.visible
        search_results.visible = not search_results.visible
        if search_input.visible:
            update_search_results('')
        else:
            search_results.controls.clear()
        page.update()

    # Update search results inline
    def update_search_results(search_text):
        search_results.controls.clear()
        for item in student_data:
            if (search_text in item['Name']) or (search_text in item['SurName']) or (search_text in item['Nick']):
                search_results.controls.append(
                    ft.Row(
                        [
                            ft.TextButton(
                                text=f"{item['Name']} {item['SurName']} ({item['Nick']}) - ID: {item['S_ID']}",
                                on_click=lambda e, s_id=item['S_ID']: select_student(s_id)
                            )
                        ]
                    )
                )
        page.update()

    # Select a student from search results
    def select_student(s_id):
        student_id_input.value = s_id
        student = next((s for s in student_data if s["S_ID"] == s_id), None)
        if student:
            display_student_info(student)
        search_input.visible = False
        search_results.visible = False
        search_results.controls.clear()
        page.update()

    # Add student dialog function (unchanged from previous)
    def add_student_dialog(e):
        def close_dialog(e):
            dialog.open = False
            page.update()

        def save_student(e):
            new_s_id = max([int(s["S_ID"]) for s in student_data]) + 1 if student_data else 1
            new_p_id = max([int(p["P_ID"]) for p in parent_data]) + 1 if parent_data else 1
            new_student = {
                "S_ID": new_s_id,
                "Name": name_input.value,
                "SurName": surname_input.value,
                "Nick": nick_input.value,
                "P_ID": new_p_id,
                "School": school_input.value,
                "Class": class_input.value,
                "S_Tel": s_tel_input.value,
                "M_Tel": m_tel_input.value,
                "M_Name": m_name_input.value,
                "M_SurName": m_surname_input.value,
                "line": line_input.value,
                "facebook": facebook_input.value,
                "H_Adr": h_adr_input.value,
                "H_Mu": h_mu_input.value,
                "H_Tum": h_tum_input.value,
                "H_Amp": h_amp_input.value,
                "H_Prov": h_prov_input.value,
                "H_Post": h_post_input.value,
            }
            student_sql = f"INSERT INTO Student (S_ID, Name, SurName, Nick, P_ID, School, Class, S_Tel) VALUES ({new_s_id}, '{name_input.value}', '{surname_input.value}', '{nick_input.value}', {new_p_id}, '{school_input.value}', '{class_input.value}', '{s_tel_input.value}')"
            parent_sql = f"INSERT INTO Parent (P_ID, M_Tel, M_Name, M_SurName, line, facebook, H_Adr, H_Mu, H_Tum, H_Amp, H_Prov, H_Post) VALUES ({new_p_id}, '{m_tel_input.value}', '{m_name_input.value}', '{m_surname_input.value}', '{line_input.value}', '{facebook_input.value}', '{h_adr_input.value}', '{h_mu_input.value}', '{h_tum_input.value}', '{h_amp_input.value}', '{h_prov_input.value}', '{h_post_input.value}')"
            Exec_Sql(student_sql)
            Exec_Sql(parent_sql)
            
            student_data[:] = Exec_Sql("SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID ORDER BY S.S_ID DESC")
            display_student_info(new_student)
            dialog.open = False
            page.update()

        name_input = ft.TextField(label="ชื่อนักเรียน", bgcolor=white)
        surname_input = ft.TextField(label="นามสกุล", bgcolor=white)
        nick_input = ft.TextField(label="ชื่อเล่น", bgcolor=white)
        school_input = ft.TextField(label="โรงเรียนประจำ", bgcolor=white)
        class_input = ft.TextField(label="ระดับชั้น", bgcolor=white)
        s_tel_input = ft.TextField(label="หมายเลขโทรศัพท์", bgcolor=white)
        m_name_input = ft.TextField(label="ชื่อผู้ปกครอง", bgcolor=white)
        m_surname_input = ft.TextField(label="นามสกุล", bgcolor=white)
        m_tel_input = ft.TextField(label="หมายเลขโทรศัพท์ผู้ปกครอง", bgcolor=white)
        line_input = ft.TextField(label="Line ID", bgcolor=white)
        facebook_input = ft.TextField(label="Facebook", bgcolor=white)
        h_adr_input = ft.TextField(label="บ้านเลขที่", bgcolor=white)
        h_mu_input = ft.TextField(label="หมู่", bgcolor=white)
        h_tum_input = ft.TextField(label="ตำบล", bgcolor=white)
        h_amp_input = ft.TextField(label="อำเภอ", bgcolor=white)
        h_prov_input = ft.TextField(label="จังหวัด", bgcolor=white)
        h_post_input = ft.TextField(label="รหัสไปรษณีย์", bgcolor=white)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("เพิ่มนักเรียนใหม่"),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row([name_input, surname_input, nick_input], spacing=5),
                        ft.Row([school_input, class_input], spacing=5),
                        ft.Row([s_tel_input], spacing=5),
                        ft.Row([m_name_input, m_surname_input], spacing=5),
                        ft.Row([m_tel_input, line_input, facebook_input], spacing=5),
                        ft.Row([h_adr_input, h_mu_input, h_tum_input], spacing=5),
                        ft.Row([h_amp_input, h_prov_input, h_post_input], spacing=5),
                    ]
                ),
                width=600,
                height=400,
            ),
            actions=[
                ft.Row(
                    [
                        ft.ElevatedButton("Cancel", icon="CANCEL", color=navy_blue, bgcolor=grey, on_click=close_dialog),
                        ft.ElevatedButton("Save", icon="SAVE", color=yellow, bgcolor=navy_blue, on_click=save_student),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Initial display of the first student
    if current_student:
        display_student_info(current_student)

    # Hide search panel initially
    search_input.visible = False
    search_results.visible = False

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
                student_info_content,
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
                parent_info_content,
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

# Example usage
def main(page: ft.Page):
    page.add(containers(page))

if __name__ == "__main__":
    ft.app(target=main)