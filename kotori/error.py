class ConfigError(ValueError):
    def __init__(self, message: str = ""):
        super().__init__(f"Config Error: {message}")
