import datetime
tz_utc_7 = datetime.timezone(datetime.timedelta(hours=7))
timestamp = lambda : datetime.datetime.now(tz_utc_7)  # Adjusted for UTC+7 timezone