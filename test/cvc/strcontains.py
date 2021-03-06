from symbolic.args import symbolic


@symbolic(s="foo")
def strcontains(s):
    if "bar" in s:
        return 0
    elif "x" not in s:
        return 2
    else:
        return 1


def expected_result_set():
    return {0, 1, 2}
