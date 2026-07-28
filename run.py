# run the progress of the program
from core import Core

class Run:
    def __init__(self):
        self.core = Core()

    def main(self):
        self.menu()
        option = input("Enter your option: ").lower()
        while option not in ["qrcode" , "face"]:
            print("Invalid option")
            option = input("Enter your option: ").lower()
        self.core.run(option = option)

    def menu(self):
        print("================")
        print("qrcode")
        print("face")
        print("================")
    
    

Run().main()
