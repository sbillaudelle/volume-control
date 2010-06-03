import cream
import cream.ipc

import pulseaudio

HOTKEYS = {
    'raise-volume': 'XF86AudioRaiseVolume',
    'lower-volume': 'XF86AudioLowerVolume',
    'mute-volume': 'XF86AudioMute',
    'change-sink': '<Ctrl>XF86AudioMute'
    }

class VolumeControl(cream.Module):

    def __init__(self):

        cream.Module.__init__(self)

        self.hotkey_manager = cream.ipc.get_object('org.cream.hotkeys', '/org/cream/hotkeys')
        self.hotkey_broker = cream.ipc.get_object('org.cream.hotkeys', self.hotkey_manager.register(), interface='org.cream.hotkeys.broker')

        for action, hotkey in HOTKEYS.iteritems():
            self.hotkey_broker.set_hotkey(action, hotkey)

        self.hotkey_broker.connect_to_signal('hotkey_activated', self.hotkey_activate_cb)

        self.pulse = pulseaudio.PulseAudio('Volume Control Service')
        self.pulse.connect()


    def hotkey_activate_cb(self, action):

        volume = self.pulse.get_volume()
        mute = self.pulse.get_mute()
		
        if action == 'raise-volume':
            vol = (min(100, volume[0] + 5), min(100, volume[1] + 5))
            self.pulse.set_volume(vol)
        elif action == 'lower-volume':
            vol = (max(0, volume[0] - 5), max(0, volume[1] - 5))
            self.pulse.set_volume(vol)
        elif action == 'mute-volume':
            self.pulse.set_mute(not mute)
        elif action == 'change-sink':
            sinks = self.pulse.get_sinks().keys()
            for i in xrange(0, len(sinks)):
                if sinks[i] == self.pulse.get_default_sink():
                    self.pulse.set_default_sink(sinks[(i + 1) % len(sinks)])


if __name__ == '__main__':
    volume_control = VolumeControl()
    volume_control.main()