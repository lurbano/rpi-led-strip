# Function to find the slope
def slope(x_1, y_1, x_2, y_2):
    # Get vertical and Horizontal differences
    Dx = x_2 - x_1
    Dy = y_2 - y_1
    # Calculate Slope
    s = Dy / Dx
    # Return result to main program
    return s


# MAIN PROGRAM STARTS HERE

# First Point
x1 = 2
y1 = 4

# Second Point
x2 = 6
y2 = 7

# Use function to get the slope
m = slope(x1, y1, x2, y2)

# Print result
print(f'The slope is {m}')
