from numpy import *
from re import *

# raw data 파일을 읽어들여 Matrix 결과값으로 return해주는 함수
def rawToMatrix(filePath):
    f = open(filePath,'r')
    for line in f:
        extractRelevantData(line)
    f.close()
    return 0


# file을 읽어들인 정보를 적정한 객체에 저장해주는 함수
def extractRelevantData(rawData):
    parseFileLine(rawData)
    # 결과값을 받아서 객체에 저장하는 코드
    return 0

# 정규표현식을 활용해서 parsing해주는 해서 필요한 정보를 return해주는 함수
def parseFileLine(rawData):
    return 0


# Matrix에 관련 정보를 추가하는 함수
def addDataToMatrx(matrix,data):
    # return matrix.append(matrix,np.)
    return 0

# 새로운 Matrix를 만드는 함수
def createNewMatrix(rowNum,colNum):
    return np.empty([rowNum,colNum],dtype=float)
