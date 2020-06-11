from random import choice, randint, seed
from os import urandom


################################################################################
#                              RULES BY DEFAULT                                #

class DefaultRules:
    """Include ASCII groups for randint"""

    ASCII_GROUPS = (
        (32, 47),    # [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/']
        (48, 57),    # [0-9]
        (58, 64),    # [':', ';', '<', '=', '>', '?', '@']
        (65, 90),    # [A-Z]
        (91, 96),    # ['[', '\\', ']', '^', '_', '`',]
        (97, 122),   # [a-z]
        (123, 126),  # ['{', '|', '}', '~']
    )
    FIGURES = ASCII_GROUPS[1]
    LOWER_EN = ASCII_GROUPS[5]
    UPPER_EN = ASCII_GROUPS[3]

    @staticmethod
    def from_sequence(sequence: (str, list, tuple)):
        """Return bool function from sequence of characters from list of integers"""
        sequence = list(sequence)

        def closure(password: list) -> bool:
            return "".join(sequence) in PasswordGenerator.to_str(password)

        return closure

#                                                                              #
################################################################################


################################################################################
#                             PASSWORD GENERATOR                               #

class PasswordGenerator:
    ASCII = (32, 126)

    def __init__(self, rules: (tuple, list, set)):
        """Use the rules for each password. If the rules is empty it will not use rules"""
        self.rules = list(rules)
        self.seed_generator = lambda: urandom(32)

    def append_rules(self, rules: (tuple, list, set)):
        """Iterable must content bool callable objects"""
        self.rules.extend(list(rules))

    def check_password(self, password: list) -> bool:
        """Return True if all rules accepted"""
        return all(rule(password) for rule in self.rules)

    def fetch_password(self, length: int, library: (tuple, list, set), use_ascii=True, limit_tries=2 ** 32) -> list:
        """Return password which follow rules. Library must be empty tuple, list or tuple, which contains group of
        two integers: ((start, stop), ...)"""
        if not (use_ascii or library):
            raise ValueError("Cannot generate password without ASCII and library")

        library = list(library)
        if use_ascii:
            library.append(PasswordGenerator.ASCII)

        for _ in range(abs(limit_tries)):
            seed(self.seed_generator())
            password = self.generate_password(length, library)
            if self.check_password(password):
                return password

    @staticmethod
    def generate_password(length: int, library: (tuple, list)):
        """Simple generator from group of two integers: ((start, stop), ...)"""
        return [randint(*choice(library)) for _ in range(length)]

    @staticmethod
    def to_str(password: list) -> str:
        """Convert [int, int...] into \"chr(int)chr(int)...\""""
        return "".join([chr(index) for index in password])

    def remove_rules(self, rules: (tuple, list, set)):
        """Iterable must content bool callable objects"""
        tuple(self.rules.remove(destrule) for destrule in list(self.rules) for rule in rules
              if rule.__code__ == destrule.__code__)  # By some reason these function may have different hashes

#                                                                              #
################################################################################
