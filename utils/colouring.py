

class ConsoleColors:
    r"""Инструмент для окрашивания текста в консоли.
    """

    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Яркие цвета
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Фоновые цвета
    BACKGROUND_BLACK = "\033[40m"
    BACKGROUND_RED = "\033[41m"
    BACKGROUND_GREEN = "\033[42m"
    BACKGROUND_YELLOW = "\033[43m"
    BACKGROUND_BLUE = "\033[44m"
    BACKGROUND_MAGENTA = "\033[45m"
    BACKGROUND_CYAN = "\033[46m"
    BACKGROUND_WHITE = "\033[47m"

    @classmethod
    def colour_text(cls, text: str, colour: str) -> str:
        match colour.upper():
            case 'BLACK':
                return cls._update(text, cls.BLACK)
            case 'RED':
                return cls._update(text, cls.RED)
            case 'GREEN':
                return cls._update(text, cls.GREEN)
            case 'YELLOW':
                return cls._update(text, cls.YELLOW)
            case 'BLUE':
                return cls._update(text, cls.BLUE)
            case 'MAGENTA':
                return cls._update(text, cls.MAGENTA)
            case 'CYAN':
                return cls._update(text, cls.CYAN)
            case 'WHITE':
                return cls._update(text, cls.WHITE)

    @classmethod
    def colour_bright_text(cls, text, colour):
        match colour.upper():
            case 'BLACK':
                return cls._update(text, cls.BRIGHT_BLACK)
            case 'RED':
                return cls._update(text, cls.BRIGHT_RED)
            case 'GREEN':
                return cls._update(text, cls.BRIGHT_GREEN)
            case 'YELLOW':
                return cls._update(text, cls.BRIGHT_YELLOW)
            case 'BLUE':
                return cls._update(text, cls.BRIGHT_BLUE)
            case 'MAGENTA':
                return cls._update(text, cls.BRIGHT_MAGENTA)
            case 'CYAN':
                return cls._update(text, cls.BRIGHT_CYAN)
            case 'WHITE':
                return cls._update(text, cls.BRIGHT_WHITE)

    @classmethod
    def colour_background(cls, text, colour):
        match colour.upper():
            case 'BLACK':
                return cls._update(text, cls.BACKGROUND_BLACK)
            case 'RED':
                return cls._update(text, cls.BACKGROUND_RED)
            case 'GREEN':
                return cls._update(text, cls.BACKGROUND_GREEN)
            case 'YELLOW':
                return cls._update(text, cls.BACKGROUND_YELLOW)
            case 'BLUE':
                return cls._update(text, cls.BACKGROUND_BLUE)
            case 'MAGENTA':
                return cls._update(text, cls.BACKGROUND_MAGENTA)
            case 'CYAN':
                return cls._update(text, cls.BACKGROUND_CYAN)
            case 'WHITE':
                return cls._update(text, cls.BACKGROUND_WHITE)

    @classmethod
    def _update(cls, text: str, color: str) -> str:
        return f'{color}{text}{cls.RESET}'

