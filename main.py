from typing import Dict




class Transition:
    def __init__(self, tapeDirection, nextState: 'State', writtenChar=None):
        self.tapeDirection = tapeDirection
        if nextState is None and writtenChar is None:
            pass
        if nextState is not None and writtenChar is not None:         
            self.nextState = nextState      
            self.currChar = writtenChar

        
class State:
    def __init__(self, alphabetTransitions: Dict[str,Transition], 
                isStart, isFinal):
        self.alphabetTransitions = alphabetTransitions
        self.isStart = isStart
        self.isFinal = isFinal

class Tape:
    # currPosition = 0
    def __init__(self, currString, isDone=False,currPosition=0) -> None:
        self.currPosition = currPosition
        self.currString = currString
        self.isDone = isDone
    def incrementPosition(self):
        self.currPosition = self.currPosition+1
        if self.currPosition > (len(self.curString)-1):
            self.isDone = True
    def decrementPosition(self):
        self.currPosition = self.currPosition-1
        if self.currPosition < 0:
            self.isDone = True

class Driver:
    currState = State()
    statesDict = {}
    turingTape = Tape()    
    def __init__(self, inputString, statesDict, initialState):
        self.turingTape.currString = inputString
        self.statesDict = statesDict
        self.currState = initialState 
    def processChar(self, currChar):

    # def processString(self):
    #     while(not self.turingTape.isDone):




