class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# First Point
p1 =  point(2, 4)

# Second Point
p2 = point(6, 7)

# Vertical and Horizontal differences
Dx = p2.x - p1.x
Dy = p2.y - p1.y

# Calculate Slope
m = Dy / Dx

# Print result
print(f'The slope is {m}')
