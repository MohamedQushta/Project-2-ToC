from typing import Dict




class Transition:
    def __init__(self, tapeDirection, nextState, writtenChar):
        # self.tapeDirection = tapeDirection
        # if nextState is None and writtenChar is None:
        #     pass
        # if nextState is not None and writtenChar is not None:         
        #     self.nextState = nextState      
        #     self.currChar = writtenChar
        self.tapeDirection = tapeDirection
        self.nextState = nextState
        self.writtenChar = writtenChar

        
class State:
    def __init__(self, alphabetTransitions: Dict[str,Transition], 
                isStart, isAccepting):
        self.alphabetTransitions = alphabetTransitions
        self.isStart = isStart
        self.isAccepting = isAccepting

class Tape:
    def __init__(self, currString, isDone=False,currPosition=0) -> None:
        self.currPosition = currPosition
        self.currString = currString
        self.isDone = isDone
    def incrementPosition(self):
        self.currPosition = self.currPosition+1
        if self.currPosition > (len(self.currString)-1):
            self.isDone = True
    def decrementPosition(self):
        self.currPosition = self.currPosition-1
        if self.currPosition < 0:
            self.isDone = True

class Driver:
    # currState = State()
    statesDict = {}
    turingTape = Tape([])    
    def __init__(self, inputString, statesDict, initialState):
        self.turingTape.currString = inputString
        self.statesDict = statesDict
        self.currState = initialState 
    def processString(self):
        while(not self.turingTape.isDone):
            letterToBeChecked = self.turingTape.currString[self.turingTape.currPosition]
            currStateNextTransition = self.currState.alphabetTransitions[letterToBeChecked]
            updatedChar = self.currState.alphabetTransitions[letterToBeChecked].writtenChar
            currentTapePosition = self.turingTape.currPosition

            if currStateNextTransition.tapeDirection == 'R':
                self.turingTape.currString[currentTapePosition] = updatedChar
                self.turingTape.incrementPosition()
                self.currState = self.statesDict[self.currState.alphabetTransitions[letterToBeChecked].nextState]
            elif currStateNextTransition.tapeDirection == 'L':
                self.turingTape.currString[currentTapePosition] = updatedChar
                self.turingTape.decrementPosition()
                self.currState = self.statesDict[self.currState.alphabetTransitions[letterToBeChecked].nextState]
        if self.currState.isAccepting == True:
            print("this string is accepted")
        else:
            print("this string is not accepted")
            

q0 = State({'1':Transition('R', 'q0','1'), 
            ' ':Transition('R', 'q1',' ')}, True,False)
q1 = State({},False,True)

driver = Driver(['1','1','1','1', ' '], 
                {'q0': q0, 'q1':q1}, q0)

driver.processString()


