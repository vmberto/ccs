def getColor(color): # pragma: no cover
    if (color == 'success'):
        return (0, 255, 0)
    elif (color == 'error'):
        return (255, 0, 0)
    elif (color == 'waiting'):
        return (255, 250, 205)
    else:
        return (255, 255, 255)

def colored(color, text): # pragma: no cover
    r, g, b = getColor(color)
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def log(log, color, testing): # pragma: no cover
    if (not testing):
        print(colored(color, log))
