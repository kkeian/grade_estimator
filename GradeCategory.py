class GradeCategory:
    """A weighted category for this class grades"""
    def __init__(self, name: str, weight: int, currPoints: float, pointsPossible: float):
        self.weight = weight
        self.name = name
        self.pointsPossible = pointsPossible
        self.pointsReceived = currPoints
        self.grade = 0.0
        self.gradeMatrix = [[]for row in range(0, int(pointsPossible)+1)]


    def __deepcopy__(self):
        return GradeCategory(self.name, self.weight, self.pointsReceived, self.pointsPossible)


    def getContrib(self) -> float:
        """Calculate contribution towards final grade"""
        self.calcGrade()
        return self.weight * self.grade


    def updateGrade(self, val: float):
        """Store current grade as percentage"""
        self.grade = val
    

    def getName(self) -> str:
        return self.name

    
    def getWeight(self) -> int:
        return self.weight

    
    def getPointsPossible(self) -> float:
        return self.pointsPossible


    def updatePointsReceived(self, pr: float):
        self.pointsReceived = pr


    def calcGrade(self):
        self.grade = self.pointsReceived / self.pointsPossible


    def getGradePercent(self) -> int:
        return int(self.grade * 100)
    

    def getPointsReceived(self) -> float:
        return float(self.pointsReceived)


    def createPointMatrix(self):
        """Creates a matrix of points received to grade"""
        for p in range(0, int(self.pointsPossible+1)):
            self.updatePointsReceived(p)
            contr = self.getContrib()
            self.gradeMatrix[p] = contr

    def getPossPercentsAdded(self) -> list[float]:
        return [percent for percent in self.gradeMatrix]