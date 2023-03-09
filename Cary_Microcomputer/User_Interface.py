import os
import time
import string
import PySimpleGUI as sg

###### Setting up the initial screen ####
sg.theme('Light Brown 6')  # Set Theme
fonts = ('Any', 20)
image_file = os.path.abspath('Cary.png')

first_column = [[sg.Text('Hi, I\'m Cary! How can I help you today?', font=('Any', 20), justification='left', pad=((0, 0), (50, 0)))],
                [sg.Text('Current Time is: ', font=('Any', 20), justification='center')],
                [sg.Text('', key='timetext', font=('Any', 20), justification='center')],
                [sg.Text('')],
                [sg.Button('Change Schedule', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key="-SCH-", enable_events=True)],
                [sg.Button('Update Users', font=('Any', 20), expand_x=True, expand_y=True, key='-UPD-', enable_events=True, size=(15, 2))],
                [sg.Button('Refill', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-REFILL-')]]

second_column = [[sg.Image(filename=image_file)]]
layout = [[sg.Column(first_column), sg.VSeparator(), sg.Column(second_column)]]
window = sg.Window('Cary', layout, finalize=True,
                   size=(800, 480), element_justification='c', location=(0, 1080))
window['timetext'].update(time.strftime('%I:%M %p'))

while True:
    # GUI Button management
    users = []
    regime = [[] for i in range(8)]

    with open(os.path.abspath('users.txt')) as file:
        for line in file.readlines():
            users.append(line.strip('\n'))
    
    with open(os.path.abspath('medications.txt')) as file:
        for line in file.readlines():
            times = line.split(' ')
            index = int(times[0].strip('.')) - 1
            for i in range(1, len(times)):
                regime[index].append((times[i].strip(',')).strip('\n'))

    event, values = window.read(timeout=10)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-UPD-':
        window.Hide()
        win2_col1 = [[sg.Text('List of current users:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Text('\n'.join([str(i) for i in users]),
                              font=('Any', 15), justification='left', key='-USR-')]]
        win2_col2 = [[sg.Text('What would you like to do?',
                              font=('Any', 20), justification='center', size=(15,2))],
                     [sg.Text('')],
                     [sg.Button('Add a New User', key='-ADD-', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Remove a User', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2), key='-REM-')],
                     [sg.Button('Back', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-BACK-')]]
        win2_layout = [
            [sg.Column(win2_col1, pad=((0,0), (0, 0))), sg.VerticalSeparator(), sg.Column(win2_col2, pad=((0,0), (50, 0)))]]

        win2 = sg.Window('Users', win2_layout, modal=True,
                         finalize=True, size=(800, 480), location=(0, 1080))
        while True:
            ev2, vals2 = win2.read()
            if ev2 == sg.WIN_CLOSED:
                win2.Close()
                window.UnHide()
                break
            if ev2 == "-BACK-":
                win2.Close()
                window.UnHide()
            if ev2 == "-ADD-":
                win2.Hide()
                initials = list(string.ascii_uppercase)
                roles = ["Caregiver", "User"]
                win3_layout = [[sg.Text('Add a new user using the buttons below.', font=('Any', 25),
                                      expand_x=True, expand_y=False, size=(20, 2), justification='c', pad=(0, 20))],
                             [sg.Text("First Initial"), sg.Spin(initials, expand_x=True, readonly=False, enable_events=True, text_color='black', expand_y=True, key='-IN1-', font=('Any', 20)),
                              sg.Text("Second Initial"), sg.Spin(initials, expand_x=True, readonly=False,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-IN2-', font=('Any', 20)),
                              sg.Text("Third Initial"), sg.Spin(initials, expand_x=True, readonly=False,
                                                                enable_events=True, text_color='black', expand_y=True, key='-IN3-', font=('Any', 20)),
                              sg.Text("Role"), sg.Spin(roles, expand_x=True, readonly=False, enable_events=True, text_color='black', expand_y=True, key='-ROL-', font=('Any', 20))],
                             [sg.Button('Save', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-SAVE-', pad=(0, 20)),
                              sg.Button('Cancel', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), pad=(0, 20), enable_events=True, key='-CANC-')]]
                win3 = sg.Window('Add New User', win3_layout, finalize=False, size=(800, 480), element_justification='c', location=(0, 1080))
                while True:
                    ev3, vals3 = win3.read()
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    elif ev3 == '-SAVE-':
                        person = str(
                            vals3['-IN1-'] + vals3['-IN2-'] + vals3['-IN3-'] + " - " + vals3['-ROL-'])
                        with open(os.path.abspath('Cary_Microcomputer/users.txt'), 'a') as f:
                            f.write(person + '\n')
                            users.append(person)
                        win3.Close()
                        win2['-USR-'].update('\n'.join([str(i) for i in users]))
                        win2.UnHide()
            if ev2 == '-REM-':
                win2.Hide()
                win3_col1 = [[sg.Text('List of current users:', size=(15, 2), font=('Any', 25), justification='center')],
                     [sg.Text('\n'.join([str(str(idx + 1) + '. ' + user) for idx, user in enumerate(users)]),
                              font=('Any', 15), justification='left', key='-USR-')]]
                win3_col2 = [[sg.Text('Select a User to Remove', font=('Any', 20), pad=((0,0), (25, 10)))],
                              [sg.Spin([str(i) for i in range(1, len(users) + 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-SEL-', font=('Any', 50))],
                              [sg.Button('Delete', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-DEL-', pad=(0, 20)),
                               sg.Button('Done', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 20))]]
                win3_layout = [[sg.Column(win3_col1, pad=((0,0), (50, 0))), sg.VerticalSeparator(), sg.Column(win3_col2, pad=((0,0), (100, 0)))]]
                win3 = sg.Window('Remove a User', win3_layout, finalize=True, size=(800, 480), element_justification='c', location=(0, 1080))
                while True:
                    ev3, vals3 = win3.Read()
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    elif ev3 == '-SAVE-':
                        person = str(
                            vals3['-IN1-'] + vals3['-IN2-'] + vals3['-IN3-'] + " - " + vals3['-ROL-'])
                        with open(os.path.abspath('Cary_Microcomputer/users.txt'), 'a') as f:
                            f.write(person + '\n')
                            users.append(person)
                        win3.Close()
                        win2['-USR-'].update('\n'.join([str(i)
                                             for i in users]))
                        win2.UnHide()
                    elif ev3 == '-DEL-':
                        if len(users) == 0:
                            break
                        to_pop = int(vals3['-SEL-']) - 1
                        if len(users) != 0 and to_pop < len(users): users.pop(to_pop)
                        with open(os.path.abspath('Cary_Microcomputer/users.txt'), 'w') as f:
                            for person in users:
                                f.write(person + '\n')
                        win3['-USR-'].update('\n'.join([str(str(idx + 1) + '. ' + user) for idx, user in enumerate(users)]))
                        win2['-USR-'].update('\n'.join([str(i)
                                             for i in users])) 
                        win3['-SEL-'].update([str(i) for i in range(1, len(users))])
    elif event == '-SCH-':
        window.Hide()
        win2_col1 = [[sg.Text('List of current medications:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Text('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]),
                              font=('Any', 15), justification='left', key='-REG-')]]
        win2_col2 = [[sg.Text('What would you like to do?', size=(15, 2),
                              font=('Any', 25), justification='center')],
                     [sg.Text('')],
                     [sg.Button('Add Medication Schedule', key='-ADD-', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2))],
                     [sg.Button('Remove a Medication', font=('Any', 20),
                                expand_x=True, expand_y=True, size=(15, 2), key='-REM-')],
                     [sg.Button('Back', font=('Any', 20), expand_x=True, expand_y=True, size=(15, 2), key='-BACK-')]]
        win2_layout = [
            [sg.Column(win2_col1, pad=((0,0), (0, 0))), sg.VerticalSeparator(), sg.Column(win2_col2, pad=((0,0), (50, 0)))]]

        win2 = sg.Window('Users', win2_layout, modal=True,
                         finalize=True, size=(800, 480), location=(0, 1080)) 
        while True:
            ev2, vals2 = win2.Read()
            if ev2 == sg.WIN_CLOSED or ev2 == '-BACK-':
                win2.Close()
                window.UnHide()
                break
            elif ev2 == '-ADD-':
                win2.Hide()
                minutes = ['00', '15', '30', '45']
                win3_layout = [[sg.Text('Add a new medication schedule using the buttons below.', font=('Any', 25),
                                      expand_x=True, expand_y=False, size=(15, 2), justification='c', pad=(0, 20))],
                             [sg.Text("Medication Number"), sg.Spin([i + 1 for i in range(8)], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-IN1-', font=('Any', 20)),
                              sg.Text("Hour"), sg.Spin([i for i in range(1, 13, 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-IN2-', font=('Any', 20)),
                              sg.Text("Minutes"), sg.Spin(minutes, expand_x=True, readonly=True,
                                                                enable_events=True, text_color='black', expand_y=True, key='-IN3-', font=('Any', 20)),
                              sg.Spin(['am', 'pm'], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-AMPM-', font=('Any', 20)),
                              sg.Text("to"),
                              sg.Text("Hour"), sg.Spin([i for i in range(1, 13, 1)], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-IN4-', font=('Any', 20)),
                              sg.Text("Minutes"), sg.Spin(minutes, expand_x=True, readonly=True,
                                                                enable_events=True, text_color='black', expand_y=True, key='-IN5-', font=('Any', 20)),
                              sg.Text(""), sg.Spin(['am', 'pm'], expand_x=True, readonly=True, enable_events=True, text_color='black', expand_y=True, key='-AMPM2-', font=('Any', 20))],
                             [sg.Button('Save', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-SAVE-', pad=(0, 20)),
                              sg.Button('Cancel', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 20))]]
                win3 = sg.Window('Add New Medication', win3_layout, finalize=True, size=(800, 480), element_justification='c')
                while True:
                    ev3, vals3 = win3.Read()
                    if ev3 == sg.WIN_CLOSED or ev3 == '-CANC-':
                        win3.Close()
                        win2.UnHide()
                        break
                    elif ev3 == '-SAVE-':
                        time_interval = str(vals3['-IN2-']) + ':' + str(vals3['-IN3-'])
                        time_interval += str(vals3['-AMPM-']) + '-'
                        time_interval += str(vals3['-IN4-']) + ':' + str(vals3['-IN5-']) + str(vals3['-AMPM2-'])

                        if time_interval not in regime[vals3['-IN1-']]:
                            regime[int(vals3['-IN1-']) - 1].append(time_interval)

                        with open(os.path.abspath('Cary_Microcomputer/medications.txt'), 'w') as f:
                            for idx, i in enumerate(regime):
                                if len(i) != 0:
                                    f.write(str(idx + 1) + '. ' + ', '.join([str(j) for j in i]))
                                    f.write('\n')

                        win3.Close()
                        win2['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win2.UnHide()
            elif ev2 == '-REM-':
                win2.Hide()
                win3_col1 = [[sg.Text('List of current medications:', size=(20, 2), font=('Any', 25), justification='center')],
                     [sg.Text('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]),
                              font=('Any', 15), justification='left', key='-REG-')]]
                win3_col2 = [[sg.Text('Select a Medication to Remove', font=('Any', 20), pad=((0,0), (25, 10)))],
                              [sg.Spin([str(idx + 1) for idx, i in enumerate(regime) if len(i) > 0], expand_x=True, readonly=True,
                                                                 enable_events=True, text_color='black', expand_y=True, key='-SEL-', font=('Any', 50))],
                              [sg.Button('Delete', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-DEL-', pad=(0, 20)),
                               sg.Button('Done', font=('Any', 10), expand_x=True, expand_y=False, size=(15, 2), key='-CANC-', pad=(0, 20))]]
                win3_layout = [[sg.Column(win3_col1, pad=((0,0), (50, 0))), sg.VerticalSeparator(), sg.Column(win3_col2, pad=((0,0), (100, 0)))]]
                win3 = sg.Window('Remove a Medication', win3_layout, finalize=True, size=(800, 480), element_justification='c') 
                while True:
                    ev3, vals3 = win3.Read()
                    if ev3 == '-CANC-' or sg.WIN_CLOSED:
                        win3.Close()
                        win2.UnHide()
                        break
                    elif ev3 == '-DEL-':
                        to_pop = int(vals3['-SEL-']) - 1
                        regime[to_pop] = []
                        with open(os.path.abspath('Cary_Microcomputer/medications.txt'), 'w') as f:
                            for idx, i in enumerate(regime):
                                if len(i) != 0:
                                    f.write(str(idx + 1) + '. ' + ', '.join([str(j) for j in i]))
                                    f.write('\n')
                                    
                        win3['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win2['-REG-'].update('\n'.join([str(idx + 1) + '. ' + ', '.join(str(j) for j in i) for idx, i in enumerate(regime) if len(i) > 0]))
                        win3['-SEL-'].update([str(idx + 1) for idx, i in enumerate(regime) if len(i) > 0])
    elif event == '-REFILL-':
        # sg.popup_no_buttons("Unlocking!", font=('Any', 25), auto_close_duration=5)
        sg.popup_auto_close("Unlocking!", font=('Any', 25), non_blocking=True)                

    # Update the time :
    window['timetext'].update(time.strftime('%I:%M %p'))

window.close()
