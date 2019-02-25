class Metrics:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.number_of_backtracks = 0
        self.number_of_flips = 0
        self.number_of_var_picks = 0
        self.simplifications = 0

    def simplify(self, modifications):
        self.simplifications += modifications

    def backtrack(self):
        self.number_of_backtracks += 1
        if self.verbose:
            print(self.number_of_backtracks)

    def flip(self):
        self.number_of_flips += 1

    def pick_var(self):
        self.number_of_var_picks += 1

    def __repr__(self):
        return (
            "number_of_backtracks:"
            + str(self.number_of_backtracks)
            + "\n"
            + "number_of_flips:"
            + str(self.number_of_flips)
            + "\n"
            + "number_of_var_picks:"
            + str(self.number_of_var_picks)
            + "\n"
            + "simplifications:"
            + str(self.simplifications)
        )

