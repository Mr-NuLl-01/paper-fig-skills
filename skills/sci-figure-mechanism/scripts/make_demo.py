#!/usr/bin/env python3
"""Original synthetic DEMO: separate spatial transport from energy alignment."""
import argparse
import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='sci-mechanism-mpl-'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


BLUE, RED, GREEN, GRAY = '#216487', '#B74C46', '#33836B', '#606060'


def arrow(ax, xy1, xy2, text, color=GRAY, dashed=False, offset=(0, .1)):
    ax.annotate('', xy=xy2, xytext=xy1,
                arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': 1.8,
                            'linestyle': '--' if dashed else '-'})
    ax.text((xy1[0]+xy2[0])/2+offset[0], (xy1[1]+xy2[1])/2+offset[1], text,
            ha='center', va='bottom', color=color, fontsize=10)


def save(fig, out, name):
    fig.savefig(out / (name+'.svg'), bbox_inches='tight')
    fig.savefig(out / (name+'.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    out = parser.parse_args().output_dir
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'svg.fonttype': 'none', 'font.size': 10})

    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.add_patch(Rectangle((.25, .25), 5.5, 2.9, facecolor='#F2F4F5', edgecolor='#A8ADB0'))
    ax.text(3, 2.92, 'DEMO homogeneous medium | drift only', ha='center', color=GRAY)
    arrow(ax, (1, 2.45), (5, 2.45), 'E points right', color=GRAY, offset=(0, .12))
    arrow(ax, (4.7, 1.8), (1.3, 1.8), 'electron particle flux: left', color=BLUE, offset=(0, .12))
    arrow(ax, (1.3, 1.1), (4.7, 1.1), 'hole particle flux: right', color=RED, offset=(0, .12))
    arrow(ax, (1.3, .48), (4.7, .48), 'conventional drift current: right', color=GREEN, offset=(0, .10))
    ax.set(xlim=(0, 6), ylim=(-.3, 3.65), xlabel='Position x (qualitative spatial axis)', yticks=[],
           title='DEMO | Spatial directions require an explicit model')
    ax.set_xticks([])
    for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
    fig.subplots_adjust(bottom=.20)
    fig.text(.12, .025, 'Synthetic concept. Assumes positive mobilities and no diffusion or ionic current.', fontsize=8)
    save(fig, out, 'demo-spatial-drift')

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    levels = {'State set A': {'x': .7, 'CB': -2.8, 'VB': -5.2},
              'State set B': {'x': 2.6, 'CB': -3.3, 'VB': -5.0}}
    ax.axhline(0, color=GRAY, lw=1)
    ax.text(.08, .08, 'Vacuum reference = 0 eV', fontsize=9, color=GRAY)
    for label, d in levels.items():
        for key in ['CB', 'VB']:
            ax.plot([d['x']-.45, d['x']+.45], [d[key], d[key]], color=BLUE if key == 'CB' else RED, lw=2)
            ax.text(d['x'], d[key]-.12, f'DEMO {key}: {d[key]} eV', ha='center', va='top', fontsize=9)
        ax.text(d['x'], -5.85, label, ha='center')
    arrow(ax, (1.12, -2.8), (2.16, -3.3), 'proposed e- transfer', BLUE, True, offset=(0, .16))
    arrow(ax, (2.6, -3.3), (2.6, -5.0), 'proposed\nradiative step', GREEN, True, offset=(.65, -.05))
    ax.set(xlim=(-.1, 3.8), ylim=(-6.15, .55), ylabel='Energy E (eV; all values are DEMO)',
           title='DEMO | Energy alignment is not a spatial trajectory', xticks=[])
    fig.subplots_adjust(bottom=.20)
    fig.text(.12, .025, 'Horizontal spacing is categorical, not distance. Dashed arrows = proposed DEMO processes.', fontsize=7.5)
    for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
    save(fig, out, 'demo-energy-alignment')
    manifest = {'status': 'SYNTHETIC_DEMO_NOT_A_REAL_DEVICE',
                'spatial_model': 'Drift-only homogeneous medium with positive mobilities; no diffusion or ions.',
                'direction_basis': {'E': 'right', 'electron_flux': 'left', 'hole_flux': 'right',
                                    'conventional_drift_current': 'right'},
                'energy_values_eV': levels, 'energy_reference': 'vacuum',
                'energy_horizontal_axis': 'categorical, not spatial',
                'process_evidence': 'proposed synthetic demonstration only',
                'purpose': 'Verify coordinate and arrow grammar, not assert a material mechanism.'}
    (out/'demo-mechanism.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(out)


if __name__ == '__main__':
    main()
