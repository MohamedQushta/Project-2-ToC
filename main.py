from typing import Dict




class Transition:
    def __init__(self, tapeDirection, nextState: 'State', currChar=None):
        self.tapeDirection = tapeDirection
        if nextState is None and currChar is None:
            pass
        if nextState is not None and currChar is not None:         
            self.nextState = nextState      
            self.currChar = currChar

        
class State:
    def __init__(self, alphabetTransitions: Dict[str,Transition], 
                isStart, isFinal):
        self.alphabetTransitions = alphabetTransitions
        self.isStart = isStart
        self.isFinal = isFinal

class Tape:
    def __init__(self, currPosition , currString) -> None:
        self.currPosition = currPosition
        self.currString = currString
        
inputString = input("Enter the input string: ") 
TuringTape = Tape(0,inputString)


for i in range(len(TuringTape.currString)):
    print(TuringTape.currString[i])
