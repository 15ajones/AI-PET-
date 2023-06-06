#week long calendar
def convertDateStringToInt(stringTime): #"0145" -> 105
    hours = int(stringTime[0:2])
    minutes = int(stringTime[2:])
    return hours*60 + minutes

def convertDateIntToString(intTime): #105 -> "1045"
    hours = 0
    minutes = 0
    while intTime >= 60:
        hours+=1
        intTime -= 60

    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    
    if intTime < 10:
        minutes = "0" + str(intTime)
    else:
        minutes = str(intTime)
    return hours + minutes

class Event:
    def __init__(self, name, startTime, endTime):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime

    def getName(self):
        return self.name
    
    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime
    
    def changeStartTime(self, newStartTime):
        self.startTime = newStartTime

    def changeEndTime(self, newEndTime):
        self.endTime = newEndTime
    

         
class Day:
    def __init__(self, dayOfWeek):
        self.dayOfWeek = dayOfWeek
        self.events = []

    def addEvent(self, newEvent):#either returns 0 meaning it happened successfully, or returns an event, which is the event which overlaps
        eventTimings = []
        for event in self.events:
            eventTimings.append([event.getStartTime(), event.getEndTime()])
        #checking if an event is already there 
        for i, eventTiming in enumerate(eventTimings):
            if (newEvent.getStartTime() > eventTiming[0] and newEvent.getStartTime() < eventTiming[1]) or (newEvent.getEndTime() > eventTiming[0] and newEvent.getEndTime() < eventTiming[1]):
                return self.events[i]

        for i in range(len(self.events)):
            if newEvent.getEndTime() <= self.events[i].getStartTime():
                self.events.insert(i, newEvent)
                return 0
            
        self.events.append(newEvent)
        return 0

    def removeEventName(self, name):#removes event. returns 0 if successful, -1 if not successful
        for i, event in enumerate(self.events):
            if event.getName() == name:
                self.events.pop(i)
                return 0
        return -1

    def removeEventStartTime(self, startTime):#removes an event based on its start time
        for i, event in enumerate(self.events):
            if event.getStartTime() == startTime:
                self.events.pop(i)
                return 0
        return -1

    def removeAllEvents(self):
        self.events = []
    
    def printEvents(self): #FOR TESTING
        eventsPrint = []
        for event in self.events:
            eventsPrint.append([event.name, event.startTime, event.endTime])
        print(eventsPrint)
    
class Calendar:

    def __init__(self, currentDayIndex):
        self.days = [Day("Monday"),Day("Tuesday"),Day("Wednesday"),Day("Thursday"),Day("Friday"),Day("Saturday"),Day("Sunday")]
        self.currentDayIndex = currentDayIndex

    def changeDay(self):
        self.days[self.currentDayIndex].removeAllEvents()
        self.currentDayIndex = (self.currentDayIndex + 1) % 7

    def checkUpcomingAppointments(self, time):
        currentDay = self.days[self.currentDayIndex]
        

def __main__():
    day = Day("Monday")
    eventA = Event("a", 100, 200)
    eventB = Event("b", 200, 300) 
    eventC = Event("c", 50, 80)
    eventD = Event("D", 90, 110)
    day.addEvent(eventA)
    day.printEvents()
    day.addEvent(eventB)
    day.printEvents()
    day.addEvent(eventC)
    day.printEvents()
    day.addEvent(eventD)
    day.printEvents()
    day.removeEventName("a")
    day.printEvents()
    day.removeEventStartTime(200)
    day.printEvents()
  

def test():
    print(convertDateIntToString(105))


    return


test()