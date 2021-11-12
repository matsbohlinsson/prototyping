from dataclasses import dataclass


@dataclass
class Food:
    name: str
    unit_price: float
    stock: int = 0

    def stock_value(self) -> float:
        return self.stock * self.unit_price


f = Food(unit_price=12)