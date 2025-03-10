import flet as ft
import sqlite3

# Database execution function
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

def max_id(data, id_name):
    maxitem = None
    maxvalue = -1
    for s in data:
        if int(s[id_name]) > maxvalue:
            maxvalue = int(s[id_name])
            maxitem = s
    return maxitem

def containers(page):
    # Define color scheme
    navy_blue = "#003087"
    yellow = "#FFC107"
    grey = "#E0E0E0"
    white = "#FFFFFF"
    darkgrey = "#616161"

    # Constants for text size and field height
    txt_size = 13
    field_height = 40

    # Fetch student data from the database
    student_sql = "SELECT S_ID, Name, SurName, Nick FROM Student ORDER BY S_ID DESC"
    student_data = Exec_Sql(student_sql)

    # Select the student with the maximum S_ID (last student)
    last_student = max_id(student_data, "S_ID") if student_data else None

    # Variables to hold student info
    student_id_text = ft.Text(
        str(last_student["S_ID"]) if last_student else "1234",
        color=navy_blue,
        size=txt_size
    )
    name_text = ft.Text(
        last_student["Name"] if last_student else "เด็กชาย",
        color=navy_blue,
        size=txt_size
    )
    surname_text = ft.Text(
        last_student["SurName"] if last_student else "นามสกุล",
        color=navy_blue,
        size=txt_size
    )
    nickname_text = ft.Text(
        last_student["Nick"] if last_student else "ชื่อเล่น",
        color=navy_blue,
        size=txt_size
    )

    # Search input field for filtering students
    search_input = ft.TextField(
        label="ค้นหา: ชื่อ นามสกุล หรือ ชื่อเล่น",
        bgcolor=white,
        visible=False,
        on_change=lambda e: update_search_results(e.control.value)
    )

    # Search results container
    search_results = ft.Column(visible=False, scroll="auto", height=150)

    # Fetch course data from the database
    course_sql = "SELECT C_ID, Class, Day, Period, Subject, Cost FROM Course ORDER BY C_ID"
    course_data = Exec_Sql(course_sql)
    filtered_course_data = course_data.copy()

    # Track selected courses
    selected_course_ids = set()

    # Populate dropdown options from course data
    class_options = sorted(list(set(course["Class"] for course in course_data if course["Class"])))
    day_options = sorted(list(set(course["Day"] for course in course_data if course["Day"])))

    # Dropdowns for filtering courses
    class_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("ทั้งหมด")] + [ft.dropdown.Option(opt) for opt in class_options],
        bgcolor=white,
        expand=True,
        width=250,
        label="ห้องเรียน",
        value="ทั้งหมด",
        on_change=lambda e: filter_courses()
    )
    day_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("ทั้งหมด")] + [ft.dropdown.Option(opt) for opt in day_options],
        bgcolor=white,
        expand=True,
        width=250,
        label="วันเรียน",
        value="ทั้งหมด",
        on_change=lambda e: filter_courses()
    )

    # Course table
    course_table = ft.ListView(
        controls=[ft.DataTable(
            column_spacing=5,
            columns=[
                ft.DataColumn(ft.Text("")),  # Checkbox column
                ft.DataColumn(ft.Text("รหัสคอร์ส", size=txt_size)),
                ft.DataColumn(ft.Text("ห้องเรียน", size=txt_size)),
                ft.DataColumn(ft.Text("วัน", size=txt_size)),
                ft.DataColumn(ft.Text("ช่วงเวลา", size=txt_size)),
                ft.DataColumn(ft.Text("วิชา", size=txt_size)),
                ft.DataColumn(ft.Text("ราคา", size=txt_size)),
            ],
            rows=[]
        )],
        expand=True,
        height=240,
        auto_scroll=True
    )

    # Functions for search functionality
    def toggle_search_panel():
        search_input.visible = not search_input.visible
        search_results.visible = not search_results.visible
        if search_input.visible:
            search_input.value = ""
            update_search_results("")
        else:
            search_results.controls.clear()
        page.update()

    def update_search_results(search_text):
        search_results.controls.clear()
        if not student_data:
            search_results.controls.append(ft.Text("ไม่มีข้อมูลนักเรียนในฐานข้อมูล"))
        else:
            filtered_students = [
                s for s in student_data
                if (search_text.lower() in str(s["Name"]).lower() or
                    search_text.lower() in str(s["SurName"]).lower() or
                    search_text.lower() in str(s["Nick"]).lower())
            ]
            if not filtered_students:
                search_results.controls.append(ft.Text("ไม่พบนักเรียนที่ตรงกับการค้นหา"))
            else:
                for student in filtered_students:
                    search_results.controls.append(
                        ft.TextButton(
                            text=f"{student['Name']} {student['SurName']} ({student['Nick']}) - ID: {student['S_ID']}",
                            on_click=lambda e, s_id=student["S_ID"]: select_student(s_id)
                        )
                    )
        page.update()

    def select_student(s_id):
        selected_student = next((s for s in student_data if s["S_ID"] == s_id), None)
        if selected_student:
            student_id_text.value = str(selected_student["S_ID"])
            name_text.value = selected_student["Name"]
            surname_text.value = selected_student["SurName"]
            nickname_text.value = selected_student["Nick"]
        search_input.visible = False
        search_results.visible = False
        search_results.controls.clear()
        page.update()

    # Function to update selected course IDs
    def update_selection(e, cid):
        if e.control.value:
            selected_course_ids.add(cid)
        elif cid in selected_course_ids:  # Only remove if it exists
            selected_course_ids.remove(cid)
        page.update()  # Optional: refresh UI if needed

    # Function to filter courses and update the table
    def filter_courses():
        nonlocal filtered_course_data
        selected_class = class_dropdown.value
        selected_day = day_dropdown.value

        # Filter the course data
        filtered_course_data = course_data.copy()
        if selected_class != "ทั้งหมด":
            filtered_course_data = [course for course in filtered_course_data if course["Class"] == selected_class]
        if selected_day != "ทั้งหมด":
            filtered_course_data = [course for course in filtered_course_data if course["Day"] == selected_day]

        # Update the table rows with preserved checkbox states
        course_table.controls[0].rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Checkbox(
                    value=course["C_ID"] in selected_course_ids,
                    on_change=lambda e, cid=course["C_ID"]: update_selection(e, cid)
                )),
                ft.DataCell(ft.Text(course["C_ID"], size=txt_size)),
                ft.DataCell(ft.Text(course["Class"], size=txt_size)),
                ft.DataCell(ft.Text(course["Day"], size=txt_size)),
                ft.DataCell(ft.Text(course["Period"], size=txt_size)),
                ft.DataCell(ft.Text(course["Subject"], size=txt_size)),
                ft.DataCell(ft.Text(str(course["Cost"]), size=txt_size)),
            ]) for course in filtered_course_data
        ]
        page.update()

    # Initial population of the course table
    filter_courses()

    return ft.Column(
        controls=[
            # Course Selection Container
            ft.Container(
                border_radius=15,
                margin=ft.margin.only(10, 0, 10, 0),
                content=ft.Column(
                    spacing=0,
                    controls=[
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
                        ft.Container(
                            bgcolor=grey,
                            padding=ft.padding.only(10, 10, 10, 10),
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        [
                                            ft.Text("รหัสนักเรียน :", color=navy_blue, size=txt_size),
                                            student_id_text,
                                            ft.Text("ชื่อ :", color=navy_blue, size=txt_size),
                                            name_text,
                                            ft.Text("", color=navy_blue, size=txt_size),
                                            surname_text,
                                            ft.Text("(", color=navy_blue, size=txt_size),
                                            nickname_text,
                                            ft.Text(")", color=navy_blue, size=txt_size),
                                            ft.IconButton(
                                                icon="SEARCH",
                                                on_click=lambda e: toggle_search_panel()
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.START,
                                    ),
                                    search_input,
                                    search_results,
                                    ft.Row(
                                        [
                                            class_dropdown,
                                            day_dropdown
                                        ]
                                    ),
                                    course_table,
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
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            # Payment Information Container (unchanged)
            ft.Container(
                border_radius=15,
                margin=ft.margin.only(10, 0, 10, 0),
                bgcolor=grey,
                content=ft.Column(
                    controls=[
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

if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(containers(page))
    ft.app(target=main)