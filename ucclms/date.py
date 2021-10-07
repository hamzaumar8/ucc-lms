from datetime import date, timedelta, datetime
datey = datetime.now()
datey = datey + timedelta(days=7)
datey = datey.strftime("%Y-%m-%d %H:%M:%S")
print(datey)