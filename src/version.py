import itertools
import re


class Version:
    def __init__(self, version) -> None:
        self.text = version
        self.epoch, self.upstream, self.revision = split_debian_version(version)

    def __repr__(self) -> str:
        return self.text

    def __hash__(self) -> int:
        return hash(self.text)

    def __eq__(self, other) -> bool:
        if isinstance(other, Version):
            return self._compare(other) == 0
        else:
            raise NotImplementedError

    def __gt__(self, other) -> bool:
        if isinstance(other, Version):
            return self._compare(other) >= 1
        else:
            raise NotImplementedError

    def __lt__(self, other) -> bool:
        if isinstance(other, Version):
            return self._compare(other) <= -1
        else:
            raise NotImplementedError

    def __ge__(self, other) -> bool:
        if isinstance(other, Version):
            return self._compare(other) >= 0
        else:
            raise NotImplementedError

    def __le__(self, other) -> bool:
        if isinstance(other, Version):
            return self._compare(other) <= 0
        else:
            raise NotImplementedError

    def _compare(self, other) -> int:
        """
        compare 2 debain version strings
        """
        if int(self.epoch) > int(other.epoch):
            return 1
        if int(self.epoch) < int(other.epoch):
            return -1

        rc = debian_upstream_compare(self.upstream, other.upstream)
        if rc:
            return rc

        return debian_upstream_compare(self.revision, other.revision)


def split_debian_version(version):
    """
    split a debian version string into an epoch, upstream version and debian revision
    """
    pattern = re.compile(
        r"((\d+):)?(([0-9A-Za-z.+~-]+(?=-))|([0-9A-Za-z.+~]+))(-([0-9A-Za-z.+~]+))?"
    )
    result = re.match(pattern, version)

    if result is None:
        raise AssertionError(
            f'function failed to match "{version}" as a dpkg version string'
        )
    if result.string != version:
        raise AssertionError(
            f"function matched {result.string} instead of {version} when must match all input string"  # noqa: E501
        )

    _, epoch, upstream, _, _, _, revision = result.groups("0")

    return epoch, upstream, revision


def order(c):
    """
    give a weight to the character to order in the debian version comparison.
    """
    if c == "~":
        return -1
    elif c == " ":
        return 0
    elif c.isdigit():
        return int(c) + 1
    elif c.isalpha():
        return ord(c)
    else:
        return ord(c) + 256


def debian_upstream_compare(first, second):
    """
    compare a debian upstream version or revision string with another
    """
    first = re.findall(r"\d+|\D+", first)
    second = re.findall(r"\d+|\D+", second)

    for a, b in itertools.zip_longest(first, second, fillvalue="0"):
        if a.isdigit() and b.isdigit():
            a = int(a)
            b = int(b)
            if a < b:
                return -1
            if a > b:
                return 1
        else:
            a = (order(c) for c in a)
            b = (order(c) for c in b)
            for ac, bc in itertools.zip_longest(a, b, fillvalue=0):
                if ac < bc:
                    return -1
                if ac > bc:
                    return 1
    return 0
