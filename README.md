Udacity CS259 Software Debugging
================================

code for udacity course CS259 Software Debugging

Files
-----

* 3_optimize_simplification.py
* 3_simplify_input.py
* 4_remove_html_markup.py
* 4_remove_html_markup_tricky.py
* delta_debug.py
* fuzzer.py
* html_segment.py
* my_daikon_opt_improvements.py
* my_daikon.py
* my_spyder.py
* mysteryTest.py

Unit 4
------
`4_remove_html_markup.py` :fixed the quote bug and handles single_quote and double_quote properly

`4_remove_html_markup_tricky.py` 
* the solution provide by the udacity course, hmm, tricky
* assert(quote in ["'",'"',False])
* ' and " implicitly means true, thus the quote(" or ') sign can be stored in varable `quote`

`4_save_the_state.py`
stop and save the current state (frame.f_locals) to a global var('the_state') if some condition is satistied

`4_change_the_state.py`
stop and change the current state (frame.f_locals) according to a global var('the_diff') if some condition is satistied
Changing `frame.f_locals` is some kind of tricky, use `update`.

`4_make_it_work` : **find the cause chain automatically** 
* need a **pass case** and a **fail case**.
* use `get_state` to get their state in given line/iteration. compute the `diff`::`[(varName,fail_val)]`. failure cause must be a subset of diff.
* use `ddmin`(delta debug minimize) to find the minimum set of vars,vals pair make the test fail, for each given line/iteration.
* print the `var,fail_val` pairs in order of line/iteration. that is the cause chain
