from random import randint, seed
from os import urandom

###############################################
#              RULES BY DEFAULT               #

class DefaultRules:
    """Rules by default"""
    
    @classmethod
    def boolOrdSpecSymbolFirstGroup(cls, char):
        """[' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/']"""
        return 31 < char < 48

    @classmethod
    def boolOrdDigit(cls, char):
        """[0-9]"""
        return 47 < char < 58

    @classmethod
    def boolOrdSpecSymbolSecondGroup(cls, char):
        """[':', ';', '<', '=', '>', '?', '@']"""
        return 57 < char < 65

    @classmethod
    def boolOrdUpper(cls, char):
        """[A-Z]"""
        return 64 < char < 91

    @classmethod
    def boolOrdSpecSymbolThirdGroup(cls, char):
        """['[', '\\', ']', '^', '_', '`',]"""
        return 90 < char < 97

    @classmethod
    def boolOrdLower(cls, char):
        """[a-z]"""
        return 96 < char <123

    @classmethod
    def boolOrdSpecSymbolFourthGroup(cls, char):
        """['{', '|', '}', '~']"""
        return 122 < char < 127

    @classmethod
    def fecthDefaultRules(cls):
        return [DefaultRules.boolOrdUpper, DefaultRules.boolOrdLower, DefaultRules.boolOrdDigit,
                DefaultRules.boolOrdSpecSymbolFirstGroup, DefaultRules.boolOrdSpecSymbolSecondGroup,
                DefaultRules.boolOrdSpecSymbolThirdGroup, DefaultRules.boolOrdSpecSymbolFourthGroup]

#                                             #
###############################################


###############################################
#             PASSWORD GENERATOR              #

class PasswordGenerator:
    """Return PasswordGenerator object"""
    def __init__(self, rules: (tuple, list, set)):
        """If rules is [] It is use rules by default. Rules must be iterable, example:  (boolOrdFunctionChar, ...)"""
        self.ASCII = (32, 126)
        self.rules = list(rules) or DefaultRules.fecthDefaultRules()
        self.seed_generator = lambda: urandom(32)

    def checkPassword(self, password: list):
        """Return True if all rule is accept"""
        for rule in self.rules:
            for char in password:
                if rule(char):
                    break
            else:
                return False
        return True

    def fetchPassword(self, lenth: int, library: (tuple, list, set), use_ascii=True, limit_tries=2**32):
        """Return password which follow rules. Library must be empty tuple, list or be tuple, list which contain group of two integers: ((start, stop), ...)"""
        if (not use_ascii) and (not library):
            raise ValueError("PasswwordGenerator cannot fetch without ASCII and library")

        library = list(library)
        if use_ascii:
            library.append(self.ASCII)

        for _ in range(abs(limit_tries)):
            seed(self.seed_generator())
            password = self.generatePassword(lenth, library)
            if self.checkPassword(password):
                return password

    def generatePassword(self, lenth: int, library: (tuple, list)):
        """Simple generator from group of two integers: ((start, stop), ...)"""
        password = []

        for _ in range(lenth):
            start, stop = library[randint(0, (len(library) - 1))]
            char = randint(start, stop)
            password.append(char)

        return password

    def prettyPrint(self, password):
        """Convert [int, int...] into \"chr(int)chr(int)...\""""
        return "".join([chr(index) for index in password])

    def appendRules(self, rules: (tuple, list, set)):
        """Iterable must content bool functions: (boolOrdFunctionChar, ...)"""
        self.rules.extend(list(rules))

    def removeRules(self, rules: (tuple, list, set)):
        """Iterable must content bool functions: (boolOrdFunctionChar, ...)"""
        for rule in rules:
            if rule in self.rules:
                self.rules.remove(rule)

#                                             #
###############################################


###############################################
#         CUSTOM CHARACTERS SEQUENCE          #

class CustomCharactersSequence:
    def __init__(self, sequence: str):
        """Example of rule which require sequence in password. You can imagine yours custom rule in such style"""
        self.sequence = tuple(ord(char) for char in sequence)
        self.iterator = iter(sequence)
        self.match = False

    def __call__(self, char):
        try:
            next_char = next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.sequence)
            if self.match:
                self.match = False
                return True

        if self.match and (not (next_char == char)):
                self.iterator = iter(self.sequence)
                self.match = False
                self.__call__(char)

        elif (not self.match):
            if (next_char == char):
                self.match = True
            else:
                self.iterator = iter(self.sequence)

#                                             #
###############################################
