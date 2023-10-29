def pascal_case_to_snake_case(name):
    result = ""
    for i, c in enumerate(name):
        if (
            i > 0
            and c.isupper()
            and ((i + 1 < len(name) and not name[i + 1].isupper()) or name[i - 1].islower())
        ):
            result += "_"
        result += c.lower()
    return result


def snake_case_to_pascal_case(name):
    result = ""
    uppercase_next = True
    for c in name:
        if c == "_":
            uppercase_next = True
            continue
        if uppercase_next:
            c = c.upper()
            uppercase_next = False
        else:
            c = c.lower()
        result += c
    return result
