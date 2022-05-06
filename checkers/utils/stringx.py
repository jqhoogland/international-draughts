from math import ceil

HR = "-" * 80


def wrap_text(text: str, width=80) -> str:
    def _wrap_text(s: str):
        lines = ceil(len(s) / width)
        return "\n".join((s[i * width:min((i + 1) * width, len(s))].ljust(width) for i in range(lines)))

    return "\n".join(map(
        lambda s: _wrap_text(s), text.split("\n")))


def center_text(text: str, char="", width=80) -> str:
    return "\n".join(map(lambda s: f"{{:{char}^{width}}}".format(s), text.split("\n")))
