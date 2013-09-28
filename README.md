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
