from render import rect

LINES = rect(0, 0, 5, 3.5)
LINES.extend(rect(0, 0, 1.2, 0.6))
LINES.extend(rect(1.2, 0, 0.4, 0.4))

LINES.extend(rect(3, 0, 2, 1.6))

LINES.append(((2.3, 0.2), (2.4, 0.2)))
LINES.append(((2.8, 0.2), (2.9, 0.2)))
LINES.append(((2.3, 0.7), (2.4, 0.7)))
LINES.append(((2.8, 0.7), (2.9, 0.7)))
LINES.append(((2.35, 0.9), (2.45, 0.9)))
LINES.append(((2.75, 0.9), (2.85, 0.9)))
LINES.append(((2.35, 1.3), (2.45, 1.3)))
LINES.append(((2.75, 1.3), (2.85, 1.3)))

LINES.extend(rect(3, 2.7, 2, 0.8))
LINES.extend(rect(3.5, 2.2, 0.5, 0.5))

LINES.extend(rect(0, 3, 2, 0.5))
LINES.extend(rect(0, 2.5, 0.5, 0.5))

if __name__ == "__main__":
    import render
    img = render.render(LINES)
    render.display(img)
