def segment_html(html):
    """html is a string"""
    quote = False
    tag = False
    seg = ""
    result = []

    for c in html:
        if not quote and not tag:
            if c == '<':
                if seg != "":
                    result.append(seg)

                    # print "#|1|#",seg

                seg = ""
                tag = True
            else:
                seg += c
        if not quote and tag:

            # print "#|3|#",seg

            if c == '>':
                result.append(seg+'>')

                # print "#|2|#",seg+'>'

                seg = ""
                tag = False
            elif c=='"' or c=="'":
                seg += c ##
                quote = True
            else:
                seg += c
                assert seg[0]==('<')
        if quote and tag:
            assert seg[0]==('<')
            if c=='"' or c=="'":
                seg += c
                quote = False
            else:
                seg += c

    return result

input = '<vbox><listbox rows="2">aaaaaa<listitem label="listitem"/><listitem><html:input type="checkbox" style="margin:0px;"/></listitem></listbox></vbox>'
print "____________input_____________"
print input
print "______________________________"
print segment_html(input)
