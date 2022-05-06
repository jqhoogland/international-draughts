"""
The standard library has a core module called "string", hence the "x" in this
module of eXtended string functions/constants.

"""

from math import ceil

HR = "-" * 80


def wrap_text(text: str, width=80) -> str:
    """Forces a (multiline) ``text`` string to a certain ``width``."""

    def _wrap_text(s: str):
        lines = ceil(len(s) / width)
        return "\n".join((s[i * width:min((i + 1) * width, len(s))].ljust(width) for i in range(lines)))

    return "\n".join(map(
        lambda s: _wrap_text(s), text.split("\n")))


def center_multiline(text: str, char=" ", width=80) -> str:
    """Pads a string on left and right.
    The built-in ``str.center(width, fillchar)`` doesn't work with multiline strings
    """
    return "\n".join(map(lambda s: s.center(width, char), text.split("\n")))
