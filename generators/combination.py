import json
from pathlib import Path
from typing import Dict, List


class Combination(Dict):
    def __init__(self, data: Dict):
        if data is None:
            raise ValueError('data cannot be None')
        if 'factor1' not in data:
            raise ValueError('data must contain a "factor1" key')
        if 'factor2' not in data:
            raise ValueError('data must contain a "factor2" key')
        if 'product' not in data:
            raise ValueError('data must contain a "product" key')

        super().__init__(data)

    def __str__(self) -> str:
        return f'{self["factor1"]} * {self["factor2"]} = {self["product"]}'

    def __repr__(self) -> str:
        return f'Combination({self["factor1"]}, {self["factor2"]}, {self["product"]})'

    def uses(self, unit: str) -> bool:
        return unit in [self['factor1'], self['factor2'], self['product']]

    def get_deps_for(self, unit: str) -> List[str]:
        match unit:
            case self.get('factor1'):
                return [self['factor2'], self['product']]

            case self.get('factor2'):
                return [self['factor1'], self['product']]

            case self.get('product'):
                return [self['factor1'], self['factor2']]

            case _:
                return []


def load_all_combinations(file: Path) -> List[Combination]:
    if not file.exists():
        raise FileNotFoundError(f'File {file} does not exist')
    if not file.suffix == '.json':
        raise ValueError(f'File {file} is not a json file')

    return [Combination(comb) for comb in json.loads(file.read_text())]


def get_defined_for(unit: str, combinations: List[Combination]) -> List[Combination]:
    return [comb for comb in combinations if comb.uses(unit)]
