"""
Project VNPT January 2024
Product by: Truong Cong Quoc Huy
"""

import sys, os, datetime
from PyQt6.QtWidgets import QApplication
from pyutils.extend___dlg_box import show_dlg
import traceback
from pyutils.extend___send_email_report import Send_Report
import socket, cx_Oracle
import pandas as pd


new_path = os.path.join(os.getcwd(),'dist\\app\\ASUS\\product\\12.2.0\\client_1')
if not os.path.exists(new_path):
    new_path = os.path.join(os.getcwd(),'app\\ASUS\\product\\12.2.0\\client_1')
current_path = os.environ.get('PATH', '')
os.environ['PATH'] = current_path + os.pathsep + new_path

db_user = 'huytcq'
db_password = 'itc123'
db_connectstring = "(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 10.92.53.53)(PORT = 1521)))(CONNECT_DATA =(SERVER = DEDICATED)(SERVICE_NAME = DBCTO)))"
db_url = f"{db_user}\\{db_password}:{db_connectstring}"
socket.setdefaulttimeout(3)
try:
    db_connection = cx_Oracle.connect(user=db_user, password=db_password, dsn=db_connectstring)
    cursor_db = db_connection.cursor()
except cx_Oracle.DatabaseError as e:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"\n----- Lỗi đã xảy ra vào lúc {current_time} -----\n"
    with open(os.path.join(os.getcwd(),'History\Error_Log.txt'), 'a', encoding='utf-8') as file:
        file.write(error_message)
        file.write(traceback.format_exc())
    app = QApplication(sys.argv)
    button = show_dlg('Warning','Chương trình gặp lỗi không mong muốn, hãy báo cáo về sự cố',['Gửi báo cáo', 'Hủy'],-1)
    if button == 'Gửi báo cáo':
        Send_Report(str(e))
        sys.exit()
    elif button == 'Hủy':
        sys.exit()
    sys.exit(app.exec())

current_version = '1.0'
query = "SELECT column_name FROM user_tab_columns WHERE table_name = 'VERSION_DATABASE_UPLOAD_TOOL' ORDER BY column_id"
cursor_db.execute(query)
column = {row[0]: [] for row in cursor_db.fetchall()}

query = "SELECT * FROM VERSION_DATABASE_UPLOAD_TOOL ORDER BY time_update DESC FETCH FIRST 1 ROWS ONLY"
cursor_db.execute(query)
version_data = cursor_db.fetchone()
df = pd.DataFrame([version_data], columns=column.keys())

if current_version != df['VERSION'].values[0]:

    app = QApplication(sys.argv)
    button = show_dlg('Information','Đã có bản cập nhật mới! Tải về để cập nhật',['Đến trang tải về', 'Hủy'],0)
    if button == 'Đến trang tải về':
        Send_Report(str(e))
        sys.exit()
    elif button == 'Hủy':
        sys.exit()
    sys.exit(app.exec())



try:
    from main_process import DatabaseUploadTool
    if __name__=="__main__":
        app=QApplication(sys.argv)
        main_win=DatabaseUploadTool()
        main_win.show()
        main_win.setWindowTitle("Database Upload Tool")
        sys.exit(app.exec())
except Exception as e:
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = f"\n----- Lỗi đã xảy ra vào lúc {current_time} -----\n"
    with open(os.path.join(os.getcwd(),'History\Error_Log.txt'), 'a', encoding='utf-8') as file:
        file.write(error_message)
        file.write(traceback.format_exc())
    app = QApplication(sys.argv)
    button = show_dlg('Warning','Chương trình gặp lỗi không mong muốn, hãy báo cáo về sự cố',['Gửi báo cáo', 'Hủy'],-1)
    if button == 'Gửi báo cáo':
        Send_Report(str(e))
        sys.exit()
    elif button == 'Hủy':
        sys.exit()
    sys.exit(app.exec())
