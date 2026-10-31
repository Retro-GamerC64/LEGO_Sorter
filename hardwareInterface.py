import threading
import time
class hardwareInterfaceHandler:
    def __init__(self):
        self.placeholder = 0
        self.binTotals = [0] * 12
        self.beltMove = True
        self.lock = threading.Lock()
        self.stopped = False
        self.activeBin =-1
        self.binState = False
        self.movementThread = threading.Thread(
            target=self.runLoop,
            daemon=True,
        )
    def runLoop(self):
        while not self.stopped:
            if not self.beltMove:
                print("Belt Stopped")
            if not self.activeBin == -1:
                print(f"Active bin: {self.activeBin}")
                self.moveArm(self.activeBin)
            time.sleep(0.2)


    def moveArm(self, binNum):
        self.binState = True
        self.beltMove = False
        print('extending arm')
        time.sleep(2)
        self.binState = False
        print('retracting arm')
        self.beltMove = True
        self.activeBin = -1

    def sortBin(self, binNum):
        if binNum == None:
            binNum == 12
        print(f"Placed in Bin # {binNum}\n")
        self.binTotals[binNum] = self.binTotals[binNum] + 1
        self.activeBin = binNum
        print("Bins have this many parts in them: " + str(self.binTotals))

    