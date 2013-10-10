# handles single_quote and double_quote properly

def remove_html_markup(s):
    tag = False
    single_quote = False
    double_quote = False
    out = ""

    for c in s:
        quote = single_quote or double_quote
        # print c,"--quote:",quote,";single_quote:",single_quote,";double_quote:",double_quote,";--tag:",tag
        if c=='<' and not quote:
            tag = True
        elif c=='>' and not quote:
            tag = False
        elif c=="'" and not quote and tag:
            single_quote = True
        elif c=='"' and not quote and tag:
            double_quote = True
        elif c=="'" and single_quote and tag:
            single_quote = False
        elif c=='"' and double_quote and tag:
            double_quote = False
        elif not tag:
            out = out + c
    assert out.find('<') == -1
    return out

input = """<a href="don't">link</a>
"""
print remove_html_markup(input)
