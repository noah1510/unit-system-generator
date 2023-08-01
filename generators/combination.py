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
        if unit == self.get('factor1', ''):
            return [self['factor2'], self['product']]

        elif unit == self.get('factor2', ''):
            return [self['factor1'], self['product']]

        elif unit == self.get('product', ''):
            return [self['factor1'], self['factor2']]

        else:
            return []


def load_all_combinations(file: Path) -> List[Combination]:
    if not file.exists():
        raise FileNotFoundError(f'File {file} does not exist')
    if not file.suffix == '.json':
        raise ValueError(f'File {file} is not a json file')

    return [Combination(comb) for comb in json.loads(file.read_text())]


def get_defined_for(unit: str, combinations: List[Combination]) -> List[Combination]:
    return [comb for comb in combinations if comb.uses(unit)]


def get_all_deps_for(unit: str, combinations: List[Combination]) -> List[str]:
    deps = []
    for comb in combinations:
        if comb.uses(unit):
            new_deps = comb.get_deps_for(unit)
            for dep in new_deps:
                if dep == unit:
                    continue
                if dep not in deps:
                    deps.append(dep)

    return deps


def get_multiplication_for(unit: str, combinations: List[Combination]) -> List[Dict]:
    multiplications = []
    for comb in combinations:
        if comb['factor1'] == unit:
            multiplications.append({
                'factor': comb['factor2'],
                'product': comb['product'],
            })
            continue
        if comb['factor2'] == unit:
            multiplications.append({
                'factor': comb['factor1'],
                'product': comb['product'],
            })
    return multiplications


def get_division_for(unit: str, combinations: List[Combination]) -> List[Dict]:
    divisions = []
    for comb in combinations:
        if comb['product'] == unit:
            divisions.append({
                'divisor': comb['factor1'],
                'result': comb['factor2'],
            })

            if comb['factor1'] != comb['factor2']:
                divisions.append({
                    'divisor': comb['factor2'],
                    'result': comb['factor1'],
                })
    return divisions
