
class Version:
    def __init__(self, version: str):
        self.ver = version

    def __lt__(self, other):
        format_self, format_other = make_format(self.ver, other.ver)

        if format_self < format_other:
            return True
        return False

    def __gt__(self, other):
        format_self, format_other = make_format(self.ver, other.ver)

        if format_self > format_other:
            return True
        return False

    def __ne__(self, other):
        if self.ver != other.ver:
            return True
        return False


def make_format(*args) -> tuple:

    result = tuple()

    for a in args:
        new_string = ''
        for char in a:
            if not char.isdigit():
                continue

            new_string += char

        result += (new_string,)
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
        print(version_1, version_2)
        assert Version(version_1) < Version(version_2), 'le failed'
        assert Version(version_2) > Version(version_1), 'ge failed'
        assert Version(version_2) != Version(version_1), 'neq failed'


if __name__ == "__main__":
    main()
