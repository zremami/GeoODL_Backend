# This class is created to convert the sent attributes to json format
import json

class predictionDTO(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __init__(self, localityCode="",meanPredictValue=0,stdPredictValue=0 ,localityName="", result=[], truePoints=[], falsePoints=[], message=""):
        self.localityCode=localityCode
        self.localityName=localityName
        self.stdRealValue = stdPredictValue
        self.meanRealValue = meanPredictValue
        self.result=result
        self.truePoints=truePoints
        self.falsePoints=falsePoints
        self.message=message
        

