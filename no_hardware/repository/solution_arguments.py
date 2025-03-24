from artiq.experiment import *


class ArgumentsDemoSolution(EnvExperiment):

    def build(self):        
        self.setattr_argument("number", 
                              NumberValue(42e-6, unit="us", step=0.0001e-6, precision=4),
                              tooltip="This is a number argument")
        self.setattr_argument("string",
                              StringValue("Hello World"),
                              tooltip="This is a string argument")
        self.setattr_argument("boolean",
                              BooleanValue(True),
                              tooltip="This is a boolean argument")
        self.setattr_argument("enum", 
                              EnumerationValue(
                                    ["foo", "bar"], "foo", quickstyle=True),
                              tooltip="This is an enumeration argument")
        self.setattr_argument("scan", 
                              Scannable(global_max=400, 
                                        default=ExplicitScan([1,2,3]),
                                        precision=6))

    def run(self):
        print(self.boolean)
        print(self.enum)
        print(self.number, type(self.number))
        print(self.string)
        for i in self.scan:
            print(i)
