"""A discrete event simulation framework."""

import debug, config

class Event(object):
    """An occurrence initiated from within the simulation."""

    def __init__(self, label, sender, bubble_time = 0):

        assert bubble_time >= time

        self.label = label
        self.sender = sender
        self.time = bubble_time

    def __repr__(self):
        return '%s (t = %d, s = %s)' % (self.label, self.time, self.sender)
        
class Dispatcher(object):
    """Allows functions to be called when an event occurs."""

    def __init__(self):
        self.listeners = {}

    def register(self, event_label, listener):
        """Register a function to be called when an event occurs."""
        if event_label not in self.listeners:
            self.listeners[event_label] = []
        self.listeners[event_label].append(listener)

    def bubble(self, event):
        """Execute registered listeners. Do not call from outside."""
        log_event(event)
        if event.label not in self.listeners:
            return
        for listener in self.listeners[event.label]:
            listener(event)

def log_event(event):
    """Print a log message to standard output when events occur."""
    if event.label not in config.events_printed:
        return

    headers = []
    headers.append(('Time', '%d' % time))
    headers.append((event.sender.__class__.__name__, event.label))

    debug.print_object(event.sender, headers = headers)

time = 0
events = []
dispatcher = Dispatcher()
    
def run():
    """Enumerate events and bubble each until no more events exist.

    Events live in the events list (sim.events), which can be altered at
    will, including while the simulation is running.
    """
    while len(events) > 0:
        event = min(events, key = lambda e: e.time)
        global time
        assert event.time >= time

        time = event.time
        events.remove(event)
        dispatcher.bubble(event)