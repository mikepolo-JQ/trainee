
weight_dict = {
    '': 0,

    'dev': 1,
    '-dev': 1,

    'rc': 2,
    '-rc': 2,

    'a': 100,
    '-a': 100,
    'alpha': 100,
    '-alpha': 100,

    'b': 101,
    '-b': 101,
    'beta': 101,
    '-beta': 101,

}


class Version:
    def __init__(self, version: str):
        self.ver = version

        self.ver_in_parts = [part for part in version.split('.')]

    def __lt__(self, other: "Version"):

        # determine which part_list is longer
        longer = func_longer(self.ver_in_parts, other.ver_in_parts)

        # then there is a comparison in parts
        for i in range(len(longer)):

            # if the parts are equal before, and
            # the quantity of version parts
            # is greater , it is greater
            try:
                self_part = self.ver_in_parts[i]
                other_part = other.ver_in_parts[i]
            except IndexError:
                if longer is self.ver_in_parts:
                    return False
                return True

            # divide part into digits and chars
            digit_format_self, char_format_self, digit_format_other, char_format_other = \
                make_format(self_part, other_part)

            # comparison by chars starts there if digits of part are equal
            if digit_format_self == digit_format_other:

                # if a suitable key isn't found in weight_dict,
                # the comparison will be alphabetically

                self_part_weight = weight_dict.get(char_format_self, None)
                other_part_weight = weight_dict.get(char_format_other, None)

                if not(self_part_weight and other_part_weight):
                    self_part_weight = char_format_self
                    other_part_weight = char_format_other

                if self_part_weight < other_part_weight:
                    return True

                elif self_part_weight == other_part_weight:
                    continue

                else:
                    return False

            if digit_format_self < digit_format_other:
                return True
            return False

    def __eq__(self, other):

        # if the quantity of pairs isn't equal - the versions aren't equal
        if len(self.ver_in_parts) != len(other.ver_in_parts):
            return False

        # then there is a comparison in parts
        for i in range(len(self.ver_in_parts)):

            self_part = self.ver_in_parts[i]
            other_part = other.ver_in_parts[i]

            # divide part into digits and chars
            digit_format_self, char_format_self, digit_format_other, char_format_other = \
                make_format(self_part, other_part)

            if digit_format_self != digit_format_other:
                return False

            # only if the type and value are equal, comparison will continue
            if weight_dict.get(char_format_self, char_format_self) == \
                    weight_dict.get(char_format_other, char_format_other):
                continue
            else:
                return False

        return True


def func_longer(a, b):
    if len(a) < len(b):
        return b
    return a


def make_format(*args) -> tuple:
    result = tuple()

    for string in args:
        new_digits_string = str()
        new_chars_string = str()
        for char in string:
            if char.isdigit():
                new_digits_string += char
            else:
                new_chars_string += char

        result += (new_digits_string, new_chars_string)
    return result


def main():
    to_test = [
        ('1.0.0', '2.0.0'),
        ('1.0.0', '1.42.0'),
        ('1.2.0', '1.2.42'),
        ('1.1.0-alpha', '1.2.0-alpha.1'),
        ('1.0.1b', '1.0.10-alpha.beta'),
        ('1.0.0', '1.0.0-rc.1'),
        ('1.0.0alpha', '1.0.0-beta'),
        ('1.0.0a', '1.0.0c')
    ]

    for version_1, version_2 in to_test:

        assert Version(version_2) != Version(version_1), 'neq failed'
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'


if __name__ == "__main__":
    main()
