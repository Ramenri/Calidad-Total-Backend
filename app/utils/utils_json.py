from functools import wraps

class UtilsJSON:


    @staticmethod
    def JSON(cls):
        @wraps(cls)
        def getJSON(self) -> dict:
            result = {}
            for attr, value in self.__dict__.items():
                if attr.startswith(f"_{cls.__name__}__"):
                    attr = attr[len(f"_{cls.__name__}__"):]
                result[attr] = value
            return result

        cls.getJSON = getJSON
        return cls