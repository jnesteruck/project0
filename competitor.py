from abc import ABC, abstractmethod


class Competitor(ABC):
    def __init__(self, name, city, state, age, seed=0):
        self._name = str(name)
        self._city = str(city)
        self._state = str(state)
        self._seed = int(seed)
        self._age = int(age)
    
    def setName(self, name):
        self._name = name
    
    def setLocation(self, city, state):
        self._city = str(city)
        self._state = str(state)
    
    def setSeed(self, seed):
        self._seed = int(seed)
    
    def setAge(self,age):
        self._age = int(age)
    
    # getters
    def getName(self):
        return self._name
    
    def getSeed(self):
        return self._seed
    
    @abstractmethod
    def getResult():
        pass

    def __str__(self):
        if self._state == "":
            return "Team: " + self._name + ", Seed: " + str(self._seed) + ", Location: " + self._state
        return "Team: " + self._name + ", Seed: " + str(self._seed) + ", Location: " + self._city + ", " + self._state
    
class Team(Competitor):
    def getResult():
        return None

class IndividualPro(Competitor):
    def getResult():
        return None
    
    def __str__(self):
        if self._state == "":
            return "Team: " + self._name + ", Seed: " + str(self._seed) + ", Age: " + str(self._age) + ", Location: " + self._state
        return "Name: " + self._name + ", Seed: " + str(self._seed) + ", Age: " + str(self._age) + " Location: " + self._city + ", " + self._state

class IndividualCasual(Competitor):
    def getResult():
        return None
    
    def __str__(self):
        return "Name: " + self._name + ", Seed: " + str(self._seed) + ", Age: " + str(self._age)
