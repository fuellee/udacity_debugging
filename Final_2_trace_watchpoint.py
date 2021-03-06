#!/usr/bin/env python
# Simple debugger
# See instructions around line 85
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
    print remove_html_markup('"<b>foo</b>"')

# globals
breakpoints = {10:True, 13:True, 19:True, 21:True}
breakpoints = {}
watchpoints = {"quote": True}
watchpoints_initialized = {}
watch_values = {}
stepping = True

"""
Our debug function
"""
def debug(command, my_locals):
    global stepping
    global breakpoints

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
        # YOUR CODE HERE
        if arg is None:
            print 'You must supply a variable name'
        elif arg in my_locals:
            watchpoints_initialized[arg] = my_locals[arg]
        else:  # not in my_locals, add to watchpoints
            # print "No such variable:", arg
            watchpoints[arg] = True

    elif command.startswith('q'):   # quit
        print "Exiting my-spyder..."
        sys.exit(0)
    else:
        print "No such command", repr(command)

    return False

commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"]

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

"""
Our traceit function
Improve the traceit function to watch for variables in the watchpoint
dictionary and print out (literally like that):
event, frame.f_lineno, frame.f_code.co_name
and then the values of the variables, each in new line, in a format:
somevar ":", "Initialized"), "=>", repr(somevalue)
if the value was not set, and got set in the line, or
somevar ":", repr(old-value), "=>", repr(new-value)
when the value of the variable has changed.
If the value is unchanged, do not print anything.
"""
def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or (frame.f_lineno in breakpoints):
            resume = False
            while not resume:

                command = input_command()
                resume = debug(command, frame.f_locals)

        # watchpoints
        output = ""
        for varName,old_value in watchpoints_initialized.iteritems():
            new_value = frame.f_locals[varName]
            if (varName in frame.f_locals) and (old_value != new_value):
                output += varName+' : '+repr(old_value)+' => '+repr(new_value)+'\n'
                watchpoints_initialized[varName] = new_value
        new_initialized = set()
        for varName in watchpoints:
            if varName in frame.f_locals:  # varName initize
                new_value = frame.f_locals[varName]
                output += varName+' : '+'Initialized'+' => '+repr(new_value)+'\n'
                # move varName to watchpoints_initialized
                new_initialized.add(varName)
                watchpoints_initialized[varName] = new_value
        for varName in new_initialized:
            del watchpoints[varName]

        if output:
            print event, frame.f_lineno, frame.f_code.co_name
            print output,
    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)

# with the commands = ["w c", "c", "c", "w out", "c", "c", "c", "q"],
# the output should look like this (line numbers may be different):
#line 26 main {}
#line 10 remove_html_markup
#quote : Initialized => False
#line 13 remove_html_markup
#c : Initialized => '"'
#line 19 remove_html_markup
#quote : False => True
#line 13 remove_html_markup
#c : '"' => '<'
#line 21 remove_html_markup
#out : '' => '<'
#Exiting my-spyder...
