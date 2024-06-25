import curses
import sbr
import device_control

def main(stdscr):
    curses.echo()

    # Show available slot numbers before asking for which slot numbers to test
    stdscr.addstr(0, 0, "Available slot numbers:\n")
    slot_numbers = sbr.get_slot_numbers()
    for i, slot in enumerate(slot_numbers):
        stdscr.addstr(i + 1, 0, slot)
    stdscr.refresh()
    stdscr.addstr(len(slot_numbers) + 2, 0, "Press any key to continue...\n")
    stdscr.getch()
    stdscr.clear()

    stdscr.addstr(0, 0, "Enter your password (sudo access): ")
    user_password = stdscr.getstr().decode()

    stdscr.addstr(1, 0, "Number of Loops: ")
    inputnum_loops = int(stdscr.getstr().decode())

    stdscr.addstr(2, 0, "Do you want to kill on error? (y/n): ")
    kill = stdscr.getstr().decode()

    stdscr.addstr(3, 0, "Choose slot numbers to test (comma separated): ")
    slot_input = stdscr.getstr().decode()
    slotlist = list(map(int, slot_input.split(',')))

    stdscr.clear()
    stdscr.addstr(0, 0, "Starting the test with the following parameters:\n")
    stdscr.addstr(1, 0, f"Password: {'*' * len(user_password)}\n")
    stdscr.addstr(2, 0, f"Number of Loops: {inputnum_loops}\n")
    stdscr.addstr(3, 0, f"Kill on error: {kill}\n")
    stdscr.addstr(4, 0, f"Slot numbers to test: {slotlist}\n")
    stdscr.refresh()
    stdscr.addstr(6, 0, "Press any key to continue...\n")
    stdscr.getch()

    # Set error reporting to 0
    bdfs = device_control.get_all_bdfs()
    device_control.store_original_values(bdfs)
    device_control.process_bdfs(bdfs)

    # Run the sbr functionality
    sbr.run_test(stdscr, user_password, inputnum_loops, kill, slotlist)

    # Reset device control registers to original values
    device_control.reset_to_original_values()

curses.wrapper(main)
