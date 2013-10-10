# handles single_quote and double_quote properly
# the solution provide by the udacity course, hmm, tricky
# assert(quote in ["'",'"',False])
# ' and " implicitly means true, thus the quote sign can be stored in varable `quote`

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c=='<' and not quote:
            tag = True
        elif c=='>' and not quote:
            tag = False
        elif (c=='"' or c == "'") and not quote and tag:
            quote = c
        elif c==quote and tag:
            quote = not quote
        elif not tag:
            out = out + c
    assert out.find('<') == -1
    return out

input = """<a href="don't">link</a>
"""
print remove_html_markup(input)
