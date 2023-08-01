class Prefix:
    def __init__(self, short: str, long: str, amount: float):
        self.__short = short
        self.__long = long
        self.__amount = amount

    def __str__(self) -> str:
        return self.__long

    def __float__(self):
        return self.__amount

    def __repr__(self) -> str:
        return f'Prefix({self.__short}, {self.__long}, {self.__amount})'

    def value(self) -> float:
        return self.__amount

    def short(self) -> str:
        return self.__short

    def long(self) -> str:
        return self.__long

    @staticmethod
    def from_string(data: str) -> 'Prefix':
        if '^' in data:
            name, exponent = data.split('^')
        else:
            name = data
            exponent = 1

        try:
            exponent = int(exponent)
            prefix = Prefix.direct_prefix_string(name)
        except ValueError:
            raise ValueError('Invalid prefix string: ' + data)

        return Prefix(prefix.short(), prefix.long()+f'^{exponent}', prefix.value() ** exponent)

    @staticmethod
    def direct_prefix_string(raw_str: str) -> 'Prefix':
        if raw_str == 'quetta':
            return Prefix.quetta()
        elif raw_str == 'ronna':
            return Prefix.ronna()
        elif raw_str == 'yotta':
            return Prefix.yotta()
        elif raw_str == 'zetta':
            return Prefix.zetta()
        elif raw_str == 'exa':
            return Prefix.exa()
        elif raw_str == 'peta':
            return Prefix.peta()
        elif raw_str == 'tera':
            return Prefix.tera()
        elif raw_str == 'giga':
            return Prefix.giga()
        elif raw_str == 'mega':
            return Prefix.mega()
        elif raw_str == 'kilo':
            return Prefix.kilo()
        elif raw_str == 'hecto':
            return Prefix.hecto()
        elif raw_str == 'deca':
            return Prefix.deca()
        elif raw_str == 'deci':
            return Prefix.deci()
        elif raw_str == 'centi':
            return Prefix.centi()
        elif raw_str == 'milli':
            return Prefix.milli()
        elif raw_str == 'micro':
            return Prefix.micro()
        elif raw_str == 'nano':
            return Prefix.nano()
        elif raw_str == 'pico':
            return Prefix.pico()
        elif raw_str == 'femto':
            return Prefix.femto()
        elif raw_str == 'atto':
            return Prefix.atto()
        elif raw_str == 'zepto':
            return Prefix.zepto()
        elif raw_str == 'yocto':
            return Prefix.yocto()
        elif raw_str == 'ronto':
            return Prefix.ronto()
        elif raw_str == 'quecto':
            return Prefix.quecto()
        else:
            raise ValueError('Invalid prefix string: ' + raw_str)

    @staticmethod
    def quetta() -> 'Prefix':
        return Prefix('Q', 'quetta', 1e30)

    @staticmethod
    def ronna() -> 'Prefix':
        return Prefix('R', 'ronna', 1e27)

    @staticmethod
    def yotta() -> 'Prefix':
        return Prefix('Y', 'yotta', 1e24)

    @staticmethod
    def zetta() -> 'Prefix':
        return Prefix('Z', 'zetta', 1e21)

    @staticmethod
    def exa() -> 'Prefix':
        return Prefix('E', 'exa', 1e18)

    @staticmethod
    def peta() -> 'Prefix':
        return Prefix('P', 'peta', 1e15)

    @staticmethod
    def tera() -> 'Prefix':
        return Prefix('T', 'tera', 1e12)

    @staticmethod
    def giga() -> 'Prefix':
        return Prefix('G', 'giga', 1e9)

    @staticmethod
    def mega() -> 'Prefix':
        return Prefix('M', 'mega', 1e6)

    @staticmethod
    def kilo() -> 'Prefix':
        return Prefix('k', 'kilo', 1e3)

    @staticmethod
    def hecto() -> 'Prefix':
        return Prefix('h', 'hecto', 1e2)

    @staticmethod
    def deca() -> 'Prefix':
        return Prefix('da', 'deca', 1e1)

    @staticmethod
    def deci() -> 'Prefix':
        return Prefix('d', 'deci', 1e-1)

    @staticmethod
    def centi() -> 'Prefix':
        return Prefix('c', 'centi', 1e-2)

    @staticmethod
    def milli() -> 'Prefix':
        return Prefix('m', 'milli', 1e-3)

    @staticmethod
    def micro() -> 'Prefix':
        return Prefix('u', 'micro', 1e-6)

    @staticmethod
    def nano() -> 'Prefix':
        return Prefix('n', 'nano', 1e-9)

    @staticmethod
    def pico() -> 'Prefix':
        return Prefix('p', 'pico', 1e-12)

    @staticmethod
    def femto() -> 'Prefix':
        return Prefix('f', 'femto', 1e-15)

    @staticmethod
    def atto() -> 'Prefix':
        return Prefix('a', 'atto', 1e-18)

    @staticmethod
    def zepto() -> 'Prefix':
        return Prefix('z', 'zepto', 1e-21)

    @staticmethod
    def yocto() -> 'Prefix':
        return Prefix('y', 'yocto', 1e-24)

    @staticmethod
    def ronto() -> 'Prefix':
        return Prefix('r', 'ronto', 1e-27)

    @staticmethod
    def quecto() -> 'Prefix':
        return Prefix('q', 'quecto', 1e-30)
