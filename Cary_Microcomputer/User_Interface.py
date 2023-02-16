import os
import time
import string
import PySimpleGUI as sg

sg.theme('Light Brown 6')  # Set Theme
fonts = ('Any', 20)
image_file = os.path.abspath('Cary_Microcomputer/Cary.png')

first_column = [[sg.Text('Hi, I\'m Cary! How can I help you today?', font=('Any', 30),
                         justification='left', pad=((0, 0), (50, 0)))],
                [sg.Text('Current Time is: ', font=(
                    'Any', 20), justification='center')],
                [sg.Text('', key='timetext', font=(
                    'Any', 20), justification='center')],
                [sg.Text('')],
                [sg.Button('Change Schedule', font=('Any', 10), expand_x=True,
                           expand_y=True, size=(15, 2), key="-SCH-", enable_events=True)],
                [sg.Button('Update Users', font=('Any', 10), expand_x=True,
                           expand_y=True, key='-UPD-', enable_events=True, size=(15, 2))],
                [sg.Button('Refill', font=('Any', 10), expand_x=True, expand_y=True, size=(15, 2))]]

second_column = [[sg.Image(filename=image_file)]]

layout = [[sg.Column(first_column), sg.VSeparator(), sg.Column(second_column)]]

window = sg.Window('Cary', layout, finalize=True,
                   size=(800, 480), element_justification='c')
window['timetext'].update(time.strftime('%I:%M %p'))

win2_active = False
while True:
    # GUI Button management
    users = []

    with open(os.path.abspath('Cary_Microcomputer/users.txt')) as file:
        for line in file.readlines():
            users.append(line)

    event, values = window.read(timeout=10)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-UPD-' and not win2_active:
        win2_active = True
        window.Hide()
        win2_col1 = [[sg.Text('List of current users:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('\n'.join([str(i) for i in users]),
                              font=('Any', 15), justification='left', key='-USR-')]]
        win2_col2 = [[sg.Text('What would you like to do?', size=(25, 2),
                              font=('Any', 25), justification='center', pad=((0, 0), (50, 0)))],
                     [sg.Button('Add a New User', key='-ADD-', font=('Any', 10),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Remove a User', font=('Any', 10),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Back', font=('Any', 10), expand_x=True, expand_y=True, size=(15, 2), key='-BACK-')]]
        win2_layout = [
            [sg.Column(win2_col1), sg.VerticalSeparator(), sg.Column(win2_col2)]]

        win2 = sg.Window('Users', win2_layout, modal=True,
                         finalize=True, size=(800, 480))
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED:
                win2.Close()
                win2_active = False
                window.UnHide()
                break
            if ev2 == "-BACK-":
                win2.Close()
                win2_active = False
                window.UnHide()
            if ev2 == "-ADD-":
                win2.Hide()
                win2_active = False
                initials = list(string.ascii_uppercase)
                roles = ["Caregiver", "User"]
                win3_col1 = [[sg.Text('Add a new user using the buttons below.', font=('Any', 25),
                                expand_x=True, expand_y=False, size=(15, 2), justification='c', pad=(0, 20))],
                             [sg.Text("First Initial"), sg.Spin(initials, expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-IN1-'),
                              sg.Text("Second Initial"), sg.Spin(initials, expand_x=True, readonly=True,
                                enable_events=True, text_color='black', expand_y=True, key='-IN2-'),
                              sg.Text("Third Initial"), sg.Spin(initials, expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-IN3-'),
                              sg.Text("Role"), sg.Spin(roles, expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-ROL-')],
                             [sg.Button('Save', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-SAVE-', pad=(0, 20)),
                              sg.Button('Cancel', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 20))]]
                win3 = sg.Window('Add New User', win3_col1, finalize=True, size=(
                    800, 480), element_justification='c')
                while True:
                    ev3, vals3 = win3.Read()
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    elif ev3 == '-SAVE-':
                        person = str(vals3['-IN1-'] + vals3['-IN2-'] + vals3['-IN3-'] + " - " + vals3['-ROL-'])
                        with open(os.path.abspath('Cary_Microcomputer/users.txt'), 'a') as f:
                            f.write(person + '\n')
                            users.append(person)
                        win3.Close()
                        win2['-USR-'].update('\n'.join([str(i) for i in users]))
                        win2.UnHide()

    # Update the time :
    window['timetext'].update(time.strftime('%I:%M %p'))

window.close()
