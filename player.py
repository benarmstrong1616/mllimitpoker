class Player:
    def resume(self):
        resume = input("Keep playing? (y/n)")
        return resume != 'n'

    def make_decision(self, stack, pot, hand, board, options):
        random.shuffle(options)
        return options[0]