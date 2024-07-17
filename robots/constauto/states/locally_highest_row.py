class LocallyHighestRow():
    def __init__(self):
        self.state = 'run_north'

    def reset(self):
        self.state = 'run_north'

    def move(self, moves):
        if 'U' in moves:
            return 'U'

        for direction in moves:
            if 'U' in direction:
                return direction

        if self.state == 'run_north':
            if 'F' in moves:
                return 'F'
            else:
                self.state = 'run_south'

        if self.state == 'run_south':
            if 'B' in moves:
                return 'B'
            else:
                self.state = 'terminate'


