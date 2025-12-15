from colorama import Style, Fore, Back, init

init(autoreset=True)

class ConsoleLogger:
    def __init__(self):
        self.SUCCESS_COLOR = Style.BRIGHT + Fore.GREEN
        self.WARNING_COLOR = Style.BRIGHT + Fore.YELLOW
        self.ERROR_COLOR = Style.BRIGHT + Fore.RED
        self.INFO_COLOR = Fore.CYAN
        self.TERMINATION_COLOR = Fore.MAGENTA + Style.BRIGHT

        self.SUCCESS_PREFIX = f"[{Fore.GREEN}SUCCESS{Style.RESET_ALL}{self.SUCCESS_COLOR}] "
        self.WARNING_PREFIX = f"[{Fore.YELLOW}WARNING{Style.RESET_ALL}{self.WARNING_COLOR}] "
        self.ERROR_PREFIX = f"[{Fore.RED}ERROR{Style.RESET_ALL}{self.ERROR_COLOR}] "
        self.INFO_PREFIX = f"[{Fore.CYAN}INFO{Style.RESET_ALL}{self.INFO_COLOR}] "
        self.TERMINATION_PREFIX = f"[{Fore.MAGENTA}TERMINATED{Style.RESET_ALL}{self.TERMINATION_COLOR}] "

    def _log(self, prefix, color, message):
        """Internal helper to structure and print messages."""
        print(prefix + color + message)

    def info(self, message):
        self._log(self.INFO_PREFIX, self.INFO_COLOR, message)

    def success(self, message):
        self._log(self.SUCCESS_PREFIX, self.SUCCESS_COLOR, message)

    def warn(self, message):
        self._log(self.WARNING_PREFIX, self.WARNING_COLOR, message)

    def error(self, message):
        self._log(self.ERROR_PREFIX, self.ERROR_COLOR, message)

    def terminate(self, message):
        self._log(self.TERMINATION_PREFIX, self.TERMINATION_COLOR, message)
