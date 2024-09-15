from datetime import datetime

def iso_str_date_to_format(isostrdate:str, format='%H:%M %d.%m.%Y'):
    return datetime.fromisoformat(isostrdate).strftime(format)