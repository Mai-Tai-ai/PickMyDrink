from core.chatgpt import llm_strict
from core.history import History
from pydantic import BaseModel, Field

monster_options = {
    "original": "original.png",
    "zero ultra": "zero_ultra.png",
    "ultra red": "ultra_red.png",
    "mango loco": "mango_loco.png",
    "pipeline punch": "pipeline_punch.png",
    "pacific punch": "pacific_punch.png",
    "lo-carb": "lo_carb.png",
    "java mean bean": "java_mean_bean.png",
    "khaos": "khaos.png",
    "ultra sunshine": "ultra_sunrise.png"
}

available_drinks = list([drink.capitalize() for drink in monster_options.keys()])


class MonsterEnergyRecommendation(BaseModel):
    drink_name: str = Field(..., description="Recommend a Monster Energy drink from the following list: " + str(available_drinks))
    explanation: str = Field(..., description="Explain why this Monster Energy drink should be recommended at this time to the customer.")


def recommend_monster(weather, exclude=None) -> MonsterEnergyRecommendation:
    if exclude is None:
        exclude = []
    history = History()
    history.user(str(weather))
    if exclude:
        history.user(f"Don't recommend: {', '.join(exclude)}.")
    return llm_strict(history, MonsterEnergyRecommendation)
