from artiq.experiment import *


class InteractiveDemo(EnvExperiment):

    def run(self):
        print("Waiting for user input...")
        try:
            with self.interactive(title="Interactive Demo") as interactive:
                interactive.setattr_argument("number", 
                                            NumberValue(42e-6, unit="us", precision=4))
        except CancelledArgsError:
            print("User cancelled")
            return
        
        print("Done! Values:")
        print(interactive.number, type(interactive.number))
