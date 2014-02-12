from . import bridge
from . import effects
from rgb import Colors, PartyModes

def connect(address='192.168.1.100', port=50000, protocol='udp', short_pause_duration=0.025, long_pause_duration=0.1):
    return bridge.Bridge(address=address, port=port, protocol=protocol, short_pause_duration=short_pause_duration, long_pause_duration=long_pause_duration)
