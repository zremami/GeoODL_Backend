import json

class predictionDTO(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __init__(self, localityCode="",meanRealValue=0,stdRealValue=0, mape=0, meanAbsoluteError=0 ,localityName="", result=[], goodPoints=[], badPoints=[], message=""):
        self.localityCode=localityCode
        self.localityName=localityName
        self.stdRealValue = stdRealValue
        self.meanRealValue = meanRealValue
        self.mape = mape
        self.meanAbsoluteError = meanAbsoluteError
        self.result=result
        self.goodPoints=goodPoints
        self.badPoints=badPoints
        self.message=message
        

