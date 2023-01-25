from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Mountain_Peak(models.Model):
    
    id = fields.IntField(pk=True)
    name_attribute = fields.CharField(max_length=250)
    lattitude = fields.FloatField(max=53)
    longitude = fields.FloatField(max=53)
    alltitude_in_meters = fields.IntField(max_length=10)

    class PydanticMeta:
        pass

Mountain_Peak_Pydantic = pydantic_model_creator(Mountain_Peak, name= "MountainPeak")
Mountain_PeakIn_Pydantic = pydantic_model_creator(Mountain_Peak, name= "MountainPeakIn", exclude_readonly=True)

DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/peak_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()