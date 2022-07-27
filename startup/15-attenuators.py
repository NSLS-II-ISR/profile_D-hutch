from ophyd import Device, Component as Cpt
from nslsii.devices import TwoButtonShutter

class AttnShutter(TwoButtonShutter):
    def stop(self):
        # do not want the default stop behavior of closing
        ...

class AttenuatorBank(Device):
    attn1 = Cpt(AttnShutter, '{Fil:1}')
    attn2 = Cpt(AttnShutter, '{Fil:2}')
    attn3 = Cpt(AttnShutter, '{Fil:3}')
    attn4 = Cpt(AttnShutter, '{Fil:4}')

bank = AttenuatorBank('XF:04IDD-ES', name='bank')