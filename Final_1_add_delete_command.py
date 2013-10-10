#!/usr/bin/env python
# Simple debugger
# See instructions around lines 36

import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out

# main program that runs the buggy program
def main():
    print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")


# globals
breakpoints = {14: True}
watchpoints = {'c': True}
stepping = False

"""
Our debug function
Improve and expand the debug function to accept a new command:
a delete command 'd <type> <argument>', where <type> is either b for breakpoint,
or w for watchpoint. The following argument should be either a number
for the breakpoint or a string for the watchpoint.
If there is mismatch between type and argument, you should print out
"Incorrect command".
In the case of "d b <argument>" you should delete that breakpoint from the
breakpoint dictionary, or print "No such breakpoint defined", repr(argument)
In case of watchpoint, you should delete the watchpoint if such variable exists,
or print: variable, "is not defined as watchpoint"
"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    global watchpoints

    if command.find(' ') > 0:
        args = command.split(' ')
        args.pop(0)
        arg = args[0]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):   # print <var_name>
        if arg is None:  # no arg, print all variables
            print my_locals
        elif arg in my_locals:  # has arg, print that variable
            print arg, "=", repr(my_locals[arg])
        else:  # no such variable exists
            print "No such variable:", arg

    elif command.startswith('b'):   # breakpoint <line_no>
        if arg is None:  # no arg, print all variables
            print 'You must supply a line number'
        else:
            line_no = int(arg)
            breakpoints[line_no] = True

    elif command.startswith('w'):   # watch <var_name>
        if arg is None:
            print 'You must supply a variable name'
        elif arg in my_locals:
            watchpoints[arg] = my_locals[arg]
        else:
            print "No such variable:", arg

    elif command.startswith('d'):    # delete watch/break point
        """
        a delete command 'd <type> <argument>', where <type> is either b for breakpoint,
        or w for watchpoint. The following argument should be either a number
        for the breakpoint or a string for the watchpoint.
        If there is mismatch between type and argument, you should print out
        "Incorrect command".
        In the case of "d b <argument>" you should delete that breakpoint from the
        breakpoint dictionary, or print "No such breakpoint defined", repr(argument)
        In case of watchpoint, you should delete the watchpoint if such variable exists,
        or print: variable, "is not defined as watchpoint"
        """
        # YOUR CODE HERE
        if len(args)>=2:
            type = args[0]
            argument = args[1]

            # print "type:", type
            # print "argument", argument

            if type is "b" and argument.isdigit():
                argument = int(argument)
                if argument in breakpoints:
                    del breakpoints[argument]
                else:
                    print "No such breakpoint defined", repr(argument)
            elif type is "w":
                if argument in watchpoints:
                    del watchpoints[argument]
                else:
                    print argument, "is not defined as watchpoint"
            else:
                print "Incorrect command"
        else:
            print "Incorrect command"

    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)

    return False

commands = ["w out", "d w out", "w out", "b 12", "b", "d b 14", "b", "q"]

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

"""
Our traceit function
"""
def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or frame.f_lineno in breakpoints:
            resume = False
            print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals
            while not resume:
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
#sys.settrace(traceit)
#main()
#sys.settrace(None)

#Simple test
watchpoints = {'s': True}
print watchpoints
debug("d w s", {'s': 'xyz', 'tag': False})
print watchpoints
breakpoints = {8: True, 12: True, 20: True}
print breakpoints
debug("d b 12", {'s': 'xyz', 'tag': False})
print breakpoints
