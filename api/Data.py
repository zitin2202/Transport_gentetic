class Data:
    def __init__(self,A,B,costs_table,capacity,distance_between_destinations=None):
        self.A = A
        self.B = B
        self.costs_table = costs_table
        self.excessPoint = None
        self.distance_between_destinations = distance_between_destinations
        self.addExcess()
        self.capacity = capacity
        # self.A = [55, 123, 200, 60, 10]
        # self.B = [50, 75, 50, 125, 88, 24]
        #
        # self.costs_table = [
        #     [3, 6, 6, 12, 4, 1],
        #     [5, 14, 4, 20, 5, 25],
        #     [3, 15, 6, 21, 10, 12],
        #     [9, 13, 30, 6, 5, 8],
        #     [4, 25, 8, 10, 7, 4],
        #
        # ]



    def setA(self,new_A):
        self.A = new_A

    def setB(self,new_B):
        self.B = new_B

    def setCosts(self,new_costs):
        self.costs_table = new_costs



    def addExcess(self):
        sumA = sum(self.A)
        sumB = sum(self.B)
        diff = sumA - sumB
        print(diff)
        if diff < 0:
            self.A.append(-diff)
            self.excessPoint = "A"
        if diff > 0:
            self.B.append(diff)
            self.excessPoint = "B"


    def giveWithoutExcess(self):
        copyA = [i for i in self.A]
        copyB = [i for i in self.B]
        if self.excessPoint == "A":
            copyA = copyA[:-1]
        elif self.excessPoint == "B":
            copyB = copyB[:-1]


        return copyA,copyB
