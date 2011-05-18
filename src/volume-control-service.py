#! /usr/bin/python2
# -*- coding: utf-8 -*-

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import cream
import pulseaudio

class VolumeControlService(cream.Module):

    def __init__(self):

        cream.Module.__init__(self, 'org.sbillaudelle.VolumeControlService')

        self.hotkeys.connect('hotkey-activated', self.hotkey_activate_cb)

        self.pulse = pulseaudio.PulseAudio('Volume Control Service')
        self.pulse.connect()


    def hotkey_activate_cb(self, hotkeys, action):

        volume = self.pulse.get_volume()
        mute = self.pulse.get_mute()
		
        if action == 'raise-volume':
            vol = (min(100, volume[0] + 5), min(100, volume[1] + 5))
            self.pulse.set_volume(vol)
            self.messages.debug("Increasing volume to '{0}'…".format(vol[0]))
        elif action == 'lower-volume':
            vol = (max(0, volume[0] - 5), max(0, volume[1] - 5))
            self.pulse.set_volume(vol)
            self.messages.debug("Lowering volume to '{0}'…".format(vol[0]))
        elif action == 'mute-volume':
            self.pulse.set_mute(not mute)
            self.messages.debug("Muting…")
        elif action == 'change-sink':
            sinks = self.pulse.get_sinks().keys()
            for i in xrange(0, len(sinks)):
                if sinks[i] == self.pulse.get_default_sink():
                    sink = sinks[(i + 1) % len(sinks)]
                    self.pulse.set_default_sink(sink)
                    self.messages.debug("Setting '{0}' as default sink…".format(sink))


if __name__ == '__main__':
    volume_control_service = VolumeControlService()
    volume_control_service.main()
