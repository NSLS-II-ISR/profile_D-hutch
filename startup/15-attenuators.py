from ophyd import Device, Component as Cpt
from nslsii.devices import TwoButtonShutter


class AttnShutter(TwoButtonShutter):
    def stop(self):
        # do not want the default stop behavior of closing
        ...


class AttenuatorBank(Device):
    attn1 = Cpt(AttnShutter, "{Fil:1}")
    attn2 = Cpt(AttnShutter, "{Fil:2}")
    attn3 = Cpt(AttnShutter, "{Fil:3}")
    attn4 = Cpt(AttnShutter, "{Fil:4}")

    def set_attenuation_level(self, n):
        s1, s2, s3, s4 = [{"0": "Close", "1": "Open"}[v] for v in format(n, "04b")]
        yield from bps.mv(
            bank.attn1,
            s1,
            bank.attn2,
            s2,
            bank.attn3,
            s3,
            bank.attn4,
            s4,
        )


bank = AttenuatorBank("XF:04IDD-ES", name="bank")
