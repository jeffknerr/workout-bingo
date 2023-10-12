"""
workout done/not done class

J. Knerr
Fall 2023
"""

class Workout(object):
    """workout object"""

    def __init__(self, i, j, workout, done):
        """create a workout object"""

        # x,y coordinates of workout on bingo card
        self.i = i
        self.j = j
        # workout number or "FREE"
        self.workout = workout
        # done if 1, not done yet if 0
        self.done = done

    def __repr__(self):
        """every class needs a repr"""
        return "%s(%s,%s,%s,%s)" % (self.__class__.__name__, 
                str(self.i), str(self.j), str(self.workout), str(self.done))

    def isDone(self):
        """return True if workout done already"""
        return self.done == 1
    def notDone(self):
        """return True if workout not done"""
        return self.done == 0
    def setDone(self):
        """set done = 1"""
        self.done = 1
    def setNotDone(self):
        """set done = 0"""
        self.done = 0

    def geti(self): return self.i
    def getj(self): return self.j
    def getx(self): return self.i
    def gety(self): return self.j
    def getWorkout(self): return self.workout
    def getDone(self): return self.done

def main():
    i = 0
    j = 0
    workout = 3
    w1 = Workout(i, j, workout, 0)
    print(w1)
    assert w1.isDone() == False
    assert w1.notDone() == True
    w1.setDone()
    assert w1.notDone() == False
    assert w1.isDone() == True
    assert w1.geti() == i
    assert w1.getx() == j
    assert w1.gety() == i
    assert w1.getWorkout() == workout
    assert w1.getj() == j
    assert w1.getDone() == 1
    w2 = Workout(2, 2, "Free", 1)
    print(w2)


if __name__ == "__main__":
    main()
