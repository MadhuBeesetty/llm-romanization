#!/usr/bin/env python3
"""
plot_metrics.py — Publication-quality grouped bar charts for romanization
evaluation metrics. Saves two PDF figures for LaTeX embedding.

Run: python figures/plot_metrics.py  (from Template-2026/)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

FIG_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGES = ["Hindi", "Telugu", "Kannada"]
MODELS    = ["Anthropic", "GPT-4o", "Gemini", "Ollama (Qwen3.5)"]

DATA = {
    "query_bge": {
        "Anthropic":        [0.801, 0.767, 0.711],
        "GPT-4o":           [0.769, 0.760, 0.714],
        "Gemini":           [0.700, 0.600, 0.627],
        "Ollama (Qwen3.5)": [0.735, 0.584, 0.577],
    },
    "response_bge": {
        "Anthropic":        [0.837, 0.789, 0.733],
        "GPT-4o":           [0.828, 0.794, 0.749],
        "Gemini":           [0.763, 0.630, 0.664],
        "Ollama (Qwen3.5)": [0.787, 0.598, 0.537],
    },
    "query_bert_f1": {
        "Anthropic":        [0.669, 0.664, 0.621],
        "GPT-4o":           [0.647, 0.651, 0.627],
        "Gemini":           [0.598, 0.532, 0.550],
        "Ollama (Qwen3.5)": [0.622, 0.577, 0.514],
    },
    "query_bert_precision": {
        "Anthropic":        [0.640, 0.637, 0.592],
        "GPT-4o":           [0.617, 0.624, 0.599],
        "Gemini":           [0.571, 0.509, 0.525],
        "Ollama (Qwen3.5)": [0.595, 0.583, 0.485],
    },
    "query_bert_recall": {
        "Anthropic":        [0.702, 0.693, 0.654],
        "GPT-4o":           [0.680, 0.681, 0.658],
        "Gemini":           [0.628, 0.557, 0.578],
        "Ollama (Qwen3.5)": [0.653, 0.578, 0.552],
    },
    "response_bert_f1": {
        "Anthropic":        [0.676, 0.671, 0.620],
        "GPT-4o":           [0.663, 0.667, 0.641],
        "Gemini":           [0.617, 0.548, 0.569],
        "Ollama (Qwen3.5)": [0.639, 0.574, 0.549],
    },
    "response_bert_precision": {
        "Anthropic":        [0.644, 0.641, 0.588],
        "GPT-4o":           [0.632, 0.637, 0.610],
        "Gemini":           [0.587, 0.524, 0.541],
        "Ollama (Qwen3.5)": [0.609, 0.593, 0.577],
    },
    "response_bert_recall": {
        "Anthropic":        [0.711, 0.705, 0.657],
        "GPT-4o":           [0.699, 0.700, 0.677],
        "Gemini":           [0.650, 0.576, 0.601],
        "Ollama (Qwen3.5)": [0.672, 0.568, 0.534],
    },
}

COLORS = {
    "Anthropic":        "#2166AC",
    "GPT-4o":           "#4DAF4A",
    "Gemini":           "#E41A1C",
    "Ollama (Qwen3.5)": "#FF7F00",
}

BERT_Y_MIN, BERT_Y_MAX = 0.44, 0.76
BGE_Y_MIN,  BGE_Y_MAX  = 0.48, 0.88


def draw_grouped_bar(ax, metric_key, title, y_min, y_max, ylabel=None):
    values   = DATA[metric_key]
    n_langs  = len(LANGUAGES)
    n_models = len(MODELS)
    width    = 0.18
    offsets  = np.linspace(-(n_models - 1) / 2,
                            (n_models - 1) / 2, n_models) * width
    x = np.arange(n_langs)

    for model, offset in zip(MODELS, offsets):
        bars = ax.bar(x + offset, values[model], width,
                      color=COLORS[model], edgecolor="white",
                      linewidth=0.4, zorder=3)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2,
                    h + 0.003,
                    f"{h:.3f}",
                    ha="center", va="bottom",
                    fontsize=5, rotation=90, color="#333333")

    ax.set_title(title, fontsize=8.5, fontweight="bold", pad=5)
    ax.set_xticks(x)
    ax.set_xticklabels(LANGUAGES, fontsize=8)
    ax.set_ylim(y_min, y_max)
    ax.yaxis.set_minor_locator(MultipleLocator(0.02))
    ax.yaxis.set_tick_params(labelsize=7)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=7)


def make_legend(fig):
    handles = [mpatches.Patch(color=COLORS[m], label=m) for m in MODELS]
    fig.legend(handles=handles, loc="lower center", ncol=4,
               fontsize=8, frameon=False,
               bbox_to_anchor=(0.5, 0.01))


# Figure 1: BERTScore (2x3)
BERT_PANELS = [
    ("query_bert_f1",           "F1 --- Query"),
    ("query_bert_precision",    "Precision --- Query"),
    ("query_bert_recall",       "Recall --- Query"),
    ("response_bert_f1",        "F1 --- Response"),
    ("response_bert_precision", "Precision --- Response"),
    ("response_bert_recall",    "Recall --- Response"),
]

fig1, axes1 = plt.subplots(2, 3, figsize=(7.5, 5.0))
fig1.suptitle("BERTScore by Model and Language",
              fontsize=10, fontweight="bold", y=0.97)

for ax, (metric, title) in zip(axes1.flat, BERT_PANELS):
    ylabel = "BERTScore" if ax in axes1[:, 0] else None
    draw_grouped_bar(ax, metric, title, BERT_Y_MIN, BERT_Y_MAX, ylabel)

fig1.subplots_adjust(hspace=0.52, wspace=0.32, bottom=0.12)
make_legend(fig1)

bert_path = os.path.join(FIG_DIR, "bert_scores.pdf")
fig1.savefig(bert_path, dpi=300, bbox_inches="tight", format="pdf")
print(f"Saved: {bert_path}")


# Figure 2: BGE Cosine (1x2)
BGE_PANELS = [
    ("query_bge",    "BGE Cosine --- Query"),
    ("response_bge", "BGE Cosine --- Response"),
]

fig2, axes2 = plt.subplots(1, 2, figsize=(7.5, 2.8))
fig2.suptitle("BGE Embedding Cosine Similarity by Model and Language",
              fontsize=10, fontweight="bold", y=1.02)

for ax, (metric, title) in zip(axes2.flat, BGE_PANELS):
    ylabel = "Cosine Similarity" if ax is axes2[0] else None
    draw_grouped_bar(ax, metric, title, BGE_Y_MIN, BGE_Y_MAX, ylabel)

fig2.subplots_adjust(wspace=0.32, bottom=0.18)
make_legend(fig2)

bge_path = os.path.join(FIG_DIR, "bge_cosine.pdf")
fig2.savefig(bge_path, dpi=300, bbox_inches="tight", format="pdf")
print(f"Saved: {bge_path}")

print("Done.")
