from datetime import date

def serialize_date(obj):
    if isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")