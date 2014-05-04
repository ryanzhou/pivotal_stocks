from pivotal_stocks import app

STARTING_COLOR = "#FF8F09"
MEDIAN_COLOR = "#FFFFFF"
ENDING_COLOR = "#66E152"

def rgb_tuple(s):
    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))

def rgb_code(t):
    return "#%02X%02X%02X" % t

def value_at_position(value, upper, lower, a, b, c):
    try:
        pos = (float(value)-lower)/(upper-lower)
        mid_pos = (0.0-lower)/(upper-lower) if upper > 0 and lower < 0 else 0.5
        return int(b+(c-b)*(pos-mid_pos)*(1/(1-mid_pos))) if pos >= mid_pos else int(a+(b-a)*pos*(1/mid_pos))
    except TypeError:
        return 224

@app.context_processor
def cell_color_processor():
    def cell_color(value, upper, lower):
        r1, g1, b1 = rgb_tuple(STARTING_COLOR)
        r2, g2, b2 = rgb_tuple(MEDIAN_COLOR)
        r3, g3, b3 = rgb_tuple(ENDING_COLOR)
        r = value_at_position(value, upper, lower, r1, r2, r3)
        g = value_at_position(value, upper, lower, g1, g2, g3)
        b = value_at_position(value, upper, lower, b1, b2, b3)
        return rgb_code((r, g, b))
    return dict(cell_color=cell_color)
