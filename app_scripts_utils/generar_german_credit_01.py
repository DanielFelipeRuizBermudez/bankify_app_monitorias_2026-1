from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "statlog+german+credit+data" / "german.data"
OUTPUT_PATH = ROOT / "app" / "assets" / "eda" / "german_credit_01.png"


def main() -> None:
    df = pd.read_csv(DATA_PATH, sep=" ", header=None)
    counts = df[20].value_counts()
    good, bad = int(counts[1]), int(counts[2])
    total = good + bad

    names = {f.name for f in font_manager.fontManager.ttflist}
    plt.rcParams["font.family"] = "Inter" if "Inter" in names else "DejaVu Sans"

    ink, muted, grid = "#0f172a", "#475569", "#e2e8f0"
    colors = ["#00c29b", "#be123c"]
    labels = ["Crédito bueno", "Crédito malo"]
    details = [
        "El cliente cumplió\nel contrato del crédito",
        "El cliente no cumplió\nel contrato del crédito",
    ]

    fig, ax = plt.subplots(figsize=(10.6, 5.0), dpi=100)
    fig.patch.set_facecolor("white")
    bars = ax.barh([1, 0], [good, bad], color=colors, height=0.62)

    for bar, value in zip(bars, [good, bad]):
        y = bar.get_y() + bar.get_height() / 2
        ax.text(
            value + 12, y, f"{value} créditos  ·  {value / total:.0%}",
            va="center", ha="left", fontsize=12.5, color=ink, fontweight="semibold",
        )

    ax.set_yticks([1, 0])
    ax.set_yticklabels([""] * 2)
    for ypos, label, detail in zip([1, 0], labels, details):
        ax.text(
            -0.025, ypos + 0.13, label, transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=12.5, fontweight="bold", color=ink,
        )
        ax.text(
            -0.025, ypos - 0.12, detail, transform=ax.get_yaxis_transform(),
            ha="right", va="center", fontsize=10, color=muted, linespacing=1.3,
        )
    ax.set_xlim(0, total)
    ax.set_xlabel("Número de créditos (de 1.000 en total)", fontsize=11, color=muted, labelpad=8)
    ax.tick_params(axis="x", colors=muted, labelsize=10)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=grid, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(grid)

    fig.text(
        0.012, 0.96, "¿Cuántos de los 1.000 créditos fueron buenos y cuántos malos?",
        fontsize=15, fontweight="bold", color=ink, ha="left", va="top",
    )
    fig.text(
        0.012, 0.895,
        "Son créditos que un banco alemán ya había otorgado entre 1973 y 1975. Un crédito es bueno si el cliente\n"
        "cumplió lo pactado en el contrato y malo si no lo cumplió. Esto es lo que el modelo aprende a predecir.",
        fontsize=10.5, color=muted, ha="left", va="top", linespacing=1.45,
    )
    fig.text(
        0.012, 0.065,
        "Nota de muestreo: en la muestra se incluyeron a propósito más créditos malos de los que había en la realidad, "
        "así que el 30 % no es la tasa real de incumplimiento del banco.",
        fontsize=9, color=muted, ha="left", va="bottom",
    )
    fig.text(
        0.012, 0.02,
        "Fuente: South German Credit Data (UCI), Prof. Hans Hofmann, Universidad de Hamburgo.",
        fontsize=9, color="#94a3b8", ha="left", va="bottom",
    )

    fig.subplots_adjust(left=0.25, right=0.97, top=0.72, bottom=0.24)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=100, facecolor="white")


if __name__ == "__main__":
    main()
