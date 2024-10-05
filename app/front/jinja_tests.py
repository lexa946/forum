

def include_extension(filename:str, extensions:list[str]):
    extension = filename.split('.')[-1].lower()
    if extension in extensions:
        return True
    return False