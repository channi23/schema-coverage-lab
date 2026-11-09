"""Rebuild the study's vector figure (optional ReportLab4.4.9 dependency)."""
import argparse
import json
from pathlib import Path
from reportlab.graphics.shapes import Drawing, String, Line
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics import renderPDF, renderSVG
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, default=ROOT / "paper/figures")
options = parser.parse_args()
options.output.mkdir(parents=True, exist_ok=True)
summary = json.loads((ROOT / "results/milestone-2/summary.json").read_text())
methods = ["decision", "predicate", "independence", "boundary", "random"]
colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#333333"]
drawing = Drawing(540, 270)
for panel, (metric, title) in enumerate([
    ("independence", "(a) Local independence coverage"),
    ("mutant_detectable", "(b) Root-observable mutation detection"),
]):
    x = 45 + panel * 270
    plot = LinePlot()
    plot.x, plot.y, plot.width, plot.height = x, 70, 210, 155
    plot.data = [[(int(r["budget"]), float(r[metric]["mean"]))
                  for r in summary["comparisons"] if r["method"] == method] for method in methods]
    plot.xValueAxis.valueMin, plot.xValueAxis.valueMax = 2, 8
    plot.xValueAxis.valueSteps = [2, 4, 8]
    plot.yValueAxis.valueMin, plot.yValueAxis.valueMax = 0, 1.02
    plot.yValueAxis.valueSteps = [0, .25, .5, .75, 1]
    for axis in (plot.xValueAxis, plot.yValueAxis):
        axis.labels.fontName, axis.labels.fontSize = "Helvetica", 9
    for i, color in enumerate(colors):
        plot.lines[i].strokeColor, plot.lines[i].strokeWidth = HexColor(color), 1.5
        plot.lines[i].symbol = makeMarker("FilledCircle")
        plot.lines[i].symbol.size = 3
        plot.lines[i].symbol.fillColor = HexColor(color)
        plot.lines[i].symbol.strokeColor = HexColor(color)
    plot.lines[4].strokeDashArray = [3, 2]
    drawing.add(plot)
    drawing.add(String(x + 105, 244, title, textAnchor="middle", fontName="Helvetica-Bold", fontSize=10))
    drawing.add(String(x + 105, 45, "Distinct-input budget", textAnchor="middle", fontName="Helvetica", fontSize=9))
for i, (method, color) in enumerate(zip(methods, colors)):
    x = 14 + i * 107
    drawing.add(Line(x, 19, x + 16, 19, strokeColor=HexColor(color), strokeWidth=1.6))
    drawing.add(String(x + 20, 16, method.capitalize(), fontName="Helvetica", fontSize=8.5))
renderPDF.drawToFile(drawing, str(options.output / "results.pdf"))
renderSVG.drawToFile(drawing, str(options.output / "results.svg"))
