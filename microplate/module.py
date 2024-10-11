
class ModuleInterface:
    socket = None

    def __init__(self, io, tick):
        self.io = None
        if io is not None:
            self.io = io
        self.ticks = [tick]
        self.time_counters = [0]
        self.actions = [self.action]
        self.data = 0
        self.callback = None

    def add_action(self, tick, function):
        self.ticks.append(tick)
        self.time_counters.append(0)
        self.actions.append(function)

    def tick(self, dt):
        results = []
        for idx in range(0, len(self.time_counters)):
            results.append(False)
            self.time_counters[idx] += dt
            if self.time_counters[idx] >= self.ticks[idx]:
                self.time_counters[idx] = 0.0
                self.actions[idx]()
                results[idx] = True

        return results

    def action(self):
        raise Exception("define action")
        
    def value(self):
        return self.data
