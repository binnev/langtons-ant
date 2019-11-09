def create_rules(string):
    rules = dict()
    for ruleNo, char in enumerate(string):
        rule = dict(nextColour=(ruleNo+1) % len(string),
                    turnDirection=(1 if char == "r" else -1))
        rules[ruleNo] = rule
    return rules


def nonlinear_range(start, stop, m=10, spacing=1, multiplier=2):
    # base case -- will the remaining numbers fit into the current range
    if stop <= m:
        return list(range(start, stop, spacing))

    # recursive case -- split off the bottom numbers and recurse
    else:
        first = nonlinear_range(start, m, m, spacing)
        last = nonlinear_range(m, stop, int(m*multiplier),
                              int(spacing*multiplier))
        return first + last
