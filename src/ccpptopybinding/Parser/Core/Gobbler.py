import os

class Gobbler:
    def __init__(
            self, 
            workingDirectory: str | None = None):
        self.workingDirectory = workingDirectory
        self.outputDir : str | None = None

    @staticmethod
    def singleFile(
        *, 
        filePath: str
        ) -> Gobbler:
        if not os.path.isfile(filePath):
            raise FileNotFoundError(f"Not a file: {filePath}")
        return Gobbler(workingDirectory=os.path.dirname(os.path.abspath(filePath)))

    def setOutputDir(
            self,
            outputDir : str
    ) -> None:
        self.outputDir = outputDir
