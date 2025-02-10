import time

class Debugger:
    def __init__(self):
        self.nodeVisited: int = 0
        self.numOfMups: int = 0
        self.timeBegin = None
        self.timeElapsed = None

    def increment_node_visited(self):
        self.nodeVisited += 1

    def increment_mups(self):
        self.numOfMups += 1
    
    def setTimeBegin(self):
        self.timeBegin = time.time()
    
    def end(self):
        timeEnd = time.time()
        self.timeElapsed = timeEnd - self.timeBegin

    def get_execution_time(self) -> float:
        return self.timeElapsed
        
    def get_node_visited(self) -> int:
        return self.nodeVisited
    
    def get_num_of_mups(self) -> int:
        return self.numOfMups

