import sys
import threading
import pulsectl
import curses


pulse = pulsectl.Pulse('pulse-volume-control')

class sink:
    def __init__(self, sink_index):
        self.sink_index = sink_index
        self.sink_obj = pulse.sink_list()[sink_index]
        self.current_vol = pulse.volume_get_all_chans(self.sink_obj)


    def change_vol(self, shift_step):
        changed_vol = self.current_vol + shift_step
        pulse.volume_set_all_chans(self.sink_obj, changed_vol)
        


def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    
    #max_height,max_width = stdscr.getmaxyx()
    
    #bar_width = max_width
    #for char in range(bar_width):
    #    stdscr.addch(1,char,'=')

    print_vol(stdscr)

    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == ord('a'):
            sink(0).change_vol(-0.01)
            print_vol(stdscr)
            stdscr.clrtoeol()
            #stdscr.refresh()
        elif key == ord('d'):
            sink(0).change_vol(0.01)
            print_vol(stdscr)
            stdscr.clrtoeol()
            #stdscr.refresh()
        

    curses.endwin()

def print_vol(stdscr):
    vol_level = '{:.0%}'.format(sink(0).current_vol)
    stdscr.addstr(0,0,vol_level)

if __name__ == "__main__":
    main()
    