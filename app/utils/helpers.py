
def clean_dict(data : dict) -> dict:
    return {key: val for (key, val) in data.items() if val is not None}

