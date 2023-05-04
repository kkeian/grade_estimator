from copy import deepcopy
from GradeCategory import GradeCategory


class ClassGrade:
    """Represents a class overall grade"""
    def __init__(self, className: str, gradeCats: dict[str]):
        self.className = className
        self.gradeCats = gradeCats
        self.pointsToPass = 0.0

    
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result


    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


    def setCategory(self, catName: str, cat: GradeCategory):
        self.gradeCats[catName] = cat


    def calcGrade(self) -> float:
        """Calculates current overall grade"""
        currGrade = 0
        for _, cat in self.gradeCats.items():
            currGrade += cat.getContrib()
        self.pointsToPass = (70 - currGrade) if currGrade < 70 else 0
        return currGrade

    def getName(self) -> str:
        return self.className

    
    def getCategories(self) -> dict[str]:
        return self.gradeCats

    
    def getPointsToPass(self) -> float:
        return self.pointsToPass