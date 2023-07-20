class Prefix:
    def __init__(self):
        self.prefix = ''

    @staticmethod
    def from_string(data: str) -> (float, str):
        if '^' in data:
            name, exponent = data.split('^')
        else:
            name = data
            exponent = 1

        try:
            exponent = int(exponent)
            amount, prefix = Prefix.direct_prefix_string(name)
        except ValueError:
            raise ValueError('Invalid prefix string: ' + data)

        return amount ** exponent, prefix

    @staticmethod
    def direct_prefix_string(raw_str: str) -> (float, str):
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
    def quetta() -> (float, str):
        return 1e30, 'Q'

    @staticmethod
    def ronna() -> (float, str):
        return 1e27, 'R'

    @staticmethod
    def yotta() -> (float, str):
        return 1e24, 'Y'

    @staticmethod
    def zetta() -> (float, str):
        return 1e21, 'Z'

    @staticmethod
    def exa() -> (float, str):
        return 1e18, 'E'

    @staticmethod
    def peta() -> (float, str):
        return 1e15, 'P'

    @staticmethod
    def tera() -> (float, str):
        return 1e12, 'T'

    @staticmethod
    def giga() -> (float, str):
        return 1e9, 'G'

    @staticmethod
    def mega() -> (float, str):
        return 1e6, 'M'

    @staticmethod
    def kilo() -> (float, str):
        return 1e3, 'k'

    @staticmethod
    def hecto() -> (float, str):
        return 1e2, 'h'

    @staticmethod
    def deca() -> (float, str):
        return 1e1, 'da'
    @staticmethod
    def deci() -> (float, str):
        return 1e-1, 'd'

    @staticmethod
    def centi() -> (float, str):
        return 1e-2, 'c'

    @staticmethod
    def milli() -> (float, str):
        return 1e-3, 'm'

    @staticmethod
    def micro() -> (float, str):
        return 1e-6, 'u'

    @staticmethod
    def nano() -> (float, str):
        return 1e-9, 'n'

    @staticmethod
    def pico() -> (float, str):
        return 1e-12, 'p'

    @staticmethod
    def femto() -> (float, str):
        return 1e-15, 'f'

    @staticmethod
    def atto() -> (float, str):
        return 1e-18, 'a'

    @staticmethod
    def zepto() -> (float, str):
        return 1e-21, 'z'

    @staticmethod
    def yocto() -> (float, str):
        return 1e-24, 'y'

    @staticmethod
    def ronto() -> (float, str):
        return 1e-27, 'r'

    @staticmethod
    def quecto() -> (float, str):
        return 1e-30, 'q'
