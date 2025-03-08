import flet as ft
import sqlite3
import json

# Function to execute SQL queries
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
    # Define styles
    text_size = 13
    Icon_Size = 15
    field_height = 50
    class_options = ["อ.3", "ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6", "ม.1", "ม.2", "ม.3"]
    day_options = ["เสาร์", "อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"]
    subject_options = ["คณิต", "วิทย์", "อังกฤษ", "ไทย"]

    # Fetch initial data
    def load_data():
        sql = "SELECT * FROM Course ORDER BY ID DESC"
        return Exec_Sql(sql)

    # Initialize state
    original_data = load_data()
    data = original_data.copy()
    editing_index = None
    new_record_fields = None
    
    # Get unique class values from data
    def get_unique_classes():
        classes = set()
        for row in original_data:
            if row["Class"] and row["Class"].strip():
                classes.add(row["Class"])
        return sorted(list(classes))
    
    # Create filter dropdown
    class_filter = ft.Dropdown(
        width=500,
        text_size=text_size,
        hint_text="Filter by Class",
        autofocus=False
    )
    
    # Fill filter dropdown with options
    def update_filter_options():
        unique_classes = get_unique_classes()
        # Add "All Classes" option at the beginning
        options = [ft.dropdown.Option(key="all", text="All Classes")]
        # Add all unique class options
        options.extend([ft.dropdown.Option(key=cls, text=cls) for cls in unique_classes])
        class_filter.options = options
        class_filter.value = "all"  # Default to showing all classes
        page.update()
    
    # Filter data based on selected class
    def filter_data(e):
        nonlocal data
        if class_filter.value == "all":
            data = original_data.copy()
        else:
            data = [item for item in original_data if item["Class"] == class_filter.value]
        refresh_table()

    # Refresh table function
    def refresh_table():
        nonlocal data, editing_index, new_record_fields
        datatbl.controls[1] = build_table()
        page.update()

    # Delete record
    def delete_record(index):
        nonlocal data, original_data
        record_id = data[index]['ID']
        
        # Delete from the database
        sql = f"DELETE FROM Course WHERE ID = '{record_id}'"
        Exec_Sql(sql)
        
        # Delete from both data sets
        data = [item for item in data if item['ID'] != record_id]
        original_data = [item for item in original_data if item['ID'] != record_id]
        
        # Update filter options in case we deleted the last instance of a class
        update_filter_options()
        refresh_table()

    # Edit record (start editing)
    def edit_record(index):
        nonlocal editing_index
        editing_index = index
        refresh_table()

    # Save edited record
    def save_edit_record(e, index):
        nonlocal editing_index, data, original_data
        
        # Get the current row from the table
        row = datatbl.controls[1].controls[0].rows[index]
        record_id = data[index]["ID"]
        
        # Update data with edited values
        updated_values = {
            "C_ID": row.cells[0].content.value,
            "Class": row.cells[1].content.value,
            "Day": row.cells[2].content.value,
            "Period": row.cells[3].content.value,
            "Subject": row.cells[4].content.value,
            "Cost": row.cells[5].content.value,
            "ID": record_id  # Preserve original ID
        }
        
        # Update current filtered data
        data[index] = updated_values
        
        # Update original data
        for i, item in enumerate(original_data):
            if item["ID"] == record_id:
                original_data[i] = updated_values
                break

        # Update database
        sql = f"""
        UPDATE Course 
        SET C_ID = '{updated_values["C_ID"]}', 
            Class = '{updated_values["Class"]}', 
            Day = '{updated_values["Day"]}', 
            Period = '{updated_values["Period"]}', 
            Subject = '{updated_values["Subject"]}', 
            Cost = '{updated_values["Cost"]}'
        WHERE ID = '{record_id}'
        """
        Exec_Sql(sql)
        editing_index = None  # Reset editing state
        
        # Update filter options in case we changed a class value
        update_filter_options()
        refresh_table()
        print("Save completed")  # Debug

    # Copy record
    def copy_record(index):
        nonlocal data, original_data
        
        # Find the highest ID in original_data
        highest_id = max([int(item["ID"]) for item in original_data])
        new_id = str(highest_id + 1)
        
        new_record = {
            "C_ID": data[index]["C_ID"],
            "Class": data[index]["Class"],
            "Day": data[index]["Day"],
            "Period": data[index]["Period"],
            "Subject": data[index]["Subject"],
            "Cost": data[index]["Cost"],
            "ID": new_id
        }
        
        sql = f"""
        INSERT INTO Course (C_ID, Class, Day, Period, Subject, Cost, ID)
        VALUES ('{new_record["C_ID"]}', '{new_record["Class"]}', '{new_record["Day"]}', 
                '{new_record["Period"]}', '{new_record["Subject"]}', '{new_record["Cost"]}', 
                '{new_record["ID"]}')
        """
        Exec_Sql(sql)
        
        # Add to both datasets
        data.insert(0, new_record)
        original_data.insert(0, new_record)
        
        refresh_table()

    # Add new record
    def add_record(e):
        nonlocal new_record_fields
        new_record_fields = [
            ft.DataCell(ft.TextField(text_size=text_size, height=field_height)),
            ft.DataCell(ft.Dropdown(
                options=[ft.dropdown.Option(key=option, text=option) for option in class_options],
                text_size=text_size
            )),
            ft.DataCell(ft.Dropdown(
                options=[ft.dropdown.Option(key=option, text=option) for option in day_options],
                text_size=text_size
            )),
            ft.DataCell(ft.TextField(text_size=text_size, height=field_height)),
            ft.DataCell(ft.Dropdown(
                options=[ft.dropdown.Option(key=option, text=option) for option in subject_options],
                text_size=text_size
            )),
            ft.DataCell(ft.TextField(text_size=text_size, height=field_height)),
            ft.DataCell(ft.IconButton(ft.Icons.SAVE, on_click=lambda e: save_new_record(e)))
        ]
        refresh_table()

    # Save new record
    def save_new_record(e):
        nonlocal new_record_fields, data, original_data
        
        # Find the highest ID in original_data
        highest_id = max([int(item["ID"]) for item in original_data]) if original_data else 0
        new_id = str(highest_id + 1)
        
        new_record = {
            "C_ID": new_record_fields[0].content.value,
            "Class": new_record_fields[1].content.value,
            "Day": new_record_fields[2].content.value,
            "Period": new_record_fields[3].content.value,
            "Subject": new_record_fields[4].content.value,
            "Cost": new_record_fields[5].content.value,
            "ID": new_id
        }
        
        sql = f"""
        INSERT INTO Course (C_ID, Class, Day, Period, Subject, Cost, ID)
        VALUES ('{new_record["C_ID"]}', '{new_record["Class"]}', '{new_record["Day"]}', 
                '{new_record["Period"]}', '{new_record["Subject"]}', '{new_record["Cost"]}', 
                '{new_record["ID"]}')
        """
        Exec_Sql(sql)
        
        # Add to both datasets
        data.insert(0, new_record)
        original_data.insert(0, new_record)
        
        new_record_fields = None
        
        # Update filter options in case we added a new class
        update_filter_options()
        refresh_table()

    # Build table with ListView
    def build_table():
        return ft.ListView(
            controls=[ft.DataTable(
                column_spacing=5,
                columns=[
                    ft.DataColumn(label=ft.Text("C_ID", size=text_size)),
                    ft.DataColumn(label=ft.Text("Class", size=text_size, width=150)),
                    ft.DataColumn(label=ft.Text("Day", size=text_size, width=80)),
                    ft.DataColumn(label=ft.Text("Period", size=text_size, width=100)),
                    ft.DataColumn(label=ft.Text("Subject", size=text_size)),
                    ft.DataColumn(label=ft.Text("Cost", size=text_size, width=90)),
                    ft.DataColumn(label=ft.Text("Actions", size=text_size, text_align=ft.TextAlign.END)),
                ],
                rows=([ft.DataRow(cells=new_record_fields)] if new_record_fields else []) + [
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.TextField(value=item["C_ID"], text_size=text_size, height=field_height) if index == editing_index else ft.Text(item["C_ID"], size=text_size)),
                            ft.DataCell(ft.TextField(value=item["Class"], text_size=text_size, height=field_height) if index == editing_index else ft.Text(item["Class"], size=text_size)),
                            ft.DataCell(ft.TextField(value=item["Day"], text_size=text_size, height=field_height) if index == editing_index else ft.Text(item["Day"], size=text_size)),
                            ft.DataCell(ft.TextField(value=item["Period"], text_size=text_size, height=field_height, width=100) if index == editing_index else ft.Text(item["Period"], size=text_size)),
                            ft.DataCell(ft.TextField(value=item["Subject"], text_size=text_size, height=field_height, width=100) if index == editing_index else ft.Text(item["Subject"], size=text_size)),
                            ft.DataCell(ft.TextField(value=item["Cost"], text_size=text_size, height=field_height, width=90) if index == editing_index else ft.Text(str(item["Cost"]), size=text_size)),
                            ft.DataCell(
                                ft.Row(
                                    [
                                        # Use separate buttons for edit and save functionality
                                        ft.IconButton(
                                            icon=ft.Icons.SAVE,
                                            on_click=lambda e, idx=index: save_edit_record(e, idx),
                                            visible=index == editing_index,
                                            icon_size = Icon_Size
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            on_click=lambda e, idx=index: edit_record(idx),
                                            visible=index != editing_index,
                                            icon_size = Icon_Size
                                        ),
                                        ft.IconButton(ft.Icons.COPY_OUTLINED, on_click=lambda e, 
                                            idx=index: copy_record(idx),
                                            icon_size = Icon_Size),
                                        ft.IconButton(ft.Icons.DELETE, on_click=lambda e, 
                                            idx=index: delete_record(idx),
                                            icon_size = Icon_Size),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=0,
                                )
                            ),
                        ]
                    )
                    for index, item in enumerate(data)
                ]
            )],
            expand=True,
            auto_scroll=False
        )

    # Create the table UI
    datatbl = ft.Column(
        controls=[
            ft.Row(
                [
                    # Class filter on the left
                    ft.Text("Filter:", size=text_size),
                    class_filter,
                    # Spacer to push add button to the right
                    ft.Container(expand=True),
                    # Add button on the right
                    ft.ElevatedButton("Add", icon=ft.Icons.ADD_CIRCLE, on_click=add_record),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            build_table(),
        ]
    )
    
    # Initialize class filter dropdown
    class_filter.on_change = filter_data
    update_filter_options()

    return datatbl

# For testing, you might want to add this if running standalone
if __name__ == "__main__":
    ft.app(target=lambda page: page.add(containers(page)))