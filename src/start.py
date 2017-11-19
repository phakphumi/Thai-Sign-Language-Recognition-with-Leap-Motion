import main, settings, utils

# Import the modules needed to run the script.
import sys, os, time, threading, cv2

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

def main_menu():
    clear_screen()

    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Start"
    print "\nq. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '1': menu_enter_name,
        'q': exit,
    })

    return

# Execute menu
def exec_menu(choice, action):
    ch = choice.lower()
    if ch == 'm':
        main_menu()
    else:
        try:
            action[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            main_menu()
    return

# Menu Name
def menu_enter_name():
    clear_screen()

    default = settings.file_name
    default_str = default and ('['+ default +']') or ''

    name = raw_input("Enter File's name " + default_str + ": >>")
    main.set_settings('file_name', name or default)

    utils.create_folder(settings.path + '/' + settings.file_name)

    menu_enter_index()

# Menu Index
def menu_enter_index():
    default = int(utils.get_last_index_from_folder(settings.path + '/' + settings.file_name)) + 1
    default_str = ('['+ str(default) +']') or ''

    index = default

    index_raw = raw_input("Enter File's index " + default_str + " : >> ")

    if (index_raw == 'q') :
        exit()
        return
    elif (index_raw != '') :
        index = int(index_raw)

    main.set_settings('file_index', index)

    menu_record_preparing()

# Menu Record Decision
def menu_record_preparing():
    clear_screen()

    print "Record Menu,\n"
    print "Please choose the menu you want to start:"
    print "(Enter) Start record '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + "'"
    print "(2) Edit Name & Index"
    print "\nq. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '': menu_start_record,
        '2': menu_enter_name,
        'q': exit,
    })

    return

def menu_show_ready_list () :
    clear_screen()
    print 'Device ready list (Waiting for all true) : '
    for key, value in settings.is_ready.iteritems() :
        print key, value

def is_device_on () :
    while (True) :
        if main.is_all_ready() :
            break
        time.sleep(0.100)
        menu_show_ready_list()

def menu_show_recording (start_record) :
    while settings.is_recording :
        clear_screen()
        print "\nRecording.....,\n"
        print '\nTime : ', time.time() - start_record
        print '\nLeft hand  : ', '[X]' if settings.hands['left'] else '[_]'
        print 'Right hand : ', '[X]' if settings.hands['right'] else '[_]'
        print '\n\n to Stop press Enter ! '
        time.sleep(0.050)

# Menu Start Record
def menu_start_record():
    is_device_on()

    clear_screen()

    print "Files : '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + "'"
    choice = raw_input(" Start ? ")


    main.start_record()
    start_record = time.time()

    t = threading.Thread(name='menu_show_recording', target=menu_show_recording, args=([start_record]))
    t.start()

    conclusion_screen(start_record)

# Conclusion screen
def conclusion_screen (start_record) :
    choice = raw_input()
    main.stop_record()
    clear_screen()

    print '\nTotal time : ' + str(time.time() - start_record)
    print '\nWriting Files...'
    main.wait_for_finish()
    print '\nDone'

    print "\nNext index,\n"
    menu_enter_index()

    return

# Exit program
def exit():
    main.exit()
    sys.exit()

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # pass

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Initialized Settings
    settings.init()
    # Initialized Cameras
    main.init()
    # Launch main menu
    main_menu()
