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

def max_id(data, id_name):
    maxitem = ""
    maxvalue = 0
    for s in data:
        if int(s[id_name]) >= maxvalue:
            maxvalue = int(s[id_name])
            maxitem = s
    return maxitem 

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
    global student_data
    student_data = Exec_Sql(student_sql)
    parent_data = Exec_Sql(parent_sql)

    # Global variable for current student, initialized as None if no data
    global current_student
    current_student = student_data[0] if student_data else None

    # State variables for editing
    editing_student = [False]
    editing_parent = [False]

    # Student ID input field
    student_id_input = ft.TextField(
        label="รหัสนักเรียน",
        value=str(current_student["S_ID"]) if current_student else "",
        bgcolor=white,
        expand=True,
        on_submit=lambda e: search_student(e),
    )

    # Search input and results
    search_input = ft.TextField(
        label="ค้นหา: ชื่อ นามสกุล หรือ ชื่อเล่น",
        bgcolor=white,
        on_change=lambda e: update_search_results(e.control.value)
    )
    search_results = ft.Column(expand=True, scroll="auto")

    # Containers to hold dynamic content
    student_info_content = ft.Container()
    parent_info_content = ft.Container()

    # Edit buttons
    edit_save_student_btn = ft.ElevatedButton(
        text="Edit",
        icon="EDIT",
        color=yellow,
        bgcolor=navy_blue,
        icon_color=yellow,
        on_click=lambda e: toggle_student_edit(e)
    )
    edit_save_parent_btn = ft.ElevatedButton(
        text="Edit",
        icon="EDIT",
        color=navy_blue,
        bgcolor=yellow,
        icon_color=navy_blue,
        on_click=lambda e: toggle_parent_edit(e)
    )

    # Editable student fields (global to access values)
    name_input = ft.TextField(bgcolor=white, height=40)
    surname_input = ft.TextField(bgcolor=white, height=40)
    nick_input = ft.TextField(bgcolor=white, height=40)
    school_input = ft.TextField(bgcolor=white, height=40)
    class_input = ft.TextField(bgcolor=white, height=40)
    s_tel_input = ft.TextField(bgcolor=white, height=40)

    # Editable parent fields (global to access values)
    parent_name_input = ft.TextField(bgcolor=white, height=40)
    parent_surname_input = ft.TextField(bgcolor=white, height=40)
    parent_tel_input = ft.TextField(bgcolor=white, height=40)
    parent_line_input = ft.TextField(bgcolor=white, height=40)
    parent_facebook_input = ft.TextField(bgcolor=white, height=40)

    # Function to create editable student fields
    def create_editable_student_fields(student):
        if student:
            name_input.value = student["Name"]
            surname_input.value = student["SurName"]
            nick_input.value = student["Nick"]
            school_input.value = student["School"]
            class_input.value = student["Class"]
            s_tel_input.value = student["S_Tel"]
        
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            [
                                student_id_input,
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.SEARCH,
                                            icon_color=navy_blue,
                                            on_click=lambda e: toggle_search_panel()
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.ADD,
                                            icon_color=navy_blue,
                                            on_click=lambda e: add_student(e)
                                        ),
                                    ],
                                    spacing=0,
                                ),
                            ],
                            expand=3,
                        ),
                        ft.Row([edit_save_student_btn], expand=1, alignment=ft.MainAxisAlignment.END),
                    ]
                ),
                search_input,
                search_results,
                ft.Row(
                    [
                        ft.Column([ft.Text("ชื่อนักเรียน", size=13), name_input], expand=2, spacing=0),
                        ft.Column([ft.Text("นามสกุล", size=13), surname_input], expand=2, spacing=0),
                        ft.Column([ft.Text("ชื่อเล่น", size=13), nick_input], expand=1, spacing=0),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.Column([ft.Text("โรงเรียนประจำ", size=13), school_input], expand=5, spacing=0),
                        ft.Column([ft.Text("ระดับชั้น", size=13), class_input], expand=2, spacing=0),
                    ],
                    spacing=5,
                ),
                ft.Row(
                    [ft.Column([ft.Text("หมายเลขโทรศัพท์", size=13), s_tel_input], expand=True, spacing=0)],
                    spacing=5,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(text="Enroll", icon="APP_REGISTRATION", color=yellow, bgcolor=navy_blue, icon_color=yellow, width=150),
                        ft.ElevatedButton(text="Payment", icon="PAYMENT", color=yellow, bgcolor=navy_blue, icon_color=yellow, width=150),
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            ]
        )

    # Function to create editable parent fields
    def create_editable_parent_fields(student):
        if student:
            parent_name_input.value = student["M_Name"]
            parent_surname_input.value = student["M_SurName"]
            parent_tel_input.value = student["M_Tel"]
            parent_line_input.value = student["line"]
            parent_facebook_input.value = student["facebook"]
            
            return ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"รหัสผู้ปกครอง: {student['P_ID']}"),
                            edit_save_parent_btn,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("ชื่อผู้ปกครอง", size=13), parent_name_input],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("นามสกุล", size=13), parent_surname_input],
                                expand=1, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("หมายเลขโทรศัพท์", size=13), parent_tel_input],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("Line ID", size=13), parent_line_input],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("Facebook", size=13), parent_facebook_input],
                                expand=1, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                ]
            )
        return ft.Column([ft.Text("No parent data available")])

    # Function to display student info dynamically
    def display_student_info(student):
        if student:
            student_info_content.content = create_editable_student_fields(student) if editing_student[0] else ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Row(
                                [
                                    student_id_input,
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.SEARCH,
                                                icon_color=navy_blue,
                                                on_click=lambda e: toggle_search_panel()
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.ADD,
                                                icon_color=navy_blue,
                                                on_click=lambda e: add_student(e)
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                ],
                                expand=3,
                            ),
                            ft.Row([edit_save_student_btn], expand=1, alignment=ft.MainAxisAlignment.END),
                        ]
                    ),
                    search_input,
                    search_results,
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("ชื่อนักเรียน", size=13), ft.TextField(value=student["Name"], read_only=True, bgcolor=white, height=40)],
                                expand=2, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("นามสกุล", size=13), ft.TextField(value=student["SurName"], read_only=True, bgcolor=white, height=40)],
                                expand=2, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("ชื่อเล่น", size=13), ft.TextField(value=student["Nick"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("โรงเรียนประจำ", size=13), ft.TextField(value=student["School"], read_only=True, bgcolor=white, height=40)],
                                expand=5, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("ระดับชั้น", size=13), ft.TextField(value=student["Class"], read_only=True, bgcolor=white, height=40)],
                                expand=2, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("หมายเลขโทรศัพท์", size=13), ft.TextField(value=student["S_Tel"], read_only=True, bgcolor=white, height=40)],
                                expand=True, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Enroll", icon="APP_REGISTRATION", color=yellow, bgcolor=navy_blue, icon_color=yellow, width=150),
                            ft.ElevatedButton(text="Payment", icon="PAYMENT", color=yellow, bgcolor=navy_blue, icon_color=yellow, width=150),
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )
                ]
            )
            parent_info_content.content = create_editable_parent_fields(student) if editing_parent[0] else ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(f"รหัสผู้ปกครอง: {student['P_ID']}"),
                            edit_save_parent_btn,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("ชื่อผู้ปกครอง", size=13), ft.TextField(value=student["M_Name"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("นามสกุล", size=13), ft.TextField(value=student["M_SurName"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [ft.Text("หมายเลขโทรศัพท์", size=13), ft.TextField(value=student["M_Tel"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("Line ID", size=13), ft.TextField(value=student["line"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                            ft.Column(
                                [ft.Text("Facebook", size=13), ft.TextField(value=student["facebook"], read_only=True, bgcolor=white, height=40)],
                                expand=1, spacing=0
                            ),
                        ],
                        spacing=5,
                    ),
                ]
            )
        else:
            if editing_student[0]:
                student_info_content.content = create_editable_student_fields(None)
            else:
                student_info_content.content = ft.Text("No student selected")
                
            if editing_parent[0]:
                parent_info_content.content = create_editable_parent_fields(None)
            else:
                parent_info_content.content = ft.Text("")
        page.update()

    # Toggle student edit mode and save to database
    def toggle_student_edit(e):
        global current_student, student_data
        
        editing_student[0] = not editing_student[0]
        
        if editing_student[0]:
            edit_save_student_btn.text = "Save"
            edit_save_student_btn.icon = "SAVE"
            display_student_info(current_student)
        else:
            if current_student and "S_ID" in current_student and current_student["S_ID"] is not None:  # Editing an existing student
                if not str(student_id_input.value).strip():
                    student_info_content.content = ft.Text("กรุณากรอกรหัสนักเรียน")
                    page.update()
                    return
                
                sql = f"""
                    UPDATE Student 
                    SET Name = '{name_input.value}', 
                        SurName = '{surname_input.value}', 
                        Nick = '{nick_input.value}', 
                        School = '{school_input.value}', 
                        Class = '{class_input.value}', 
                        S_Tel = '{s_tel_input.value}' 
                    WHERE S_ID = {student_id_input.value}
                """
                Exec_Sql(sql)
            else:  # Adding a new student
                # Get the next available IDs
                all_students = Exec_Sql("SELECT * FROM Student ORDER BY S_ID DESC")
                all_parents = Exec_Sql("SELECT * FROM Parent ORDER BY P_ID DESC")
                
                next_s_id = int(max_id(all_students, "S_ID")["S_ID"]) + 1 if all_students else 1
                next_p_id = int(max_id(all_parents, "P_ID")["P_ID"]) + 1 if all_parents else 1
                
                # First, insert the parent data WITH explicit P_ID
                parent_sql = f"""
                    INSERT INTO Parent (P_ID, M_Name, M_SurName, M_Tel, line, facebook)
                    VALUES ({next_p_id}, '{parent_name_input.value}', '{parent_surname_input.value}', 
                            '{parent_tel_input.value}', '{parent_line_input.value}', 
                            '{parent_facebook_input.value}')
                """
                Exec_Sql(parent_sql)
                
                # Insert the student data with the new parent ID
                student_sql = f"""
                    INSERT INTO Student (S_ID, Name, SurName, Nick, School, Class, S_Tel, P_ID)
                    VALUES ({next_s_id}, '{name_input.value}', '{surname_input.value}', '{nick_input.value}', 
                            '{school_input.value}', '{class_input.value}', '{s_tel_input.value}', 
                            {next_p_id})
                """
                Exec_Sql(student_sql)
                
                # Update the student ID input field
                student_id_input.value = str(next_s_id)

            # Refresh student data
            student_data = Exec_Sql("SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID ORDER BY S.S_ID DESC")
            current_student = next((s for s in student_data if s["S_ID"] == int(student_id_input.value)), None) if student_id_input.value else student_data[0] if student_data else None
            
            edit_save_student_btn.text = "Edit"
            edit_save_student_btn.icon = "EDIT"
            editing_parent[0] = False  # Reset parent edit mode after saving
            edit_save_parent_btn.text = "Edit"
            edit_save_parent_btn.icon = "EDIT"
            display_student_info(current_student)

    # Toggle parent edit mode and save to database
    def toggle_parent_edit(e):
        global current_student
        
        if not current_student:
            parent_info_content.content = ft.Text("ไม่พบข้อมูลผู้ปกครอง")
            page.update()
            return
        
        editing_parent[0] = not editing_parent[0]
        
        if editing_parent[0]:
            edit_save_parent_btn.text = "Save"
            edit_save_parent_btn.icon = "SAVE"
        else:
            parent_id = current_student["P_ID"]
            sql = f"""
                UPDATE Parent 
                SET M_Name = '{parent_name_input.value}', 
                    M_SurName = '{parent_surname_input.value}', 
                    M_Tel = '{parent_tel_input.value}', 
                    line = '{parent_line_input.value}', 
                    facebook = '{parent_facebook_input.value}' 
                WHERE P_ID = {parent_id}
            """
            Exec_Sql(sql)
            
            student_data = Exec_Sql("SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID ORDER BY S.S_ID DESC")
            current_student = next((s for s in student_data if s["S_ID"] == int(student_id_input.value)), None)
            
            edit_save_parent_btn.text = "Edit"
            edit_save_parent_btn.icon = "EDIT"
        
        display_student_info(current_student)

    # Search student by ID when Enter is pressed
    def search_student(e):
        student_id = str(student_id_input.value).strip()
        if not student_id:
            student_info_content.content = ft.Text("กรุณากรอกรหัสนักเรียน")
            parent_info_content.content = ft.Text("")
            page.update()
            return
        sql = f"SELECT * FROM Student as S, Parent as P WHERE S.P_ID = P.P_ID AND S.S_ID = {student_id}"
        result = Exec_Sql(sql)
        global current_student
        current_student = result[0] if result else None
        if current_student:
            display_student_info(current_student)
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
        student_id_input.value = str(s_id)
        student = next((s for s in student_data if s["S_ID"] == s_id), None)
        if student:
            global current_student
            current_student = student
            display_student_info(student)
        search_input.visible = False
        search_results.visible = False
        search_results.controls.clear()
        page.update()

    # Add new student function
    def add_student(e):
        global current_student
        
        # Fetch latest data to ensure we have current max IDs
        all_students = Exec_Sql("SELECT * FROM Student ORDER BY S_ID DESC")
        all_parents = Exec_Sql("SELECT * FROM Parent ORDER BY P_ID DESC")
        
        # Find max IDs and increment by 1
        next_s_id = int(max_id(all_students, "S_ID")["S_ID"]) + 1 if all_students else 1
        next_p_id = int(max_id(all_parents, "P_ID")["P_ID"]) + 1 if all_parents else 1
        
        # Create empty student record with new IDs
        current_student = {
            "S_ID": None,  # Set to None to trigger the "Adding a new student" branch in toggle_student_edit
            "P_ID": next_p_id,
            "Name": "",
            "SurName": "",
            "Nick": "",
            "School": "",
            "Class": "",
            "S_Tel": "",
            "M_Name": "",
            "M_SurName": "",
            "M_Tel": "",
            "line": "",
            "facebook": ""
        }
        
        # Set student ID field
        student_id_input.value = str(next_s_id)
        
        # Clear all input fields
        name_input.value = ""
        surname_input.value = ""
        nick_input.value = ""
        school_input.value = ""
        class_input.value = ""
        s_tel_input.value = ""
        parent_name_input.value = ""
        parent_surname_input.value = ""
        parent_tel_input.value = ""
        parent_line_input.value = ""
        parent_facebook_input.value = ""
        
        # Enable edit mode for both student and parent
        editing_student[0] = True
        editing_parent[0] = True
        
        # Update button text and icons
        edit_save_student_btn.text = "Save"
        edit_save_student_btn.icon = "SAVE"
        edit_save_parent_btn.text = "Save" 
        edit_save_parent_btn.icon = "SAVE"
        
        # Display form in edit mode
        display_student_info(current_student)
        
        # Hide search panel if visible
        if search_input.visible:
            search_input.visible = False
            search_results.visible = False
            search_results.controls.clear()
            page.update()

    # Initial display
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

    return ft.Column(
        controls=[student_info_container, parent_info_container],
        spacing=10,
    )

# Example usage
def main(page: ft.Page):
    page.add(containers(page))

if __name__ == "__main__":
    ft.app(target=main)