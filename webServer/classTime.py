import time
import numpy as np
import argparse

import json

# get number of pixels from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nPix", default=20, type=int, help = "Number of LED Pixels.")
args = parser.parse_args()

try:
    from ledPixels import *
    ledPix = ledPixels(args.nPix, board.D18)
except:
    print("ledPix not active")



weeklySchedule = """
[
    {
        "day": "Monday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Tuesday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Wednesday",
        "periods": [
            ["8:15", "9:10"],
            ["9:15", "10:10"],
            ["10:15", "11:10"],
            ["11:15", "11:30"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:25"],
            ["13:30", "15:30"]
        ]
    },
    {
        "day": "Thursday",
        "periods": [
            ["9:15", "9:55"],
            ["10:00", "10:40"],
            ["10:45", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Friday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"]
        ]
    },
    {
        "day": "Saturday",
        "periods": [
            ["8:30", "9:25"],
            ["9:30", "10:25"],
            ["10:30", "11:25"],
            ["11:30", "12:15"],
            ["12:15", "12:40"],
            ["12:45", "13:40"],
            ["13:45", "14:40"],
            ["14:45", "15:30"],
            ["18:30", "19:55"],
            ["20:00", "21:00"]
        ]
    }
]
"""


class uTime:
    def __init__(self, t_str):
        # t_str is a string that has the time as "9:30"
        t = t_str.split(":")
        self.hr = int(t[0])
        self.min = int(t[1])
        self.totMins = self.hr * 60 + self.min

def uTimeNow():
    now = time.localtime()
    return uTime(str(now.tm_hour)+":"+str(now.tm_min))

class period:
    def __init__(self, startTime, endTime):
        self.start = uTime(startTime)
        self.end = uTime(endTime)


class schedule:
    def __init__(self):
        self.days = json.loads(weeklySchedule)
        for i in range(len(self.days)):
            print(i, self.days[i]["day"])
            for t in range(len(self.days[i]["periods"])):
                print(t, self.days[i]["periods"][t])
                strt = self.days[i]["periods"][t][0]
                end = self.days[i]["periods"][t][1]
                self.days[i]["periods"][t] = period(strt, end)

    # def findCurrentPeriod(self):
    #     period = -1
    #     now = time.localtime()
    #     d = now.tm_wday
    #     h = now.tm_hour
    #     m = now.tm_min
    #     tm = uTime(str(h)+":"+str(m))
    #     p = self.days[d][200"periods"]
    #     #print("day", d, h, m, self.days[d]["day"], len(p))
    #     for i in range(len(p)):
    #         #print(h, p[i].start.hr, m, p[i].start.min, p[i].start.totMins)
    #         if (tm.totMins >= p[i].start.totMins and tm.totMins <= p[i].end.totMins):
    #             #print(i, "bingo")
    #             period = i
    #     retime.localtime()turn (d, period)
    #
    # def getCurrentPeriod(self):
    #     (d, p) = self.findCurrentPeriod()
    #     if p == -1:
    #         return NuTimeNow()one
    #     else:
    #         return self.days[d]["periods"][p]

    # def findPeriod(self, t=time.localtime()):
    #     # t is an instance of time.time: eg. time.localtime()
    #     period = -1
    #     d = t.tm_wday
    #     h = t.tm_hour
    #     m = t.tm_min
    #     tm = uTime(str(h)+":"+str(m))
    #     p = self.days[d]["periods"]
    #     #print("day", d, h, m, self.days[d]["day"], len(p))
    #     for i in range(len(p)):
    #         #print(h, p[i].start.hr, m, p[i].start.min, p[i].start.totMins)
    #         if (tm.totMins >= p[i].start.totMins and tm.totMins <= p[i].end.totMins):
    #             #print(i, "bingo")
    #             period = i
    #     return (d, period)
    #
    # def getPeriod(self):
    #     (d, p) = self.findPeriod(time.localtime())
    #     if p == -1:
    #         return None
    #     else:
    #         return self.days[d]["periods"][p]

    def findPeriod2(self, tm = uTimeNow(), d=time.localtime().tm_wday):
        # t is an instance of uTime
        #tm = uTime(str(h)+":"+str(m))
        period = -1
        #print("d:", d, len(self.days))
        p = self.days[d]["periods"]
        #print("day", d, h, m, self.days[d]["day"], len(p))
        for i in range(len(p)):
            #print(h, p[i].start.hr, m, p[i].start.min, p[i].start.totMins)
            if (tm.totMins >= p[i].start.totMins and tm.totMins <= p[i].end.totMins):
                #print(i, "bingo")
                period = i
        return (d, period)

    def getPeriod2(self, tm = uTimeNow(), d=time.localtime().tm_wday):
        (d, p) = self.findPeriod2(tm, d)
        if p == -1:
            return None
        else:
            return self.days[d]["periods"][p]



s = schedule()
print(s.days[0]["periods"][0].start.hr, s.days[0]["periods"][0].start.min)

while True:
    now = time.localtime()
    uNow = uTimeNow()
    cp = s.getPeriod2()
    if cp != None:
        #print(cp.start.hr, cp.start.min)
        frac = (uNow.totMins - cp.start.totMins) / (cp.end.totMins-cp.start.totMins)
        #print("frac:", frac)

        nLights = int(frac*args.nPix)
        try:
            ledPix.twoColors(nLights, (150,0,0), (0,150,0))
        except:
            print("pixels not lit")
    else:
        ledPix.setColor((0,0,100))
    print(f'cp: {cp}, frac: {frac}')
    time.sleep(10)
