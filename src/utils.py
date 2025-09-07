from datetime import datetime

def generate_datetime_str(date=datetime.today()) -> str:
    return date.strftime("%d-%m-%Y")


print(generate_datetime_str())
    