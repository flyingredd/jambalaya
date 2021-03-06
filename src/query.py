from handler import Session
from leg import Leg
from datetime import datetime
from datetime import date
from datetime import time
import matplotlib.pyplot as plt
import matplotlib.dates as mpldates

session = Session()

def similar_flights(flight, all_flights):
    return [f for f in all_flights if f.represents_same_leg(flight)]

def make_groups():
    grouped = []
    matched = {leg:False for leg in l}
    for leg in l:
        if matched[leg]:
            continue
        sim = similar_flights(leg, l)
        grouped.append(sim)
        for s in sim:
            matched[s] = True

    for grp in grouped:
        if (len(grp)) > 1:
            multiple = grp
    return grouped

l = session.query(Leg).\
    filter(Leg.departure_location == 'LGW').\
    filter(Leg.arrival_location == 'DUB').\
    filter(Leg.airline == 'Aer Lingus').\
    filter(Leg.request_time >= datetime(2018,1,12,0,0,0)).\
    filter(Leg.request_time < datetime(2018, 1, 13, 0, 0, 0))

same = [leg for leg in l if leg.departure_date.time() == time(19, 15)]

weekdays = [d for d in same if d.departure_date.isoweekday() in range(1,5)]
friday = [d for d in same if d.departure_date.isoweekday() == 5]
weekends = [d for d in same if d.departure_date.isoweekday() in (6,7)]

def prices(lst):
    return ([mpldates.date2num(d.departure_date) for d in lst], [d.price for d in lst])

plt.plot_date(prices(weekdays)[0], prices(weekdays)[1], 'g^', label='$Weekdays$')
plt.plot_date(prices(friday)[0], prices(friday)[1], 'b^', label='$Fridays$')
plt.plot_date(prices(weekends)[0], prices(weekends)[1], 'r^', label='$Weekends$')
plt.ylabel('Price (£)')
plt.xlabel('Departure date')
plt.title('Gatwick to Dublin 7.15pm Flight')
plt.legend()
plt.show()
