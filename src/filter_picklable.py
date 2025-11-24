import pickle

def filter_picklable(d, name="dict"):
    """Return a copy of dict `d` containing only picklable values."""
    safe = {}
    for k, v in d.items():
        try:
            pickle.dumps(v)
            safe[k] = v
        except Exception as e:
            pass
            # print(f"[skip] {name}[{k!r}] (type {type(v)}) not picklable: {e}")
    return safe