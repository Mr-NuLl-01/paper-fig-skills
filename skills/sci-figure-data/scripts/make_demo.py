#!/usr/bin/env python3
"""Original synthetic DEMO: choose representations from two different tasks."""
import argparse
import json
import os
import tempfile
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', tempfile.mkdtemp(prefix='sci-data-mpl-'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def save(fig, out, name):
    fig.savefig(out / (name + '.svg'), bbox_inches='tight')
    fig.savefig(out / (name + '.png'), dpi=180, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'svg.fonttype': 'none', 'font.size': 10,
                         'axes.spines.top': False, 'axes.spines.right': False})
    palette = ['#275D83', '#9C6033', '#7660A0']
    rows = []
    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    for batch in range(3):
        for sample in range(4):
            before = 3.4 + 0.65 * batch + 0.23 * sample + 0.12 * np.sin(sample + batch)
            after = before + [0.48, 1.08, -0.15, 0.72][sample] + 0.12 * batch
            offset = (sample - 1.5) * 0.035 + (batch - 1) * 0.13
            ax.plot([offset, 1 + offset], [before, after], color=palette[batch], alpha=.55, lw=1)
            ax.scatter([offset, 1 + offset], [before, after], color=palette[batch], s=32,
                       marker=['o', 's', '^'][batch], label=f'Batch {batch+1}' if sample == 0 else None)
            rows.extend([{'sample_id': f'B{batch+1}-S{sample+1}', 'batch_id': batch+1,
                          'condition': label, 'value': float(val)}
                         for label, val in [('Before', before), ('After', after)]])
    ax.set(xticks=[0, 1], xticklabels=['Before', 'After'], xlim=(-.4, 1.4),
           ylabel='DEMO response (a.u.)', title='DEMO | Paired samples across batches')
    ax.legend(frameon=False, loc='upper left')
    fig.subplots_adjust(bottom=.20)
    fig.text(.12, .025, 'Synthetic values; n = 12 paired DEMO units in 3 batches. No inference.', fontsize=8)
    save(fig, out, 'demo-paired-batches')

    delay = np.array([1.2, 1.7, 2.3, 2.8, 3.4, 4.0, 4.8, 5.5, 6.3])
    quality = np.array([71, 77, 80, 78, 85, 84, 88, 87, 89])
    parameter = np.arange(len(delay))
    frontier = [i for i in range(len(delay))
                if not any(delay[j] <= delay[i] and quality[j] >= quality[i]
                           and (delay[j] < delay[i] or quality[j] > quality[i])
                           for j in range(len(delay)))]
    fig, ax = plt.subplots(figsize=(6.4, 3.7))
    pts = ax.scatter(delay, quality, c=parameter, cmap='viridis', s=65, edgecolor='white', lw=.8)
    ax.plot(delay[frontier], quality[frontier], color='#444444', linestyle='--', lw=1,
            label='Non-dominated DEMO settings')
    for i in [0, 4, 8]:
        ax.annotate(f'P{i}', (delay[i], quality[i]), xytext=(5, 6), textcoords='offset points', fontsize=8)
    fig.colorbar(pts, ax=ax, label='Ordered DEMO setting index', pad=.03)
    ax.set(xlabel='DEMO delay (ms; lower is preferred)', ylabel='DEMO quality score (%)',
           title='DEMO | Retain the tradeoff rather than one winner', ylim=(68, 93))
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    fig.subplots_adjust(bottom=.23)
    fig.text(.12, .025, 'Synthetic values; frontier computed from the stated two-objective rule.', fontsize=8)
    save(fig, out, 'demo-tradeoff')
    manifest = {'status': 'SYNTHETIC_DEMO_NOT_RESEARCH_DATA',
                'purpose': 'Demonstrate task-dependent representation; not a universal layout.',
                'paired_data': rows,
                'tradeoff': [{'setting': int(i), 'delay_ms': float(delay[i]),
                             'quality_percent': int(quality[i]), 'non_dominated': i in frontier}
                            for i in range(len(delay))],
                'evidence_type': 'synthetic demonstration', 'statistical_inference': False}
    (out / 'demo-data.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(out)


if __name__ == '__main__':
    main()
