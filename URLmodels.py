from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ODL(Base):
    __tablename__ = "odls"

    ID = Column(Integer, primary_key=True)
    Locality_code = Column(String)
    Value = Column(String)
    Start_measure = Column(String)
    End_measure = Column(String)

    def __init__(self, Locality_code, Value, Start_measure, End_measure):
        self.Locality_code = Locality_code
        self.Value = Value
        self.Start_measure  = Start_measure 
        self.End_measure= End_measure
