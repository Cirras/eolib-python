def try_parse_int(value):
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None
