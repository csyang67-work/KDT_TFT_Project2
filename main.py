from datetime import datetime

from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from database import create_tables
from node.plant_node import plant_graph
from services.plant_game_service import (
    change_plant_environment,
    get_plant_status,
    register_plant,
    set_game_time,
    water_plant_for_user,
)


create_tables()
app = FastAPI()


class PlantCreate(BaseModel):
    user_id: str
    plant_name: str


class ChatRequest(BaseModel):
    user_id: str
    message: str


class WaterRequest(BaseModel):
    user_id: str
    amount: int


class EnvironmentRequest(BaseModel):
    user_id: str
    temperature: float
    humidity: float
    light_level: float


class GameTimeRequest(BaseModel):
    user_id: str
    game_time: str


@app.post("/plants")
def create_plant(request: PlantCreate):
    return register_plant(request.user_id, request.plant_name)


@app.get("/plants/{plant_id}")
def read_plant(plant_id: str, user_id: str):
    try:
        return get_plant_status(user_id, plant_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.post("/plants/{plant_id}/water")
def water_plant(plant_id: str, request: WaterRequest):
    try:
        return water_plant_for_user(
            request.user_id,
            plant_id,
            request.amount,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put("/plants/{plant_id}/environment")
def update_environment(
    plant_id: str,
    request: EnvironmentRequest,
):
    try:
        return change_plant_environment(
            request.user_id,
            plant_id,
            request.temperature,
            request.humidity,
            request.light_level,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.put("/plants/{plant_id}/game-time")
def update_game_time(
    plant_id: str,
    request: GameTimeRequest,
):
    try:
        game_time = datetime.fromisoformat(request.game_time)
        return set_game_time(
            request.user_id,
            plant_id,
            game_time,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/plants/{plant_id}/chat")
def chat_with_plant(
    plant_id: str,
    request: ChatRequest,
):
    try:
        plant = get_plant_status(request.user_id, plant_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

    graph_input = {
        **plant,
        "plant_context": "",
        "documents": [],
        "question": request.message,
        "generation": "",
        "messages": [HumanMessage(content=request.message)],
    }

    result = plant_graph.invoke(graph_input)

    return {
        "answer": result["generation"],
        "plant": get_plant_status(request.user_id, plant_id),
    }