class Fish:     # following is just used for the purpose of example in main
    def __init__(self, *args, **kwargs):
        self.preferred_flow_depth = float()
        self.preferred_flow_velocity = float()
        self.species = ""
        self.xy_position = tuple()

    def print_habitat(self):
        print("The species {0} prefers {1}m deep and {2}m/s fast flowing waters.".format(self.species,
                                                                                         str(self.preferred_flow_depth),
                                                                                         str(
                                                                                             self.preferred_flow_velocity)))


# define the child class Salmon, which inherits (is-a-type-of) from Fish
class Salmon(Fish):
    def __init__(self, species, *args, **kwargs):
        Fish.__init__(self)
        self.family = "salmonidae"
        self.species = species

    def habitat_function(self, depth, velocity):
        self.preferred_flow_depth = depth
        self.preferred_flow_velocity = velocity


atlantic_salmon = Salmon("Salmo salar")
atlantic_salmon.habitat_function(depth=0.4, velocity=0.5)
atlantic_salmon.print_habitat()

pacific_salmon = Salmon("Oncorhynchus tshawytscha")
pacific_salmon.habitat_function(depth=0.6, velocity=0.8)
pacific_salmon.print_habitat()
