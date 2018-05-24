from ophyd.quadem import QuadEM, QuadEMPort
from ophyd import Signal
from ophyd.areadetector import ADBase


class QuadEMWithPort(QuadEM):
    conf = Cpt(QuadEMPort, port_name='EM180')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('labels', ['electrometers'])
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.acquire_mode, 'One-shot')])


# TODO talk to someone who understands this IOC about what is going on
class QuadEMWithPortSS(QuadEM):
    conf = Cpt(QuadEMPort, port_name='EM180')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('labels', ['electrometers'])
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([(self.acquire_mode, 'Continuous')])


class SSASlit(Device):
    x_cntr = Cpt(EpicsMotor, '-Ax:XT}Mtr')
    x_gap = Cpt(EpicsMotor, '-Ax:XO}Mtr')
    y_cntr = Cpt(EpicsMotor, '-Ax:YT}Mtr')
    y_gap = Cpt(EpicsMotor, '-Ax:YO}Mtr')
    current = Cpt(QuadEMWithPortSS, 'XF:04IDB-BI:1{EM:3}EM180:',
                  add_prefix=(),
                  read_attrs=['sum_all.mean_value'] + \
                             [f'current{j}.mean_value' for j in range(1, 5)],
                  )


ssa = SSASlit('XF:04IDB-OP:1{SSA:1', name='ssa')


class BPM1(Device):
    x = Cpt(EpicsMotor, '-Ax:X}Mtr')
    y = Cpt(EpicsMotor, '-Ax:Y}Mtr')
    current = Cpt(QuadEMWithPort, 'XF:04IDA-BI:1{EM:1}EM180:',
                  add_prefix=(),
                  read_attrs=['sum_all.mean_value'] + \
                             [f'current{j}.mean_value' for j in range(1, 5)],
                  )


class BPM2(Device):
    x_cntr = Cpt(EpicsMotor, '-Ax:XCtr}Mtr')
    x_gap = Cpt(EpicsMotor, '-Ax:XGap}Mtr')
    y_cntr = Cpt(EpicsMotor, '-Ax:YCtr}Mtr')
    y_gap = Cpt(EpicsMotor, '-Ax:YGap}Mtr')
    current = Cpt(QuadEMWithPort, 'XF:04IDA-BI:1{EM:2}EM180:',
                  add_prefix=(),
                  read_attrs=['sum_all.mean_value'] + \
                             [f'current{j}.mean_value' for j in range(1, 5)],
                  )


bpm1 = BPM1('XF:04IDA-BI:0{BPM:1_SR1', name='bpm1')
bpm2 = BPM2('XF:04IDA-BI:1{BPM:2', name='bpm2')
