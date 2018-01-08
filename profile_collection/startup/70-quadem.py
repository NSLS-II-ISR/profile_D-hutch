from ophyd.quadem import QuadEM
from ophyd import Signal


class QuadEMWithPort(QuadEM):
    port_name = Cpt(Signal, value='EM180')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.acquire_mode, 'One-shot')  # single mode
                                ])


# TODO talk to someone who understands this IOC about what is going on
class QuadEMWithPortSS(QuadEM):
    port_name = Cpt(Signal, value='EM180')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.acquire_mode, 'Multiple')  # single mode
                                ])


class SSASlit(Device):
    x_cntr = Cpt(EpicsMotor, '-Ax:XT}Mtr')
    x_gap = Cpt(EpicsMotor, '-Ax:XO}Mtr')
    y_cntr = Cpt(EpicsMotor, '-Ax:YT}Mtr')
    y_gap = Cpt(EpicsMotor, '-Ax:YO}Mtr')
    current = Cpt(QuadEMWithPortSS, 'XF:04IDB-BI:1{EM:3}EM180:',
                  add_prefix=())


ssa = SSASlit('XF:04IDB-OP:1{SSA:1', name='ssa')


class BPM1(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    current = Cpt(QuadEMWithPort, 'XF:04IDA-BI:1{EM:1}EM180:',
                  add_prefix=())


class BPM2(Device):
    x_cntr = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    x_gap = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    y_cntr = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    y_gap = Cpt(EpicsMotor, '-Ax:YGap}Mtr')
    current = Cpt(QuadEMWithPort, 'XF:04IDA-BI:1{EM:2}EM180:',
                  add_prefix=())


bpm1 = BPM1('XF:04IDA-BI:0{BPM:1_SR1', name='bpm1')
bpm2 = BPM2('XF:04IDA-BI:1{BPM:2', name='bpm2')
