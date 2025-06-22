from pydantic import Field, BaseModel


def normalize(value: float, min_val: float, max_val: float) -> float:
    """Clamp and normalize a value between 0 and 1."""
    return max(0.0, min((value - min_val) / (max_val - min_val), 1.0))


def inverted_normalize(value: float, min_val: float, max_val: float) -> float:
    """Normalize so lower input values result in higher output (for things like pressure)."""
    return 1.0 - normalize(value, min_val, max_val)


class NormalizedWeatherInfo(BaseModel):
    clouds: float = Field(..., ge=0.0, le=1.0)
    precipitation: float = Field(..., ge=0.0, le=1.0)
    wind: float = Field(..., ge=0.0, le=1.0)
    temperature: float = Field(..., ge=0.0, le=1.0)
    visibility: float = Field(..., ge=0.0, le=1.0)
    humidity: float = Field(..., ge=0.0, le=1.0)
    pressure: float = Field(..., ge=0.0, le=1.0)  # Inverted: lower pressure = higher value
    is_day: int  # 0 or 1 — can be used to trigger night or day ambient loops
    condition: str

class WeatherInfo(BaseModel):
    clouds: float
    precipitation: float
    wind: float
    temperature: float
    condition: str
    is_day: int
    visibility: float
    humidity: float
    pressure: float

    def normalize(self) -> "NormalizedWeatherInfo":
        return NormalizedWeatherInfo(
            clouds=normalize(self.clouds, 0, 100),
            precipitation=normalize(self.precipitation, 0, 20),
            wind=normalize(self.wind, 0, 75),
            temperature=normalize(self.temperature, -30, 40),
            visibility=normalize(self.visibility, 0, 10),
            humidity=normalize(self.humidity, 0, 100),
            pressure=inverted_normalize(self.pressure, 950, 1050),
            is_day=self.is_day,
            condition=self.condition
        )
