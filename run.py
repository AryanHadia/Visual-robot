# run the progress of the program
from core import Core

class Run:
    def __init__(self):
        self.core = Core()

    def main(self):
        self.core.run()

Run().main()
