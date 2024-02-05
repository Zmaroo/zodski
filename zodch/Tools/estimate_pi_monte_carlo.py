
import random

def estimate_pi_monte_carlo(n):
    inside_circle = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x**2 + y**2 <= 1:  # Check if the point is inside the quarter circle
            inside_circle += 1
    return 4 * inside_circle / n  # Return the estimation of pi
