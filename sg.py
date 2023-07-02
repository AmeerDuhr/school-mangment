import PySimpleGUI as sg
import Models.init as main
import Views.students as sv
import Views.fess as fv
import Views.print as pv
import Views.settings as settv

sg.set_options(font=("Open Sans Regular", 12))
sg.theme(main.getTheme()[1])

def main_window():

    layout = [
        [sg.T("Scholar Year:"),
         sg.OptionMenu(key="school_year", values=main.getConstants("years"), default_value=main.getConstants("years")[0])],
        [sg.Button("Students List", key="open_students_list", expand_x=True)],
        [sg.Button("Print Reports", key="print_reports", expand_x=True)],
        # [sg.Button("Employees List", key="open_employees_list", expand_x=True)],
        [sg.Button("Fees List", key="open_fees_list", expand_x=True)],
        # [sg.Button("Users List", key="open_users_list", expand_x=True)],
        [sg.Button("Settings", key="open_settings", expand_x=True)]
        ]

    window = sg.Window("School Management", layout, margins=(
        10, 10), element_justification='c', resizable=False, finalize=True, size=(400, 300))

    def noYearValue(): # popup if no value, initiateDB if there is
        if values['school_year'] == '':
                sg.popup('Select a scholar year.')
                return True
        else:
            main.initiateDatabase(values['school_year'])
            return False

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "open_students_list":
            if noYearValue(): continue
            sv.students_window(str(values['school_year']))
        elif event == "print_reports":
            if noYearValue(): continue
            pv.print_reports_menu(values['school_year'])
        # elif event == "open_employees_list":
        #     pass
        elif event == "open_fees_list":
            if noYearValue(): continue
            fv.fess_window(values['school_year'])
        elif event == "open_settings":
            settv.settings_window()
    window.close()

if __name__ == "__main__":
    main_window()
