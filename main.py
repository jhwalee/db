# conda create -n db python=3.6.9
# pip install PyMySQL

from tkinter import *
from tkinter.ttk import *
import pymysql

# DB 관련 정보 설정
DB_IP_ADDRESS = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'rootpassword'
DB_DBNAME = 'TEAM_DB'

'''
함수 명 : initialize_widget 
설명 : Python Application Form GUI를 구성하는 각종 Widget의 선언과 그 Layout 구성에 대한 코드를 구현한 함수 입니다.
주의 : 가장 마지막 코드는  window.mainloop()로 종료.
'''
def initialize_widget():
    # Widget 중에 외부 함수에서 접근을 해서 값을 가져오거나 값을 설정할 Widge을 전역변수로 선언
    global table_dept_info, entry_dept_id, entry_dept_name, entry_dept_budget, \
        combobox_emp_list, label_emp_dept_name, label_emp_id, label_emp_name, label_emp_salary

    # 최상위 Application Frame widget Window 컴포넌트 정의
    window = Tk()
    window.title("데이터베이스 전략과 실습 강의 샘플 App")
    window.geometry("1000x500+100+100")

    '''''''''''''''''''''
    부서 정보 조회 부분 정의
    '''''''''''''''''''''
    # 부서 정보 조회 Label widget
    label_get_dept_info = Label(window, text="부서 정보 조회")
    label_get_dept_info.place(x=10, y=10, width=100, height=20)
    # 부서 정보 조회 Button Widget
    btn_db_get_dept = Button(window, text="Dept 정보조회", command=click_btn_get_dept_info)
    btn_db_get_dept.place(x=140, y=5, width=120, height=30)
    # 부서 정보 조회용 테이블형태의 Treeview Widget
    table_dept_info = Treeview(window, columns=["부서ID", "부서명", "예산"])
    table_dept_info.place(x=10, y=50, width=500, height=190)
    table_dept_info.column("부서ID", width=100, anchor="center")
    table_dept_info.heading("부서ID", text="부서ID", anchor="center")
    table_dept_info.column("부서명", width=200, anchor="center")
    table_dept_info.heading("부서명", text="부서명", anchor="center")
    table_dept_info.column("예산", width=200, anchor="center")
    table_dept_info.heading("예산", text="예산", anchor="center")
    table_dept_info["show"] = "headings"

    '''''''''''''''''''''
    부서 정보 입력 부분 정의
    '''''''''''''''''''''
    # 부서 정보 입력 Label widget
    label_set_dept_info = Label(window, text="부서 정보 입력")
    label_set_dept_info.place(x=560, y=10, width=100, height=20)
    # 부서ID 표시용 Label Widget
    label_dept_id = Label(window, text="부서 ID :")
    label_dept_id.place(x=560, y=40, width=100, height=20)
    # 부서IO 입력용 Entry Widget
    entry_dept_id = Entry(window)
    entry_dept_id.place(x=670, y=40, width=170, height=30)
    # 부서명 표시용 Label Widget
    label_dept_name = Label(window, text="부서명 :")
    label_dept_name.place(x=560, y=80, width=100, height=20)
    # 부서명 입력용 Entry Widget
    entry_dept_name = Entry(window)
    entry_dept_name.place(x=670, y=80, width=170, height=30)
    # 부서 Budget 표시용 Label Widget
    label_dept_budget = Label(window, text="예산 :")
    label_dept_budget.place(x=560, y=120, width=100, height=20)
    # 부서 Budget 입력용 Entry Widget
    entry_dept_budget = Entry(window)
    entry_dept_budget.place(x=670, y=120, width=170, height=30)
    # 부서 정보 입력 Button Widget
    btn_db_set_dept = Button(window, text="입력", command=click_btn_set_dept_info)
    btn_db_set_dept.place(x=640, y=160, width=120, height=30)

    '''''''''''''''''''''
    직원 정보 레포팅 부분 정의
    '''''''''''''''''''''
    # 직원 이름 가져오기 위해 DB 접속
    db_conn = pymysql.connect(host=DB_IP_ADDRESS, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_DBNAME, charset='utf8')
    sql = "SELECT EMP_NAME FROM EMPLOYEE"
    # 직원 정보 테이블 쿼리 결과를 가지고 옴
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute(sql)
            records = cur.fetchall()
            emp_names = [str(record[0]) for record in records]
    # 직원 정보 레포트 Label widget
    label_get_emp_info = Label(window, text="직원 정보 Report")
    label_get_emp_info.place(x=110, y=300, width=100, height=20)
    # 직원 이름을 Dropdown list로 표시할 ComboBox Widget 을 생성하고 DB에서 얻어온 직원명을 설정함
    combobox_emp_list = Combobox(window, height=15, values=emp_names)
    combobox_emp_list.place(x=230, y=300, width=100, height=30)
    combobox_emp_list.bind("<<ComboboxSelected>>", select_emp_combobox)
    combobox_emp_list.set("직원 선택")
    # 부서명을 표시할 Label Widget
    label_emp_dept_name = Label(window, text="부서명:-")
    label_emp_dept_name.place(x=110, y=350, width=200, height=20)
    # 직원번호를 표시할 Label Widget
    label_emp_id = Label(window, text="직원번호:-")
    label_emp_id.place(x=110, y=380, width=200, height=20)
    # 직원명을 표시할 Label Widget
    label_emp_name = Label(window, text="직원명:-")
    label_emp_name.place(x=110, y=410, width=200, height=20)
    # 봉급을 표시할 Label Widget
    label_emp_salary = Label(window, text="봉급:-")
    label_emp_salary.place(x=110, y=440, width=200, height=20)

    '''''''''''''''''''''
    TK Inter Frame 코드. 마지막에 꼭 입력
    '''''''''''''''''''''
    window.mainloop()

'''
함수 명 : click_btn_get_dept_info 
설명 : Python Widget 이벤트를 처리하기 위한 함수. 부서 조회 버튼 클릭에 대한 코드
'''
def click_btn_get_dept_info():
    # DB 접속
    db_conn = pymysql.connect(host=DB_IP_ADDRESS, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_DBNAME,
                              charset='utf8')
    sql = "SELECT * FROM DEPARTMENT"
    # DB Connection을 얻은 후에 Select Query를 통해서 얻은 부서 정보를 Table에 넣어준다.
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchall()
            # 기존 Table Widget의 내용을 지워줌
            table_dept_info.delete(*table_dept_info.get_children())
            # 받아온 SQL Query 결과를 Table Widget에 입력
            for data in result:
                table_dept_info.insert(parent="", index='end', text="", values=(data[0], data[1], data[2]), iid=data)

'''
함수 명 : click_btn_set_dept_info 
설명 : Python Widget 이벤트를 처리하기 위한 함수. 부서 정보 입력 버튼 클릭에 대한 코드
'''
def click_btn_set_dept_info():
    # DB 접속
    db_conn = pymysql.connect(host=DB_IP_ADDRESS, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_DBNAME, charset='utf8')
    # Dept ID, Name, Budget Entry컨트롤에 입력한 값을 가져와서 Insert SQL QUery를 만들어줌.
    dept_id = entry_dept_id.get()
    dept_name = entry_dept_name.get()
    dept_budget = entry_dept_budget.get()
    sql = "INSERT INTO DEPARTMENT VALUES (%s, %s, %s)"
    val = (dept_id, str(dept_name), dept_budget)
    # DB 에 Insert Query를 실행시킴
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute(sql, val)
            db_conn.commit()

'''
함수 명 : select_emp_combobox 
설명 : Python Widget 이벤트를 처리하기 위한 함수. 직원 정보 레포트 부분의 Combo Box 선택 이벤트를 처리하는 함수
'''
def select_emp_combobox(event):
    # DB 접속
    db_conn = pymysql.connect(host=DB_IP_ADDRESS, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_DBNAME,
                              charset='utf8')
    sql = f"SELECT DEPARTMENT.DEPT_NAME, EMPLOYEE.EMP_ID,  EMPLOYEE.EMP_NAME,  EMPLOYEE.EMP_SALARY FROM EMPLOYEE \
    INNER JOIN DEPARTMENT ON EMPLOYEE.EMP_DEPT_NO=DEPARTMENT.DEPT_ID WHERE EMPLOYEE.EMP_NAME = '{combobox_emp_list.get()}'"
    # DB와 SQL Join Query를 통해서 얻은 직원 정보를 Report 부분 Widget에 입력한다.
    with db_conn:
        with db_conn.cursor() as cur:
            cur.execute(sql)
            result = cur.fetchone()
            # SQL Query 결과 Widget에 설정
            label_emp_dept_name['text'] = f'부서명 : {result[0]}'
            label_emp_id['text'] = f'직원번호 : {result[1]}'
            label_emp_name['text'] = f'직원명 : {result[2]}'
            label_emp_salary['text'] = f'봉급 : {result[3]}'

if __name__ == '__main__':
    initialize_widget()