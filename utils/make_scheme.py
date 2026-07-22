class Color:
    def __init__(self,r:int,g:int,b:int):
        self.r = r
        self.g = g
        self.b = b

    def at_ratio(self, ratio: float) -> 'Color':
        main = ratio * 2 if ratio < 0.5 else 2 - ratio * 2
        white = 1 - ratio * 2 if ratio < 0.5 else 0

        return Color(
            int(self.r*main + white*255),
            int(self.g*main + white*255),
            int(self.b*main + white*255)
        )

    def format(self, 
        name:str,
        millistep:int,
        middle: float = 0.5,
        power: float = 0,
        boundarie_scale: float= 1.0,
    ) -> str:
        ratio = millistep/1000.

        ratio = ratio * boundarie_scale + (1-boundarie_scale)

        if power > 0:
            sign = -1 if ratio < 0.5 else +1
            ratio = 0.5 + 0.5 * sign * abs(2*ratio - 1)**power

        if ratio < middle:
            ratio = ratio * 0.5 / middle 
        else:
            ratio = 0.5 + 0.5 * (ratio - middle) / (1-middle)

        c = self.at_ratio(ratio)
        return f"--color-{name:s}-{millistep:d}: {c.r:3d}, {c.g:3d}, {c.b:3d}; --preview: #{c.r:02x}{c.g:02x}{c.b:02x};"

NEUTRAL = Color(127,127,127)
PRIMARY = Color(0xCC, 0xFF, 0) # Electric Lime
SECONDARY = Color(0, 0xCC, 0xFF) # Emerald?

STEPS= (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)

mapping = [
    ("neutral",   NEUTRAL,   0.50, 0.125, 1.0 ),
    ("primary",   PRIMARY,   0.30, 2,     1.0 ),
    ("secondary", SECONDARY, 0.30, 2,     1.0 ),
]

TEMPLATE = f"""
:root {{
    --color-neutral: 255, 255, 255;
    {"\n    ".join(
        c.format(n,s, m, p, x)
        for n,c,m,p,x in mapping
        for s in STEPS
    )}
}}
"""

print(TEMPLATE)