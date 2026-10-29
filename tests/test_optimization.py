import numpy as np

from cardiff_converter_opt.optimization import pareto_sweep
from cardiff_converter_opt.parameters import DesignParameters


def test_pareto_sweep_explores_switching_frequency():
    # Regression: with unscaled variables SLSQP left f_sw at its 175 kHz start value.
    p = DesignParameters()
    pts = pareto_sweep(p)
    f_sw = np.array([pt.f_sw for pt in pts])
    assert np.ptp(f_sw) > 0.5 * (p.max_frp - p.min_frp)
    # Loss-weighted end should pick a lower frequency than the volume-weighted end.
    assert f_sw[-1] < f_sw[0]


def test_pareto_sweep_trades_loss_against_volume():
    pts = pareto_sweep()
    loss = np.array([pt.p_total for pt in pts])
    vol = np.array([pt.v_total_m3 for pt in pts])
    # Raising the loss weight should not increase loss or decrease volume.
    assert np.all(np.diff(loss) <= 1e-6)
    assert np.all(np.diff(vol) >= -1e-12)
