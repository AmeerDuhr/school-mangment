import PySimpleGUI as sg
import Models.init as main

def settings_window():
    layout = [
        [sg.T("Scholar Year:"),
         sg.Combo(key="years", values=main.getConstants("years")),
         sg.Button("New Year", key="add_new_year_btn", expand_x=True)],
         [sg.T("Grades:"),
         sg.Combo(key="grades", values=main.getConstants("grades")),
         sg.Button("New Grade", key="add_new_grade_btn", expand_x=True)],
         [sg.T("Classes:"),
         sg.Combo(key="classes", values=main.getConstants("classes")),
         sg.Button("New Class", key="add_new_class_btn", expand_x=True)],
         [sg.T("Currencies:"),
          sg.OptionMenu(key="currencies", values=main.currencies, default_value=main.getCurrency()),
          sg.Button("Set Currency", key="set_new_currency_btn", expand_x=True)],
         [sg.T("Themes:"),
         sg.OptionMenu(key="themes", values=main.themesList, default_value=main.getTheme()[0]), sg.Button("Set Theme", key="set_new_theme", expand_x=True)],
    ]

    window = sg.Window("Settings", layout, margins=(10, 10), element_justification='l', resizable=False, finalize=True, size=(550, 250), modal=True)

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        elif event == "add_new_year_btn":
            if values['years'] == '':
                sg.popup('Provide a Value')
                continue
            main.addConstant("years", values['years'])
            window['years'].update(values=main.getConstants("years"))
            sg.popup("Restart the app for any changes to be visible")
        elif event == "add_new_grade_btn":
            if values['grades'] == '':
                sg.popup('Provide a Value')
                continue
            main.addConstant("grades", values['grades'])
            window['grades'].update(values=main.getConstants("grades"))
        elif event == "add_new_class_btn":
            if values['classes'] == '':
                sg.popup('Provide a Value')
                continue
            main.addConstant("classes", values['classes'])
            window['classes'].update(values=main.getConstants("classes"))
        elif event == "set_new_currency_btn":
            main.setCurrency(values['currencies'])
        elif event == "set_new_theme":
            main.setTheme(values['themes'])
            sg.popup("Restart the app for any changes to be visible")
    window.close()