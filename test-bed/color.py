import curses

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    row = 0
    col = 0
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    try:
        for i in range(0, 255):
            stdscr.addstr(row, col, str(i), curses.color_pair(i))
            col += 4
            if (i+1) % 36 == 0:
                row += 1
                col = 0
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()

curses.wrapper(main)
