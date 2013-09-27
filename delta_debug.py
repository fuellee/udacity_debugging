import re

test_count = 0

def test(input):
    global test_count
    test_count += 1

    print test_count,input, len(input)
    if re.search("<SELECT[^>]*>", input) >= 0:
        return "FAIL"
    else:
        return "PASS"


def ddmin(input):
    # assert test(input) == "FAIL"

    n = 2     # Initial granularity
    while len(input) >= 2:
        start = 0
        subset_length = len(input) / n
        some_complement_is_failing = False

        while start < len(input):
            complement = input[:start] + input[start + subset_length:]

            if test(complement) == "FAIL":
                input = complement
                n = max(n - 1, 2)
                some_complement_is_failing = True
                break

            start += subset_length

        if not some_complement_is_failing:
            n = min(2*n, len(input))
            if n == len(input):
                break

    return input

# UNCOMMENT TO TEST
html_input = '<SELECT>foo</SELECT>'
print ddmin(html_input)

print "test_count:",test_count
