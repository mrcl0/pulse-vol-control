import sys
import threading
import pulsectl
import curses
import itertools
import argparse

parser = argparse.ArgumentParser(description='Control audio volume via terminal.')
parser.add_argument('-i', type=str, metavar='true/false', default="true",  help='Show volume percentage value')
parser.add_argument('-b', type=str, metavar='true/false', default="true",  help='Show volume bar')
parser.add_argument('-d', type=str, metavar='true/false', default="true",  help='Show the number of current device')

args = parser.parse_args()

pulse = pulsectl.Pulse('pulse-volume-control')

class sink:
    def __init__(self,sink_index):
        self.max_index = len(pulse.sink_list())

        self.sink_index = sink_index
        self.sink_obj = pulse.sink_list()[sink_index]
        self.current_vol = pulse.volume_get_all_chans(self.sink_obj)

    def change_vol(self,shift_step):
        changed_vol = self.current_vol + shift_step
        pulse.volume_set_all_chans(self.sink_obj,changed_vol)
        

def main():
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    stdscr.keypad(1)

    index_array = []
    for i in range(10):
        try:
            pulse.sink_list()[i]
            index_array.append(i)
        except IndexError:
            break

    index_iter = itertools.cycle(index_array)
    current_index = next(index_iter)

    print_elements(stdscr,current_index)
    #screen.nodelay(1)
    while True:
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif (key == ord('a')) or (key == curses.KEY_LEFT):
            try:
                sink(current_index).change_vol(-0.01)
                print_elements(stdscr,current_index)
            except (pulsectl.pulsectl.PulseOperationInvalid):
                pulse.volume_set_all_chans(sink(current_index).sink_obj,0)

        elif key == ord('d') or (key == curses.KEY_RIGHT):
            sink(current_index).change_vol(0.01)
            print_elements(stdscr,current_index)

        elif key == ord('w') or (key == curses.KEY_UP):
            current_index = next(index_iter)
            print_elements(stdscr,current_index)

        elif key == ord('s') or (key == curses.KEY_DOWN):
            current_index = next(index_iter)
            print_elements(stdscr,current_index)
        

    curses.endwin()


def print_elements(stdscr,sink_index):
    stdscr.move(0,0)
    stdscr.clrtoeol()

    #Show volume level
    if args.i == "true":
        vol_level = "Volume: "+'{:.0%}'.format(sink(sink_index).current_vol)
        stdscr.addstr(0,11,vol_level)


    #Show current sink index
    if args.d == "true":
        index = "Device: "+str(sink_index)
        stdscr.addstr(0,0,index)

    #Show volume level as status bar
    if args.b == "true":
        volume = sink(sink_index).current_vol
        max_height,max_width = stdscr.getmaxyx() 

        for i in range(max_width): #First layer "------------"
            stdscr.addch(3,i,'—', curses.A_DIM) 
            stdscr.addch(4,i,'—', curses.A_DIM)

        stdscr.addch(3,0,'▕', curses.A_DIM)
        stdscr.addch(4,0,'▕', curses.A_DIM)
        stdscr.addch(3,max_width-1,'▏', curses.A_DIM)
        stdscr.addch(4,max_width-1,'▏', curses.A_DIM)
        
        bar_width = max_width*volume
        bar_width = int(bar_width)

        if volume >= 1:
            bar_width = max_width-1 # If volume is 100% or higher arrow doesn't go behind '|'

        try:
            for i in range(1,bar_width):
                stdscr.addch(3,i,'▄', curses.A_DIM)
                stdscr.addch(4,i,'▀', curses.A_DIM)
        except (curses.error):
            pass


if __name__ == "__main__":
    main()
    