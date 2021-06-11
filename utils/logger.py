def colored(r, g, b, text): # pragma: no cover
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def log(log, color, testing): # pragma: no cover
    (red, green, blue) = color
    if (not testing):
        print(colored(red, green, blue, log))
