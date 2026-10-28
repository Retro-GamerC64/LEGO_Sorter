class hardwareInterfaceHandler:
    def __init__(self):
        self.placeholder = 0
        self.binTotals = [0] * 10

    def sortBin(self, binNum):
        print(f"Placed in Bin # {binNum}\n")
        self.binTotals[binNum] = self.binTotals[binNum] + 1

        print("Bins have this many parts in them: " + str(self.binTotals))