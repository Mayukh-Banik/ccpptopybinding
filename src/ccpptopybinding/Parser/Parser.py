import os

class Parser:
    def __init__(self,
                 name : str,
                 ):
        pass

    @staticmethod
    def fromJSON(

    ) -> Parser:
        return Parser(

        )

    @staticmethod
    def fromFile(
        filePath : str
        ):
        if os.path.isfile(filePath) is False:
            return None
        else:
            return Parser()
