class Metrics:
    def __init__(self):
        self.number_of_backtracks = 0
        self.number_of_flips = 0
        self.number_of_var_picks = 0

    def backtrack(self):
        self.number_of_backtracks += 1

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
        )

