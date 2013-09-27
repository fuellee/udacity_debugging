#!/usr/bin/env python
# Simple debugger
# See instructions around line 34
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
    # print remove_html_markup('xyz')
    print remove_html_markup('"<b>foo</b>"')
    print remove_html_markup("'<b>foo</b>'")

# globals
breakpoints = {14: True}
watchpoints = {'c': True}
commands = []#['b',"p", "s", "p tag", "p foo", "q"]
stepping = False

""" *** INSTRUCTIONS ***

"""
def debug(command, my_locals):
    global stepping
    global breakpoints
    global watchpoints

    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None


    if command.startswith('s'):     # step
        stepping = True
        return True

    elif command.startswith('c'):   # continue
        stepping = False
        return True

    elif command.startswith('p'):   # print <var_name>
        if arg == None: # no arg, print all variables
            print my_locals
        elif arg in my_locals: # has arg, print that variable
            print arg, "=", repr(my_locals[arg])
        else:  # no such variable exists
            print "No such variable:",arg

    elif command.startswith('b'):   # breakpoint <line_no>
        if arg == None: # no arg, print all variables
            print 'You must supply a line number'
        else:
            line_no = int(arg)
            breakpoints[line_no] = True;

    elif command.startswith('w'):   # watch <var_name>
        if arg == None:
            print 'You must supply a variable name'
        elif arg in my_locals:
            watchpoints[arg] = my_locals[arg]
        else:
            print "No such variable:",arg

    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)

    else:
        print "No such command", repr(command)

    return False

def input_command():
    command = raw_input("(my-spyder) ")
    global commands
    # command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or breakpoints.has_key(frame.f_lineno):
            resume = False
            while not resume:

                print event, frame.f_lineno, frame.f_code.co_name, frame.f_locals

                command = input_command()
                resume = debug(command, frame.f_locals)

                # watchpoints
                for varName,varValue in watchpoints.iteritems():
                    if (varName in frame.f_locals) and (frame.f_locals[varName] != varValue):
                        print varName,':',repr(varValue),'=>',repr(frame.f_locals[varName])
                        watchpoints[varName] = frame.f_locals[varName]
    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)

#Simple test
# print watchpoints
# debug("w s", {'s': 'xyz', 'tag': False})
# print watchpoints
#>>> {'c': True}
#>>> {'c': True, 's': True}
