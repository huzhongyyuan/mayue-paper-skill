"""Generate original, editable research diagram scaffolds (no experimental data).

Usage: python generate_templates.py [output_directory]
All coordinates, labels and connections can be edited here; standard library only.
"""
from pathlib import Path
from html import escape
import sys

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
OUT.mkdir(parents=True, exist_ok=True)
C = dict(ink="#24354a", muted="#65758a", line="#bdc8d4", blue="#e4effb",
         green="#e5f3eb", orange="#fff0df", purple="#f1eafa", gray="#f1f4f7")


class Diagram:
    def __init__(self, title, subtitle, height=670):
        self.height = height
        self.parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img">
<title>{escape(title)}</title><desc>{escape(subtitle)} Original editable conceptual template; no experimental results.</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="{C['muted']}"/></marker></defs>
<style>text{{font-family:Arial,Helvetica,sans-serif;fill:{C['ink']}}}.body{{font-size:18px}}.small{{font-size:15px;fill:{C['muted']}}}.label{{font-size:20px;font-weight:600}}</style>
<rect width="1200" height="{height}" fill="white"/>''']
        self.text(32, 43, title, 27, weight=700)
        self.text(32, 72, subtitle, 16, color=C['muted'])

    def text(self, x, y, label, size=18, weight=400, color=None, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"' + (f' style="fill:{color}"' if color else '') + f'>{escape(label)}</text>')

    def box(self, x, y, w, h, fill="gray", stroke=None, dash=False, radius=10):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{C.get(fill,fill)}" stroke="{stroke or C["line"]}" stroke-width="1.5"' + (' stroke-dasharray="7 5"' if dash else '') + '/>')

    def node(self, x, y, w, h, lines, fill="gray"):
        self.box(x,y,w,h,fill)
        if isinstance(lines,str): lines=[lines]
        for n,t in enumerate(lines): self.text(x+w/2,y+h/2+(n-(len(lines)-1)/2)*24+6,t,18,anchor="middle")

    def arrow(self, points, dash=False, color=None):
        p=" ".join(f'{x},{y}' for x,y in points)
        self.parts.append(f'<polyline points="{p}" fill="none" stroke="{color or C["muted"]}" stroke-width="2" marker-end="url(#arrow)"' + (' stroke-dasharray="6 5"' if dash else '') + '/>')

    def footer(self, label="STRUCTURAL TEMPLATE · replace labels and paths with verified method details"):
        self.text(32,self.height-22,label,14,color=C['muted'])

    def save(self, name):
        self.footer()
        (OUT/name).write_text("\n".join(self.parts)+"\n</svg>",encoding="utf-8")


def framework():
    d=Diagram("01 / Learn control, then temporal coherence", "Example organization only · match stages, parameter states and objectives to your implementation",700)
    d.box(28,99,780,224,"#fcfdff")
    d.text(48,132,"A  Control learning",21,700)
    d.node(48,159,144,62,["Paired image","+ control"],"blue")
    d.node(238,159,164,62,["Control encoder","TRAIN"],"blue")
    d.node(452,159,176,62,["Image backbone","FROZEN"],"gray")
    d.node(672,159,111,62,"Prediction","green")
    d.arrow([(192,190),(238,190)])
    d.arrow([(402,190),(452,190)])
    d.arrow([(628,190),(672,190)])
    d.node(459,254,164,45,"Control objective","purple")
    d.arrow([(727,221),(727,276),(623,276)],True)
    d.text(49,282,"Verify parameter states.",15,color=C['muted'])
    d.box(28,344,780,263,"#fcfdff")
    d.text(48,378,"B  Temporal learning",21,700)
    d.node(48,414,144,72,["Unpaired","video data"],"orange")
    d.node(238,414,164,72,["Transferred","input encoder"],"blue")
    d.node(452,414,176,72,["Temporal adapter","TRAIN"],"orange")
    d.node(672,414,111,72,["Video","output"],"green")
    d.arrow([(192,450),(238,450)])
    d.arrow([(402,450),(452,450)])
    d.arrow([(628,450),(672,450)])
    d.arrow([(320,221),(320,414)])
    d.text(330,339,"transfer",14,color=C['muted'])
    d.node(459,542,164,42,"Video objective","purple")
    d.arrow([(727,486),(727,563),(623,563)],True)
    d.text(49,572,"Specify which inherited parameters remain fixed.",15,color=C['muted'])
    d.box(835,99,335,508,"#fcfdff")
    d.text(857,132,"C  Adapter detail",21,700)
    d.node(894,159,218,55,"Input feature h","gray")
    d.node(894,262,218,67,["Learned update","Δh = B(A(h))"],"orange")
    d.node(894,383,218,55,"Residual: h + Δh","green")
    d.arrow([(1003,214),(1003,262)])
    d.arrow([(1003,329),(1003,383)])
    d.arrow([(1112,186),(1144,186),(1144,411),(1112,411)])
    d.text(857,482,"Solid: forward / transfer route",15,color=C['muted'])
    d.text(857,510,"Dashed: objective dependency",15,color=C['muted'])
    d.text(857,548,"Detail is a generic adapter.",15,color=C['muted'])
    d.text(857,572,"Replace with the real operation.",15,color=C['muted'])
    d.save("01-framework.svg")


def motivation():
    d=Diagram("02 / Diagnose two factors separately", "Controlled-comparison layout · all sample panels below are placeholders, not generated results",670)
    for n,(x,title,variable,fixed) in enumerate([
        (28,"A  Factor A sweep","Vary: input resolution","Fix: expansion ratio, model, input, seed"),
        (615,"B  Factor B sweep","Vary: expansion ratio","Fix: input resolution, model, input, seed")]):
        d.box(x,102,557,490,"#fcfdff")
        d.text(x+20,137,title,21,700)
        d.text(x+20,169,variable,17)
        d.text(x+20,196,fixed,15,color=C['muted'])
        for j,level in enumerate(["Level 1","Level 2","Level 3"]):
            xx=x+20+j*176
            d.text(xx+79,240,level,17,600,anchor="middle")
            d.box(xx,256,157,145,"gray",dash=True)
            d.text(xx+78.5,320,"REAL SAMPLE",14,600,anchor="middle")
            d.text(xx+78.5,346,"to be inserted",14,anchor="middle",color=C['muted'])
            d.box(xx,416,157,63,"orange",dash=True)
            d.text(xx+78.5,453,"Matched crop",14,anchor="middle")
        d.text(x+20,517,"Observe: define an error before comparing samples.",16)
        d.text(x+20,547,"Report: protocol, metric, repetitions and uncertainty.",15,color=C['muted'])
    d.text(32,627,"A diagnostic figure supports a mechanism only to the extent that the variables and evidence isolate it.",17)
    d.save("02-motivation.svg")


def window():
    d=Diagram("03 / Global context meets local position", "Conceptual coordinate illustration · no learned attention or empirical correspondence is shown",680)
    d.box(28,105,500,473,"#fcfdff")
    d.text(49,142,"A  Shared canvas coordinates",21,700)
    for yy in range(180,441,52):
        d.parts.append(f'<line x1="63" y1="{yy}" x2="483" y2="{yy}" stroke="#dbe1e8"/>')
    for xx in range(63,484,60):
        d.parts.append(f'<line x1="{xx}" y1="180" x2="{xx}" y2="440" stroke="#dbe1e8"/>')
    d.box(94,213,171,120,"orange",stroke="#bf7c33",radius=2)
    d.text(108,249,"Anchor window",17,600)
    d.text(108,278,"source context",15)
    d.box(278,298,171,120,"green",stroke="#4f8665",radius=2)
    d.text(292,335,"Target window",17,600)
    d.text(292,363,"local generation",15)
    d.arrow([(179,338),(179,389),(268,389)])
    d.text(194,380,"Δx, Δy",16)
    d.text(63,482,"Relative position is defined in one coordinate system.",16)
    d.text(63,515,"Use normalized offsets / scale only if your method does.",15,color=C['muted'])
    d.box(554,105,618,473,"#fcfdff")
    d.text(577,142,"B  Conditional generation path",21,700)
    d.node(580,183,235,65,["Anchor representation","global content"],"orange")
    d.node(876,183,265,65,["Relative coordinates","local position"],"green")
    d.node(580,302,235,64,["Context encoder","specify actual features"],"orange")
    d.node(876,302,265,64,["Position encoder","specify encoding"],"green")
    d.node(703,453,328,67,["Target-window generator","specify fusion / injection site"],"blue")
    d.arrow([(697,248),(697,302)])
    d.arrow([(1008,248),(1008,302)])
    d.arrow([(697,366),(697,404),(789,404),(789,453)])
    d.arrow([(1008,366),(1008,404),(950,404),(950,453)])
    d.text(32,617,"Ablation plan: isolate context, position and their interaction under the same generation protocol.",17)
    d.save("03-window-alignment.svg")


def streaming():
    d=Diagram("04 / Make online timing explicit", "Rolling-window illustration · separate throughput, first-output latency and control-response latency",690)
    d.text(32,135,"Frame index →",18,600)
    for k in range(8): d.text(332+k*103,135,f"t{k}",18,600,anchor="middle")
    rows=[(177,"Update n",2,4),(305,"Update n + 1",3,5),(433,"Update n + 2",4,6)]
    for y,label,start,end in rows:
        d.text(33,y+45,label,19,600)
        for k in range(8):
            xx=286+k*103
            fill="gray" if k<start else "orange" if k<=end else "white"
            d.box(xx,y,92,81,fill,dash=k>end,radius=6)
            state="emitted" if k<start else "active" if k<=end else "pending"
            d.text(xx+46,y+47,state,14,anchor="middle")
        d.box(280+start*103,y-7,(end-start+1)*103+1,95,"none",stroke="#c78034",radius=8)
    d.arrow([(543,268),(646,296)])
    d.arrow([(646,397),(749,424)])
    d.text(34,565,"New control at update n → first affected output: record both timestamps in the implementation.",17)
    d.text(34,600,"Orange: active window    Gray: committed history    Dashed: future output not yet produced",16,color=C['muted'])
    d.text(34,630,"Verify causality, overlap and state reuse; this template does not prescribe a particular streaming algorithm.",15,color=C['muted'])
    d.save("04-streaming.svg")


if __name__ == "__main__":
    framework(); motivation(); window(); streaming()
    print(f"Generated four editable SVG templates in {OUT.resolve()}")
