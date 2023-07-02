import PySimpleGUI as sg
import Models.init as main
import Models.students as studentsModel
import Models.transactions as transactionsModel
import Models.reports as reportsModel
from datetime import datetime

studentsHeadings = ["FIRST", "LAST", "FATHER", "MOTHER", "BIRTH", "PHONE", "SCHOLARSHIP"]
reportsHeadings = ["SUBJECT", "MARK", "FULL MARK", "MONTH", "YEAR"]
transactionsHeadings = ["DATE", "AMOUNT"]

def students_window(yearN):

    def new_student_window():
        layout = [
            [sg.T("First:"), sg.I(key="new_first", size=15),
             sg.T("Last:"), sg.I(key="new_last", size=15)],
            [sg.T("Grade:"), sg.OptionMenu(values=main.getConstants("grades"), key="new_grade"),
             sg.T("Class:"), sg.OptionMenu(values=main.getConstants("classes"), key="new_class")],
            [sg.T("Father:"), sg.I(key="new_father", size=15),
             sg.T("Mother:"), sg.I(key="new_mother", size=15)],
            [sg.T("Birth Year:"), sg.I(key="new_year", size=5),
             sg.T("Month:"), sg.I(key="new_month", size=3),
             sg.T("Day:"), sg.I(key="new_day", size=3)],
            [sg.T("Phone:"), sg.I(key="new_phone", size=15)],
            [sg.T("Scholarship percentage:"), sg.Slider(
                key="new_scholarship", range=(0, 100), orientation='horizontal')],
            [sg.Button("ADD STUDENT", key="add_student_btn", expand_x=True)]
        ]

        window = sg.Window("New Student", layout, margins=(5, 5), element_justification='c', resizable=False, finalize=True, size=(550, 300), modal=True)

        while True:
            event, values = window.read()
            if event in ("Exit", sg.WIN_CLOSED):
                break
            elif event == "add_student_btn":
                try:
                    if values['new_grade'] == '' or values['new_class'] == '':
                        sg.popup("No grade or class specified.")
                    else:
                        birth = datetime(int(values['new_year']),
                                                int(values['new_month']),
                                                int(values['new_day']))
                        birth = birth.strftime("%Y-%m-%d")
                        newStudent = (values['new_first'], values['new_last'], values['new_father'], values['new_mother'], birth, values['new_phone'], values['new_scholarship'], values['new_grade'], values['new_class'])
                        studentsModel.Students(yearN).add(newStudent)
                        break
                except:
                    sg.popup("Invalid information")
        window.close()

    def edit_student_window(sid):
        student = studentsModel.Students(yearN).getOne(sid)
        birthOBJ = datetime.strptime(student[5], "%Y-%m-%d")

        layout = [
            [sg.T("First:"), sg.I(student[1], key="new_first", size=15),
             sg.T("Last name:"), sg.I(student[2], key="new_last", size=15)],
            [sg.T("Grade:"), sg.OptionMenu(default_value=student[7], values=main.getConstants("grades"), key="new_grade"),
            sg.T("Class:"),
            sg.OptionMenu(default_value=student[8], values=main.getConstants("classes"), key="new_class")],
            [sg.T("Father name:"), sg.I(student[3], key="new_father"),
             sg.T("Mother name:"), sg.I(student[4], key="new_mother")],
            [sg.T("Birth Year:"), sg.I(birthOBJ.year, key="new_year", size=5),
             sg.T("Month:"), sg.I(birthOBJ.month, key="new_month", size=3),
             sg.T("Day:"), sg.I(birthOBJ.day, key="new_day", size=3)],
            [sg.T("Phone number:"), sg.I(student[6], key="new_phone", size=15)],
            [sg.T("Scholarship percentage:"), sg.Slider(default_value=int(
                student[9]), key="new_scholarship", range=(0, 100), orientation='horizontal')],
            [sg.Button("EDIT STUDENT", key="edit_student_btn", expand_x=True)]
        ]

        window = sg.Window("EDIT STUDENT", layout, margins=(10, 10), element_justification='c', resizable=False, finalize=True, size=(550, 300), modal=True)

        while True:
            event, values = window.read()
            if event in ("Exit", sg.WIN_CLOSED):
                break
            elif event == "edit_student_btn":
                try:
                    if values['new_grade'] == 'All' or values['new_class'] == 'All':
                        sg.popup("You need to select both a grade and a class before continuing...")
                        continue
                    birth = datetime(int(values['new_year']),
                                                int(values['new_month']),
                                                int(values['new_day']))
                    birth = birth.strftime("%Y-%m-%d")
                    newStudent = (values['new_first'], values['new_last'], values['new_father'], values['new_mother'], birth, values['new_phone'], values['new_scholarship'], values['new_grade'], values['new_class'])
                    studentsModel.Students(yearN).edit(newStudent, sid)
                    break
                except:
                    sg.popup("Invalid information")
        window.close()

    def view_transactions_window(sid):
        student = studentsModel.Students(yearN).getOne(sid)
        layout = [
            [sg.T("Day:"), sg.I(key="t_day", size=3),
             sg.T("Month:"), sg.I(key="t_month", size=3),
             sg.T("Year:"), sg.I(key="t_year", size=5),
             sg.T("Amount:"), sg.I(key="t_amount", size=(20, 1)), sg.T(main.getCurrency())],
            [sg.Button("ADD", key="add_btn"), sg.Button("DELETE", key="delete_btn"), sg.Button("EDIT", key="edit_btn"), sg.Button("CLEAR", key="clear_btn")],
            [sg.T("Paid: " + "{:,}".format(transactionsModel.Transactions(yearN).getAll(sid)[1]), key="paid_prompt", text_color="green"),
             sg.T("Remaining: " + "{:,}".format(transactionsModel.Transactions(yearN).getAll(sid)[2]), key="remaining_prompt", text_color="red"),
             sg.T("Full Tuition: " + "{:,}".format(transactionsModel.Transactions(yearN).getAll(sid)[3]), key="fee_prompt", text_color="orange"),
             sg.T(main.getCurrency())],
            [sg.Table(values=transactionsModel.Transactions(yearN).getAll(sid)[0], headings=transactionsHeadings, key="-TABLE-",
                      auto_size_columns=True, expand_x=True, expand_y=True, justification='c', enable_events=True, display_row_numbers=True)]
        ]

        window = sg.Window(f"{student[1]} {student[2]} Transactions", layout, margins=(
            10, 10), element_justification='c', resizable=True, finalize=True, size=(750, 400))
        window['-TABLE-'].expand(True, True)

        def clearValues():
            window['t_day'].update(value='')
            window['t_month'].update(value='')
            window['t_year'].update(value='')
            window['t_amount'].update(value='')

        while True:
            event, values = window.read()
            if event in ("Exit", sg.WIN_CLOSED):
                break
            elif event == "clear_btn":
                clearValues()
            elif event == "add_btn":
                try:
                    transactionDate = datetime(values['t_year'], values['t_month'], values['t_day'])
                    transactionDate = transactionDate.strftime("%Y-%m-%d")
                    newTransactionOBJ = (transactionDate,
                                         str(values['t_amount']).replace(',', ''))
                    transactionsModel.Transactions(yearN).add(sid, newTransactionOBJ)
                    newGetTransactions = transactionsModel.Transactions(yearN).getAll(sid)
                    window["-TABLE-"].update(newGetTransactions[0])
                    window["paid_prompt"].update(
                        value="Paid: " + "{:,}".format(newGetTransactions[1]))
                    window["remaining_prompt"].update(
                        value="Remaining: " + "{:,}".format(newGetTransactions[2]))
                    window["fee_prompt"].update(
                        value="Full Tuition: " + "{:,}".format(newGetTransactions[3]))
                    clearValues()
                except:
                    sg.popup("Invalid information")
            elif event == "edit_btn":
                if len(values['-TABLE-']) != 0:
                    # try:
                        currentEntries = window["-TABLE-"].get()
                        i = values['-TABLE-'][0]
                        transactionDate = datetime.strptime(currentEntries[i][0], "%Y-%m-%d")
                        amount = values['t_amount']

                        if values['t_year'] != '':
                            transactionDate = transactionDate.replace(year=int(values['t_year']))

                        if values['t_month'] != '':
                            transactionDate = transactionDate.replace(month=int(values['t_month']))

                        if values['t_day'] != '':
                            transactionDate = transactionDate.replace(day=int(values['t_day']))

                        if values['t_amount'] == '':
                            amount = currentEntries[i][1]

                        transactionDate = transactionDate.strftime("%Y-%m-%d")
                        
                        newTransactionOBJ = (transactionDate, str(amount).replace(',', ''))
                        transactionsModel.Transactions(yearN).edit(currentEntries[i][-1], newTransactionOBJ)
                        newGetTransactions = transactionsModel.Transactions(
                            yearN).getAll(sid)
                        window["-TABLE-"].update(newGetTransactions[0])
                        window["paid_prompt"].update(
                            value="Paid: " + "{:,}".format(newGetTransactions[1]))
                        window["remaining_prompt"].update(
                        value="Remaining: " + "{:,}".format(newGetTransactions[2]))
                        window["fee_prompt"].update(
                        value="Full Tuition: " + "{:,}".format(newGetTransactions[3]))
                        clearValues()
                    # except:
                    #     sg.popup("Invalid information")
            elif event == "delete_btn":
                if len(values["-TABLE-"]) != 0:
                    currentEntries = window["-TABLE-"].get()
                    i = values['-TABLE-'][0]
                    yesNo = sg.popup_yes_no("Do you want to Continue?",  title="YesNo")
                    if yesNo == "No": continue
                    transactionsModel.Transactions(yearN).delete(currentEntries[i][-1])
                    newGetTransactions = transactionsModel.Transactions(
                        yearN).getAll(sid)
                    window["-TABLE-"].update(newGetTransactions[0])
                    window["paid_prompt"].update(
                        value="Paid: " + "{:,}".format(newGetTransactions[1]))
                    window["remaining_prompt"].update(
                    value="Remaining: " + "{:,}".format(newGetTransactions[2]))
                    window["fee_prompt"].update(
                    value="Full Tuition: " + "{:,}".format(newGetTransactions[3]))
                    clearValues()
        window.close()

    def view_reports_window(sid):
        student = studentsModel.Students(yearN).getOne(sid)
        layout = [
            [sg.T("Subject:"), sg.I(key="r_subject", size=(16, 1)), sg.T("Mark:"), sg.I(key="r_mark", size=(5, 1)), sg.T("Full Mark:"), sg.I(
                key="r_full", size=(5, 1)), sg.T("Month:"), sg.I(key="r_month", size=(5, 1)), sg.T("Year:"), sg.I(key="r_year", size=(5, 1))],
            [sg.Button("ADD", key="add_btn"), sg.Button("DELETE", key="delete_btn"), sg.Button(
                "EDIT", key="edit_btn"), sg.Button("CLEAR", key="clear_btn")],
            [sg.Table(values=reportsModel.Reports(yearN).getAll(sid), headings=reportsHeadings, key="-TABLE-",
                      auto_size_columns=True, expand_x=True, expand_y=True, justification='c', enable_events=True, display_row_numbers=True)]
        ]

        window = sg.Window(f"{student[1]} {student[2]} Reports", layout, margins=(
            10, 10), element_justification='c', resizable=True, finalize=True, size=(800, 400))
        window['-TABLE-'].expand(True, True)

        def clearValues():
            window['r_subject'].update(value='')
            window['r_mark'].update(value='')
            window['r_full'].update(value='')
            window['r_month'].update(value='')
            window['r_year'].update(value='')

        while True:
            event, values = window.read()
            if event in ("Exit", sg.WIN_CLOSED):
                break
            elif event == "clear_btn":
                clearValues()
            elif event == "add_btn":
                try:
                    newMarkOBJ = (values['r_subject'], values['r_mark'],
                                values['r_full'], values['r_month'], values['r_year'])
                    reportsModel.Reports(yearN).add(sid, newMarkOBJ)
                    window["-TABLE-"].update(reportsModel.Reports(yearN).getAll(sid))
                    clearValues()
                except:
                    sg.popup("Invalid information")
            elif event == "edit_btn":
                if len(values['-TABLE-']) != 0:
                    try:
                        currentEntries = window["-TABLE-"].get()
                        i = values['-TABLE-'][0]
                        subject, mark, full, month, year = values['r_subject'], values[
                            'r_mark'], values['r_full'], values['r_month'], values['r_year']
                        if values['r_subject'] == '':
                            subject = currentEntries[i][0]
                        if values['r_mark'] == '':
                            mark = currentEntries[i][1]
                        if values['r_full'] == '':
                            full = currentEntries[i][2]
                        if values['r_month'] == '':
                            month = currentEntries[i][3]
                        if values['r_year'] == '':
                            year = currentEntries[i][4]
                        newMarkOBJ = [subject, mark, full, month, year]
                        reportsModel.Reports(yearN).edit(currentEntries[i][-1], newMarkOBJ)
                        window["-TABLE-"].update(
                            reportsModel.Reports(yearN).getAll(sid))
                        clearValues()
                    except:
                        sg.popup("Invalid information")
            elif event == "delete_btn":
                if len(values["-TABLE-"]) != 0:
                    currentEntries = window["-TABLE-"].get()
                    selectedValues = values["-TABLE-"]
                    yesNo = sg.popup_yes_no("Do you want to Continue?",  title="YesNo")
                    if yesNo == "No": continue
                    for i in selectedValues:
                        reportsModel.Reports(yearN).delete(currentEntries[i][-1])
                    window["-TABLE-"].update(
                        reportsModel.Reports(yearN).getAll(sid))
                    clearValues()
        window.close()

    def view_class_report_window(gradeN, classN):

        studentsList = studentsModel.Students(yearN).getAll(gradeN, classN, '')

        def create_rows(items):
            rows = []
            counter = 1
            for i in items:
                row = [sg.Text(f"{i[0]} {i[1]}:", expand_x=True),
                       sg.Input(size=(4, 1), key=f"selected_input{counter}")]
                rows.append(row)
                counter += 1
            return rows

        rows = create_rows(studentsList)

        layout = [
            [sg.T("Subject:"), sg.I(key="subject", size=(16, 1))],
            [sg.T("Full Mark:"), sg.I(key="full", size=(5, 1))],
            [sg.T("Month:"), sg.I(key="month", size=(4, 1)),
             sg.T("Year:"), sg.I(key="year", size=(4, 1))],
            [sg.T("Grade:"), sg.I(size=(3, 1), disabled=True, default_text=gradeN),
             sg.T("Class:"), sg.I(size=(3, 1), disabled=True, default_text=classN)],
            [sg.Button("SAVE REPORTS", key="save_reports", expand_x=True)],
            [sg.Column(rows, scrollable=True, vertical_scroll_only=True,
                       element_justification='center', justification='center',
                       expand_y=True, pad=0)]
        ]

        window = sg.Window("Insert Class Report", layout, margins=(
            10, 10), element_justification='c', resizable=False, finalize=True, size=(300, 450))

        while True:
            event, values = window.read()
            if event in ("Exit", sg.WIN_CLOSED):
                break
            elif event == "save_reports":
                try:
                    counter = 1
                    for i in studentsList:
                        newMark = [values['subject'], values[f'selected_input{counter}'], values['full'],
                                values['month'], values['year']]
                        reportsModel.Reports(yearN).add(i[-1], newMark)
                        counter += 1
                    break
                except:
                    sg.popup("Invalid information")
        window.close()

    layout = [
        [sg.T("Search:"), sg.I(key="search_input", size=(32, 1)),
         sg.T("Grade:"), sg.OptionMenu(values=main.getConstants("grades"), default_value='All', key="gradeNum"),
         sg.T("Class:"), sg.OptionMenu(values=main.getConstants("classes"), default_value='All', key="classNum"),
         sg.Button("Search", key="search_btn")],
        [sg.Button("VIEW REPORTS", key="view_reports_btn"), sg.Button("VIEW TRANSACTIONS", key="view_transactions_btn"), sg.Button(
            "INSERT CLASS REPORT", key="class_report_btn"), sg.Button("ADD", key="add_btn"), sg.Button("DELETE", key="delete_btn"), sg.Button("EDIT", key="edit_btn")],
        [sg.Table(values=[], headings=studentsHeadings, key="-TABLE-", auto_size_columns=True,
                  expand_x=True, expand_y=True, justification='c', enable_events=True, display_row_numbers=True)]
    ]

    window = sg.Window("Students List", layout, margins=(
        10, 10), element_justification='c', resizable=True, finalize=True, size=(1100, 500))
    window['-TABLE-'].expand(True, True)

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "search_btn":
            window['-TABLE-'].update(studentsModel.Students(yearN).getAll(values['gradeNum'], values['classNum'], values['search_input']))
        elif event == "view_reports_btn":
            if len(values["-TABLE-"]) != 0:
                currentEntries = window["-TABLE-"].get()
                for i in values["-TABLE-"]:
                    view_reports_window(currentEntries[i][-1])
        elif event == "view_transactions_btn":
            if len(values["-TABLE-"]) != 0:
                currentEntries = window["-TABLE-"].get()
                for i in values["-TABLE-"]:
                    view_transactions_window(currentEntries[i][-1])
        elif event == "class_report_btn":
            if values['gradeNum'] == 'All' or values['classNum'] == 'All':
                sg.popup("Select a grade and a class before continuing...")
                continue
            else:
                view_class_report_window(values['gradeNum'], values['classNum'])
        elif event == "add_btn":
            new_student_window()
            window['-TABLE-'].update(studentsModel.Students(yearN).getAll(
                values['gradeNum'], values['classNum'], values['search_input']))
        elif event == "delete_btn":
            if len(values["-TABLE-"]) != 0:
                currentEntries = window["-TABLE-"].get()
                selectedValues = values["-TABLE-"]
                yesNo = sg.popup_yes_no("Do you want to Continue?",  title="YesNo")
                if yesNo == "No": continue
                for i in selectedValues:
                    studentsModel.Students(yearN).delete(currentEntries[i][-1])
                window['-TABLE-'].update(studentsModel.Students(yearN).getAll(
                    values['gradeNum'], values['classNum'], values['search_input']))
        elif event == "edit_btn":
            if len(values["-TABLE-"]) != 0:
                currentEntries = window["-TABLE-"].get()
                for i in values["-TABLE-"]:
                    edit_student_window(currentEntries[i][-1])
                window['-TABLE-'].update(studentsModel.Students(yearN).getAll(
                    values['gradeNum'], values['classNum'], values['search_input']))
    window.close()
