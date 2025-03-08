import requests
import json
from docxtpl import DocxTemplate
import os
import docx2pdf
import sys
import subprocess
import sqlite3


# def open_pdf_receipt_no(rid):
#     filename = f"receipt/{rid}.pdf"
#     pdf_path = os.path.abspath(filename)
#     webbrowser.open_new(f"file://{pdf_path}")
#     # webbrowser.open_new(f"file://{pdf_path}")

# def open_pdf_receipt_no(rid):
#     ospth = os.getcwd()
#     pdf_path = f"{ospth}/receipt/{rid}.pdf"
#     try:
#         if sys.platform.startswith('win'):
#             # Windows
#             os.startfile(pdf_path)
#         elif sys.platform.startswith('darwin'):
#             # macOS
#             subprocess.call(('open', pdf_path))
#         elif sys.platform.startswith('linux'):
#             # Linux
#             subprocess.call(('xdg-open', pdf_path))
#         else:
#             print("Platform not supported")
#     except Exception as e:
#         print(f"Error: {e}")

def open_pdf_receipt_no(rid):
    ospth = os.getcwd()
    pdf_path = f"{ospth}/receipt/{rid}.docx"
    try:
        if sys.platform.startswith('win'):
            # Windows
            os.startfile(pdf_path)
        elif sys.platform.startswith('darwin'):
            # macOS
            subprocess.call(('open', pdf_path))
        elif sys.platform.startswith('linux'):
            # Linux
            subprocess.call(('xdg-open', pdf_path))
        else:
            print("Platform not supported")
    except Exception as e:
        print(f"Error: {e}")




def max_id(data,id_name):
    maxitem = ""
    maxvalue=0
    for s in data:
        if int(s[id_name]) >= maxvalue:
                maxvalue = int(s[id_name])
                maxitem = s
    return maxitem 



# def StudentParens():
#     url = 'https://bannkruann.com/Student/php/studentparentjson.php'
#     d = jsontolist(url)
#     with open('student_data.json', 'w', encoding='utf-8') as file:
#                 json.dump(d, file, ensure_ascii=False, indent=4)
#     return d


# def Parents():
#     url = 'https://bannkruann.com/Student/php/parentjson.php'
#     d = jsontolist(url)
#     with open('parent.json', 'w', encoding='utf-8') as file:
#                 json.dump(d, file, ensure_ascii=False, indent=4)
#     return d

# def Exec_Sql(sql):
#     url = f'https://bannkruann.com/Student/php/execsql.php?sql={sql}'
#     x = requests.get(url)
#     datas = json.loads(x.text)
#     return datas

def Exec_Sql(sql):
    conn = sqlite3.connect("Bannkruann.db") 
    c = conn.cursor()
    c.execute(sql)
    result = c.fetchall()
    if len(result) > 0 :
        attb = [d[0] for d in c.description]
        jsonlist = [dict(zip(attb, item)) for item in result]
    else:
        jsonlist = result
    conn.commit()
    conn.close()
    #json_string = json.dumps(jsonlist, ensure_ascii=False, indent=2)
    return jsonlist

def receiptpdf(rid):
    # url = f'https://bannkruann.com/Student/php/receiptjson.php?r_id={rid}'
    # d = jsontolist(url)
    sql = f"SELECT R.R_ID, R.Paid_Date, R.Amount, R.Cash, R.RNote, R.ExtraNote, S.S_ID, S.Name, S.SurName, S.Nick, P.M_Name, P.M_SurName, P.H_Adr, P.H_Mu, P.H_Tum, P.H_Amp, P.H_Prov, P.H_Post FROM Receipt as R JOIN Student as S ON S.S_ID = R.S_ID JOIN Parent as P ON P.P_ID = S.P_ID WHERE R.R_ID = {rid}"
    d = Exec_Sql(sql)
    d[0]['Amounttext']=bahttext(float(d[0]['Amount']))
    d[0]['Amount']=format(float(d[0]['Amount']),",.2f")
    d[0]['Paid_Date'] = thaidate(d[0]['Paid_Date'])

    doc = DocxTemplate('template.docx')
    doc.render(d[0])
    doc.save(f'receipt/{rid}.docx')

    docx2pdf.convert(f'receipt/{rid}.docx',f'receipt/{rid}.pdf')        

def jsontolist (url):
    x = requests.get(url)
    datas = json.loads(x.text)
    return datas
    
def replace_placeholders_in_docxtpl(data, save_path):
    # โหลดเทมเพลตเอกสาร
    doc = DocxTemplate('template.docx')

    
    # แทนที่ตัวแทนด้วยค่าจริง
    doc.render(data)
    
    # บันทึกเอกสารที่แก้ไขแล้ว
    doc.save(f'{save_path}.docx')
    # แปลงเป็น pdf
    docx2pdf.convert(f'{save_path}.docx',f'{save_path}.pdf' )
    os.remove(f'{save_path}.docx')





def bahttext(amount):
    # ลิสต์ตัวเลขและหลักในภาษาไทย
    numbers = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    scales = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน"]

    # แยกจำนวนเต็มและทศนิยมออกจากกัน
    integer_part, decimal_part = str(amount).split(".")
    integer_part = int(integer_part)
    decimal_part = int(decimal_part)

    # ถ้าจำนวนเต็มเป็น 0 ให้แสดงผลลัพธ์เป็น "ศูนย์บาท"
    if integer_part == 0:
        bahttxt = "ศูนย์บาท"
    else:
        bahttxt = ""
        scale_index = 0

        # วนลูปเพื่อแปลงจำนวนเต็มเป็นคำอ่านภาษาไทย
        while integer_part > 0:
            digit = integer_part % 10
            integer_part //= 10

            if digit > 0:
                if digit == 1 and scale_index == 1:
                    bahttxt = "เอ็ด" + bahttxt
                elif digit == 2 and scale_index == 1:
                    bahttxt = "ยี่" + scales[scale_index] + bahttxt
                else:
                    bahttxt = numbers[digit] + scales[scale_index] + bahttxt

            scale_index += 1

        # เพิ่มคำว่า "บาท" ต่อท้ายจำนวนเต็ม
        bahttxt += "บาท"

    # ถ้าทศนิยมเป็น 0 ให้เพิ่มคำว่า "ถ้วน" ต่อท้าย
    if decimal_part == 0:
        bahttxt += "ถ้วน"
    else:
        # ถ้าทศนิยมน้อยกว่า 10 ให้เพิ่ม "ศูนย์" ข้างหน้า
        if decimal_part < 10:
            bahttxt += "ศูนย์"
        # แปลงทศนิยมเป็นคำอ่านภาษาไทยโดยใช้ฟังก์ชัน bahttext เรียกซ้ำ
        bahttxt += bahttext(decimal_part).strip() + "สตางค์"

    # คืนค่าคำอ่านภาษาไทยที่ได้
    return bahttxt.strip()


import datetime

# Function to convert Gregorian year to Thai Buddhist Era year
def thaidate(date_str):
    # Function to convert Gregorian year to Thai Buddhist Era year
    def gregorian_to_thai_year(year):
        return year + 543

    # Dictionary for Thai month abbreviations
    thai_months = {
        1: "ม.ค.",
        2: "ก.พ.",
        3: "มี.ค.",
        4: "เม.ย.",
        5: "พ.ค.",
        6: "มิ.ย.",
        7: "ก.ค.",
        8: "ส.ค.",
        9: "ก.ย.",
        10: "ต.ค.",
        11: "พ.ย.",
        12: "ธ.ค."
    }

    # Parse the date string into a datetime object
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # Get the day, month, and year
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year

    # Convert the year to Thai Buddhist Era
    thai_year = gregorian_to_thai_year(year) % 100  # Get the last two digits of the year

    # Format the date in the desired format
    formatted_date = f"{day} {thai_months[month]} {thai_year}"

    return formatted_date


# sql = "UPDATE Course SET C_ID = 'SUN-T.LEA', Class = 'English by Teacher Le', Day = 'วันอาทิตย์', Period = '10.00-12.00', Subject = 'สนทนภาษาอังกฤษ', Cost = '280' WHERE ID = 14"
# print(sql)  
# Exec_Sql(sql)
# sql = "select * from Course where ID=14"      
# print(Exec_Sql(sql))


# sql = "INSERT INTO Enroll (ID, S_ID, C_ID) VALUES ('35','3349','SAT-P6 -MATH-SCI-THAI-ENG')"
# Exec_Sql(sql)
# maxpaymantID = int(max_id(Exec_Sql("SELECT ID FROM Payment"),"ID")["ID"])+1
# sql = "INSERT INTO `Payment` (`ID`, `S_ID`, `Total`, `Pay1`, `Paid_Date1`, `Receipt1`, `Pay2`, `Paid_Date2`, `Receipt2`, `Pay3`, `Paid_Date3`, `Receipt3`, `Pay4`, `Paid_Date4`, `Receipt4`, `RNote`) VALUES ('11', '777', '3000', '0', '0000-00-00', '0', '0', '0000-00-00', '0', '0', '0000-00-00', '0', '0', '0000-00-00', '0', 'RNote');"
# Exec_Sql(sql)
# sql = "SELECT * FROM Payment"
# print (Exec_Sql(sql))

