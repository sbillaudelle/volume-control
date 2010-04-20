import alsaaudio as alsa
import gtk

import cream
import cream.ipc

class VolumeControl(cream.Module):

    def __init__(self):

        cream.Module.__init__(self)

        self.hotkey_manager = cream.ipc.get_object('org.cream.hotkeys', '/org/cream/hotkeys')
        self.hotkey_broker = cream.ipc.get_object('org.cream.hotkeys', self.hotkey_manager.register(), interface='org.cream.hotkeys.broker')
        self.hotkey_broker.set_hotkey('raise-volume', 'XF86AudioRaiseVolume')
        self.hotkey_broker.set_hotkey('lower-volume', 'XF86AudioLowerVolume')
        self.hotkey_broker.set_hotkey('mute-volume', 'XF86AudioMute')
        self.hotkey_broker.connect_to_signal('hotkey_activated', self.hotkey_activate_cb)

        self.mixer = alsa.Mixer()


    def hotkey_activate_cb(self, action):
		
        if action == 'raise-volume':
            vol = self.mixer.getvolume()[0]
            if vol <= 95:
                self.mixer.setvolume(vol + 5)
            else:
                self.mixer.setvolume(100)
        elif action == 'lower-volume':
            vol = self.mixer.getvolume()[0]
            if vol >= 5:
                self.mixer.setvolume(vol - 5)
            else:
                self.mixer.setvolume(0)
        elif action == 'mute-volume':
            mute = self.mixer.getmute()[0]
            if mute:
                self.mixer.setmute(False)
            else:
                self.mixer.setmute(True)


if __name__ == '__main__':
    volume_control = VolumeControl()
    volume_control.main()
