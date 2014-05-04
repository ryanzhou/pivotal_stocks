from pivotal_stocks import app

STARTING_COLOR = "#FF8F09"
MEDIAN_COLOR = "#FFFFFF"
ENDING_COLOR = "#66E152"

def rgb_tuple(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

def rgb_code(t):
    return "#%02X%02X%02X" % t

def value_at_position(index, length, a, b, c):
    pos = float(index)/length
    return int(b+(c-b)*(pos-0.5)*2) if pos >= 0.5 else int(a+(b-a)*pos*2)

@app.context_processor
def cell_color_processor():
    def cell_color(value, values):
        if value != None:
            r1, g1, b1 = rgb_tuple(STARTING_COLOR)
            r2, g2, b2 = rgb_tuple(MEDIAN_COLOR)
            r3, g3, b3 = rgb_tuple(ENDING_COLOR)
            index = list(values).index(value)
            r = value_at_position(index, len(values), r1, r2, r3)
            g = value_at_position(index, len(values), g1, g2, g3)
            b = value_at_position(index, len(values), b1, b2, b3)
            return rgb_code((r, g, b))
        else:
            return "#DDDDDD"
    return dict(cell_color=cell_color)
