class Object:
    data:dict
    _immutables:list[str]
    _builtsin:list[str]
    def __init__(_) -> None:
        object.__setattr__(_, "_immutables", [])
        object.__setattr__(_, "_builtins", [])
        object.__setattr__(_, "data", {})

        for key, value in Object.__dict__.items():
            if not key.startswith("__") and key not in _._builtins:
                _.data[key] = value


    def __setattr__(_, name, value):
        if name in _._immutables:
            raise AttributeError(f"Cannot modify {name}.")
        super().__setattr__(name, value)
        _.data.update({name:value})