# Password Generator (Python 3)
Module for simple password generation with custom rules.

## Password Generator
### Initialization
PasswordGenerator await for iterable of rules. Rules must await `List[int]` and return boolean value.
This is some ways to make generator.
```
# Ways to make generator with no rules
generator = PasswordGenerator(()) # Initialized with empty types which supports transition into list
generator = PasswordGenerator([])
generator = PasswordGenerator(dict()) # Only keys
generator = PasswordGenerator(set())
generator = PasswordGenerator(frozenset())
```

### `append_rules` and `remove_rules`
Be careful with append wrong function! If function would not return true value, generator try to make another password. And futher before 2**32 times to tries by default.
```
# Some types which supports transition into list
generator.append_rules((boolFirstRule, boolSecondRule, ...))

# Any types with iteration support
generator.removed_rules((boolFirstRule, boolSecondRule, ...))
```

By some reason two functions may have different hashes. But `__code__` of these functions never change.

### `fetch_password`
Use this function for generate password according to rules. You can use `library` and `use_ascii=False` for generate password. Also you can write your bool function but it is not effective.
```
# Lower case english password
generator = PasswordGenerator(())
generator.fetch_password(16, (DefaultRules.LOWER_EN,), use_ascii=False)

# Is more effective then
def bool_lower(password):
    return all(96 < char < 123 for char in password)

generator = PasswordGenerator((bool_lower,))
generator.fetch_password(16, ())
```

### `generate_password`
Function is build list of chars which located between `[start; stop]` of randrom group of library. Generate password without used rules and `random.seed()`. Seed is using in `fetch_password`.
```
library = [(start1, stop1), (start2, stop2), ...]
generator.generate_password(lenth, library)
```

Library is groups in interval from `[start ...` to `... stop]`, include side's points; `random.choice` is using for choice random group points, `random.randint` is using for choice symbol. If you want ASCII library (without codes like `\x00` ), you should use `ASCII_GROUPS` in library.

### Seed generator
If you gonna change pseudo random number generator (like the `self.seed_generator` by default), you can do some things like this.
```
generator.seed_generator = func # Where func is something like time.time_ns%10**10
```

## DefaultRules
Default rules is required for creating the most strongly password. You can do not use rules, or add yours rules. Contains `ASCII_GROUPS` for library, they can be used as a rule. `DefaultRules.` For convenience `DefaultRules` have `FIGURES`, `LOWER_EN` and `UPPER_EN`.
There is `from_sequence` which takes string and return closure bool function.
