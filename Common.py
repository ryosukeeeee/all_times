import datetime
import sys

def ts_to_date_object(ts):
  dt_jst_aware = datetime.datetime.fromtimestamp(ts, datetime.timezone(datetime.timedelta(hours=9)))

  return dt_jst_aware

def get_timestamp(year, month, day, hour):
  tz = datetime.timezone(datetime.timedelta(hours=9))
  dt = datetime.datetime(year,month,day,hour,tzinfo=tz)

  return dt

if __name__ == "__main__":
  args = sys.argv

  if len(args) > 1:
    dt = ts_to_date_object(float(args[1]))
    print(dt)
    if dt.hour > 2:
      res = get_timestamp(dt.year, dt.month, dt.day, 2)
    else:
      res = get_timestamp(dt.year, dt.month, dt.day - 1, 2)
    print(res.timestamp())