"""Render a 12-lead WFDB record as a paper-style ECG: 25 mm/s, 10 mm/mV, calibrated grid.

Layout follows the standard clinical printout. There are four 2.5-second columns
(I/II/III, aVR/aVL/aVF, V1-V3, V4-V6), each showing its leads over that column's time window,
plus a full 10-second lead II rhythm strip. Each row starts with a 1 mV x 200 ms calibration
pulse. All drawing is done in millimetres, and the figure is sized in millimetres, so an SVG
viewed at 100% (or a PNG printed at its dpi) measures true to paper.

Every parameter below is published with the renders, so they can be reproduced exactly.

Usage:
  python render.py <record path without extension> <out.svg|out.png> [--title TEXT]
"""
import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import wfdb  # noqa: E402
from scipy.signal import butter, sosfiltfilt  # noqa: E402

PAPER_SPEED = 25.0      # mm per second
GAIN = 10.0             # mm per mV
COLUMN_SECONDS = 2.5
ROW_HEIGHT = 37.5       # mm between row baselines (3.75 mV)
CAL_WIDTH = 10.0        # mm reserved at the left of each row for the calibration pulse
MARGIN = 5.0            # mm around the grid
FOOTER = 8.0            # mm below the grid for the caption
HIGHPASS_HZ = 0.5       # baseline-wander removal (zero-phase Butterworth, order 2)
LOWPASS_HZ = 100.0      # display smoothing, comparable to a clinical 100-150 Hz filter
GRID_MINOR = "#f6c6c6"  # 1 mm
GRID_MAJOR = "#e48a8a"  # 5 mm
TRACE = "#111111"
TRACE_WIDTH = 0.6       # points

LAYOUT = [["I", "AVR", "V1", "V4"],
          ["II", "AVL", "V2", "V5"],
          ["III", "AVF", "V3", "V6"]]
RHYTHM_LEAD = "II"
LABELS = {"AVR": "aVR", "AVL": "aVL", "AVF": "aVF"}


def load(record_path):
    rec = wfdb.rdrecord(record_path)
    if any(u.lower() != "mv" for u in rec.units):
        raise ValueError(f"expected mV units, got {rec.units}")
    sig = np.nan_to_num(rec.p_signal)
    sos_hp = butter(2, HIGHPASS_HZ, "highpass", fs=rec.fs, output="sos")
    sos_lp = butter(2, LOWPASS_HZ, "lowpass", fs=rec.fs, output="sos")
    sig = sosfiltfilt(sos_lp, sosfiltfilt(sos_hp, sig, axis=0), axis=0)
    leads = {name.upper(): sig[:, i] for i, name in enumerate(rec.sig_name)}
    return leads, rec.fs, rec.sig_len / rec.fs


def render(record_path, out_path, title="", dpi=300):
    leads, fs, duration = load(record_path)
    duration = min(duration, 4 * COLUMN_SECONDS)
    trace_w = duration * PAPER_SPEED
    n_rows = len(LAYOUT) + 1
    grid_w = CAL_WIDTH + trace_w
    grid_h = n_rows * ROW_HEIGHT
    fig_w = grid_w + 2 * MARGIN
    fig_h = grid_h + 2 * MARGIN + FOOTER

    fig = plt.figure(figsize=(fig_w / 25.4, fig_h / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-MARGIN, grid_w + MARGIN)
    ax.set_ylim(-MARGIN - FOOTER, grid_h + MARGIN)
    ax.set_aspect("equal")
    ax.axis("off")

    for x in np.arange(0, grid_w + 0.01, 1.0):
        ax.plot([x, x], [0, grid_h], color=GRID_MAJOR if round(x) % 5 == 0 else GRID_MINOR,
                lw=0.5 if round(x) % 5 == 0 else 0.25, zorder=0)
    for y in np.arange(0, grid_h + 0.01, 1.0):
        ax.plot([0, grid_w], [y, y], color=GRID_MAJOR if round(y) % 5 == 0 else GRID_MINOR,
                lw=0.5 if round(y) % 5 == 0 else 0.25, zorder=0)

    def baseline(row):  # row 0 is the top row
        return grid_h - (row + 0.6) * ROW_HEIGHT

    def cal_pulse(y0):
        x0, w = 2.0, 0.2 * PAPER_SPEED  # 200 ms
        ax.plot([x0 - 1, x0, x0, x0 + w, x0 + w, x0 + w + 1],
                [y0, y0, y0 + GAIN, y0 + GAIN, y0, y0], color=TRACE, lw=TRACE_WIDTH)

    def trace(lead, t0, t1, y0):
        i0, i1 = int(t0 * fs), int(t1 * fs)
        seg = leads[lead][i0:i1]
        x = CAL_WIDTH + (np.arange(i0, i0 + len(seg)) / fs) * PAPER_SPEED
        ax.plot(x, y0 + seg * GAIN, color=TRACE, lw=TRACE_WIDTH, solid_joinstyle="round")
        ax.text(CAL_WIDTH + t0 * PAPER_SPEED + 1.0, y0 + 0.45 * ROW_HEIGHT,
                LABELS.get(lead, lead), fontsize=8, va="top", family="sans-serif")

    for r, row in enumerate(LAYOUT):
        y0 = baseline(r)
        cal_pulse(y0)
        for c, lead in enumerate(row):
            t0 = c * COLUMN_SECONDS
            trace(lead, t0, t0 + COLUMN_SECONDS, y0)
            if c:  # lead-change marker
                xm = CAL_WIDTH + t0 * PAPER_SPEED
                ax.plot([xm, xm], [y0 - 3, y0 + 3], color=TRACE, lw=TRACE_WIDTH)
    y0 = baseline(len(LAYOUT))
    cal_pulse(y0)
    trace(RHYTHM_LEAD, 0, duration, y0)

    caption = f"{PAPER_SPEED:g} mm/s   {GAIN:g} mm/mV   {HIGHPASS_HZ:g}-{LOWPASS_HZ:g} Hz"
    if title:
        caption += f"   {title}"
    ax.text(0, -MARGIN, caption, fontsize=7, va="center", family="sans-serif", color="#444444")
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("record")
    p.add_argument("out")
    p.add_argument("--title", default="")
    a = p.parse_args()
    render(a.record, a.out, a.title)


if __name__ == "__main__":
    main()
