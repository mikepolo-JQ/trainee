
class Version:
    def __init__(self, version: str):
        self.ver = version

    def __lt__(self, other):
        digit_format_self, char_format_self, digit_format_other, char_format_other = \
            make_format(self.ver, other.ver)

        if digit_format_self == digit_format_other:
            if char_format_self < char_format_other:
                return True
            return False

        if digit_format_self < digit_format_other:
            return True
        return False

    def __gt__(self, other):
        digit_format_self, char_format_self, digit_format_other, char_format_other = \
            make_format(self.ver, other.ver)

        if digit_format_self == digit_format_other:
            if char_format_self > char_format_other:
                return True
            return False

        if digit_format_self > digit_format_other:
            return True
        return False

    def __ne__(self, other):
        if self.ver != other.ver:
            return True
        return False


def make_format(*args) -> tuple:
    result = tuple()

    for string in args:
        new_digits_string = str()
        new_chars_string = str()
        for char in string:
            if char == '.':
                new_chars_string += char
                new_digits_string += char
            elif char.isdigit():
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
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()
