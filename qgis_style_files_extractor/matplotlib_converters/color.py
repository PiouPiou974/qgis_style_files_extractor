import matplotlib.colors
import numpy as np


def rgb_hex_and_alpha_to_rgba(hex_color: str, alpha: int) -> tuple[float, float, float, float]:
    return matplotlib.colors.to_rgba(hex_color, alpha / 255)


def rgba_to_hex_and_alpha(s: str | None) -> tuple[str | None, float | None]:
    if s is None:
        return None, None

    r, g, b, alpha = (int(v)/255 for v in s.split(','))
    color = matplotlib.colors.to_hex((r, g, b), keep_alpha=False)
    return color, alpha


def rgba_to_one_letter_color_and_alpha(s: str) -> tuple[str | None, str | None]:
    if s is None:
        return None, None

    named_colors = {
        'b': [0.0, 0.0, 1.0],  # b: blue
        'c': [0.0, 0.75, 0.75],  # c: cyan
        'g': [0.0, 0.5, 0.0],  # g: green
        'k': [0.0, 0.0, 0.0],  # k: black
        'm': [0.75, 0.0, 0.75],  # m: magenta
        'r': [1.0, 0.0, 0.0],  # r: red
        'w': [1.0, 1.0, 1.0],  # w: white
        'y': [0.75, 0.75, 0.0],  # y: yellow
    }
    r, g, b, alpha = (float(int(v) / 255) for v in s.split(','))
    color = [r, g, b]

    colors = np.array(list(named_colors.values()))
    color = np.array(color)

    distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    index_of_smallest = np.where(distances == np.amin(distances))
    closest_color = colors[index_of_smallest][0]

    closest_named_color = [k for k, v in named_colors.items() if all(x[0] == x[1] for x in zip(v, closest_color))][0]
    return closest_named_color, alpha
