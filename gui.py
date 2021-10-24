import PySimpleGUI as psg


def run_gui(input_folder, output_folder, output_file, fr):
    # theme
    psg.theme('SystemDefault')

    # components inside window
    layout = [[psg.Text('Default input folder: ' + input_folder, font=(None, 8))],
              [psg.Text('Default output folder: ' + output_folder, font=(None, 8))],
              [psg.Text('Input Folder:', size=(15, None)), psg.FolderBrowse(key='input_folder', initial_folder=input_folder)],
              [psg.Text('Output Folder:', size=(15, None)), psg.FolderBrowse(key='output_folder', initial_folder=output_folder)],
              [psg.Text('Output File Name:', size=(15, None)), psg.InputText(key='output_file', default_text=output_file)],
              [psg.Text('Frame Rate:', size=(15, None)), psg.InputText(key='fr', default_text=fr)],
              [psg.Button('Enter'), psg.Button('Cancel')]]

    # create window
    window = psg.Window('Madeline Analysis', layout)

    # process inputs
    window_closed = False
    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED or event == 'Cancel':
            window_closed = True
            break
        if event == 'Enter':
            break
        print('You entered', values['input_folder'], values['output_folder'], values['fr'])
        if not values['fr'].isdigit():
            print('Error: framerate should be an integer')
        else:
            fr = int(values['fr'])
            output_file = values['output_file']
            if values['input_folder'] != '':
                input_folder = values['input_folder']
            if values['output_folder'] != '':
                output_folder = values['output_folder']

    window.close()
    if window_closed:
        print('operation canceled.')
        return None
    if input_folder == '' or output_folder == '' or output_file == '':
        print('invalid input.')
        return None
    print('gui.py: returning', input_folder, output_folder, output_file, fr)
    return input_folder, output_folder, output_file, fr
