import pytz

def convert_ist_to_timezone(dt_ist, timezone):
    ist = pytz.timezone('Asia/Kolkata')
    local_dt = ist.localize(dt_ist)
    target_tz = pytz.timezone(timezone)
    return local_dt.astimezone(target_tz)