# Password Generator (Python 3)
Module for simple password generation with custom rules.

## Password Generator
### Initialization
PasswordGenerator await for list of rules. Rules must await `ord(char)` and return boolean value.
This is some of ways to make generator.
```
# Ways to make generator with rules by default
generator = PasswordGenerator(()) # Initialized with empty types which supports transition into list
generator = PasswordGenerator([])
generator = PasswordGenerator(dict()) # Only keys
generator = PasswordGenerator(set())
generator = PasswordGenerator(frozenset())

generator = PasswordGenerator((boolFirstRule, boolSecondRule, ...)) # Rewrite rules by default
```

### `appendRules` and `removeRules`
Be careful with append wrong function! If function would not return true value, generator try to make another password. And futher before 2**32 times to tries by default.
```
# Some types which supports transition into list
generator.appendRules((boolFirstRule, boolSecondRule, ...))

# Any types with iteration support
generator.removedRules((boolFirstRule, boolSecondRule, ...))
```

### `generatePassword`
Function is build list of chars which located between `[start; stop]` of randrom group of library. Generate password without used rules and `random.seed()`. Seed is used in `fetchPassword`.
```
library = [(start1, stop1), (start2, stop2), ...] # Looks like a dict items
generator.generatePassword(lenth, library)
```

Library is groups in interval from `[start ...` to `... stop]`, include side's points; `random.randint` used for choice random group and char between points. If you want ASCII library (without codes like `\x00` ), you should use `generator.ASCII` into `library`.

### Seed generator
If you gonna change pseudo random number generator (like the `self.seed_generator` by default), you can do some things like this.
```
generator.seed_generator = func # Where func is something like time.time_ns%10**10
```

## DefaultRules
Default rules is required for creating the most strongly password. You can do not use rules, or add yours rules.

- `fetchDefaultRules()` - simple way to fetch all rules (you can remove some rules by your wish)

- `boolOrdSpecSymbolFirstGroup(char: int) -> bool`  `[' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/']` - symbols from 32 to 47 position

- `boolOrdDigit(char: int) -> bool` - digits from 48 to 57 position

- `boolOrdSpecSymbolSecondGroup(char: int) -> bool`  `[':', ';', '<', '=', '>', '?', '@']` - symbols from 58 to 64 position

- `boolOrdUpper(char: int) -> bool` - symbols A-Z from 65 to 90 position

- `boolOrdSpecSymbolThirdGroup(char: int) -> bool`  `['[', '\', ']', '^', '_', '``',]` - symbols from 91 to 96 position

- `boolOrdLower(char: int) -> bool` - symbols a-z from 97 to 122 position

- `boolOrdSpecSymbolFourthGroup(char: int) -> bool`  `['{', '|', '}', '~']` - symbols from 123 to 126 position

## Example sequence class `CustomCharactersSequence`
It is a class which await for string sequence that must be in password
```
myrule = CustomCharactersSequence("watermelon")
generator.appendRules([myrule])
```
This is a just example. You can create same class, which will take sequence of rules and it will work in the same way too
