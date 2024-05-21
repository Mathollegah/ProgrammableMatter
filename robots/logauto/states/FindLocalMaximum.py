class FindLocalMaximum():
    def __init__(self):
        self.state = 'go_top'

    def reset(self):
        self.state = 'go_top'

    def move(self, directions):
        #print(self.state)
        if self.state == 'go_top':
            # Go straight top
            if directions[0][1] != None:
                return directions[0][0]

            # Go halve step top
            if directions[4][1] != None:
                return directions[4][0]

            if directions[5][1] != None:
                return directions[5][0]

            if directions[6][1] != None:
                return directions[6][0]

            if directions[7][1] != None:
                return directions[7][0]

            # Search on same level
            self.state = 'go_back'

        if self.state == 'go_back':
            if directions[3][1] != None:
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (None, None, None, None, None):
                    return directions[3][0]
                else:
                    self.state = 'go_top'
            else:
                # Search on same level (other direction)
                self.state = 'go_front'

        if self.state == 'go_front':
            if directions[2][1] != None:
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (
                None, None, None, None, None):
                    return directions[2][0]
                else:
                    self.state = 'go_top'
                    return -1

            else:
                # Local maximum reached
                if (directions[0][1], directions[4][1], directions[5][1], directions[6][1], directions[7][1]) == (
                None, None, None, None, None):
                    self.state = 'terminate'
                else:
                    self.state = 'go_top'
                return -1
