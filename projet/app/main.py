from fastapi import FastAPI, HTTPException
from models import Mountain_Peak, Mountain_Peak_Pydantic, Mountain_PeakIn_Pydantic, engine
import models
from tortoise.contrib.fastapi import HTTPNotFoundError , register_tortoise
from pydantic import BaseModel
import uvicorn

class Message(BaseModel):
    message : str

models.Base.metadata.create_all(bind=engine)

mountain_peak_app = FastAPI(title="Mountain-Peak-API", version="v1")


@mountain_peak_app.get("/")
async def welcome():
    return {"Wyll" : "M-F-I technical test",
            "To get FatsApi interface : " : "/docs in URL",  
            }

# Create
@mountain_peak_app.post("/insert_peak", response_model=Mountain_Peak_Pydantic)
async def create_peak (peak : Mountain_PeakIn_Pydantic):
    obj = await Mountain_Peak.create(**peak.dict(exclude_unset=True))
    return await Mountain_Peak_Pydantic.from_tortoise_orm(obj)

# Read
@mountain_peak_app.get("/peak/{id}", response_model=Mountain_PeakIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one(id: int):
    return await Mountain_PeakIn_Pydantic.from_queryset_single(Mountain_Peak.get(id= id))

# FIXME NOT WORKING try to read all then filter by longitude and lattitude
# Read all
@mountain_peak_app.get("/peak_all", response_model=Mountain_PeakIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_all_peaks():
    return None

# update
@mountain_peak_app.put("/peak/{id}", response_model=Mountain_Peak_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_peak(id: int, peak: Mountain_PeakIn_Pydantic):
    await Mountain_Peak.filter(id =id).update(**peak.dict(exclude_unset=True))
    return await Mountain_Peak_Pydantic.from_queryset_single(Mountain_Peak.get(id= id))

# delete
@mountain_peak_app.delete("/peak/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_peak(id: int):
    delete_obj = await Mountain_Peak.filter(id= id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail="this peak is not found")
    return Message(message = "Successfully deleted")


register_tortoise(
    mountain_peak_app,
    db_url="sqlite://peaks.db",
    modules={'models' : ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    uvicorn.run(mountain_peak_app, host="127.0.0.1", port=8000 )
