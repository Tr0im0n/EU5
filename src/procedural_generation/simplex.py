import numpy as np
import matplotlib.pyplot as plt

"""
Written by: GEMINI
"""


def simplex_noise_2d(x, y, seed=0):
    """
    Generates 2D Simplex noise for a given (x, y) coordinate.

    Args:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
        seed (int): An optional seed for reproducibility.

    Returns:
        float: The noise value, typically in the range [-1, 1].
    """
    # Constants for 2D Simplex noise
    F2 = 0.5 * (np.sqrt(3.0) - 1.0)  # Skew factor for 2D
    G2 = (3.0 - np.sqrt(3.0)) / 6.0  # Unskew factor for 2D

    # Permutation table (a simple hash for gradient selection)
    # This is a common way to implement the pseudo-randomness in Perlin/Simplex noise.
    # It should be a permutation of 0-255 repeated to cover 0-511.
    # For simplicity and reproducibility, we'll use a fixed one or generate based on seed.
    # In a real-world application, you might want a more robust permutation.
    p = np.arange(256, dtype=int)
    if seed != 0:
        np.random.seed(seed)
    np.random.shuffle(p)
    p = np.concatenate((p, p)) # Repeat for easy indexing

    # Gradients for 2D Simplex noise
    # These are unit vectors pointing in 12 directions (for 3D, it's 16 directions)
    # For 2D, we typically use 8 or 12 directions. Here, we use 8.
    grad2d = np.array([
        [1, 1], [-1, 1], [1, -1], [-1, -1],
        [1, 0], [-1, 0], [0, 1], [0, -1]
    ])

    # Skew the input coordinates to get into the simplex grid
    s = (x + y) * F2
    i = np.floor(x + s)
    j = np.floor(y + s)

    t = (i + j) * G2
    X0 = x - (i - t)  # Unskew the cell origin back to X, Y
    Y0 = y - (j - t)

    # Determine which simplex we are in (lower left or upper right triangle)
    if X0 > Y0:
        i1, j1 = 1, 0  # Lower right triangle
    else:
        i1, j1 = 0, 1  # Upper left triangle

    # A step of (1,0) or (0,1) in the skewed (i,j) coordinates corresponds to a step
    # of (1-G2, -G2) or (-G2, 1-G2) in the original (x,y) coordinates.
    X1 = X0 - i1 + G2
    Y1 = Y0 - j1 + G2
    X2 = X0 - 1.0 + 2.0 * G2
    Y2 = Y0 - 1.0 + 2.0 * G2

    # Hash coordinates of the three corners
    # The permutation table `p` is used to get a pseudo-random index for the gradient.
    # The modulo 256 is important because the permutation table is 256 elements long.
    ii = int(i) & 255
    jj = int(j) & 255

    gi0 = p[ii + p[jj]] % 8
    gi1 = p[ii + i1 + p[jj + j1]] % 8
    gi2 = p[ii + 1 + p[jj + 1]] % 8

    # Calculate the contribution from each of the three corners
    t0 = 0.5 - X0 * X0 - Y0 * Y0
    if t0 < 0:
        n0 = 0.0
    else:
        t0 *= t0
        n0 = t0 * t0 * np.dot(grad2d[gi0], np.array([X0, Y0]))

    t1 = 0.5 - X1 * X1 - Y1 * Y1
    if t1 < 0:
        n1 = 0.0
    else:
        t1 *= t1
        n1 = t1 * t1 * np.dot(grad2d[gi1], np.array([X1, Y1]))

    t2 = 0.5 - X2 * X2 - Y2 * Y2
    if t2 < 0:
        n2 = 0.0
    else:
        t2 *= t2
        n2 = t2 * t2 * np.dot(grad2d[gi2], np.array([X2, Y2]))

    # Add contributions from each corner to get the final noise value.
    # The scaling factor (70.0) is empirical to bring the output into a typical range.
    return 70.0 * (n0 + n1 + n2)

# Example Usage:
if __name__ == "__main__":
    # Generate a 2D noise map
    width, height = 100, 100
    scale = 10.0  # Controls the "zoom" level of the noise
    noise_map = np.zeros((height, width))

    print(f"Generating a {width}x{height} Simplex noise map...")

    for y in range(height):
        for x in range(width):
            # Normalize coordinates to a smaller range for better noise characteristics
            # and scale them to control the frequency of the noise.
            noise_map[y, x] = simplex_noise_2d(x / scale, y / scale)

    print("Noise map generated.")
    print(f"Min noise value: {np.min(noise_map):.4f}")
    print(f"Max noise value: {np.max(noise_map):.4f}")
    print(f"Mean noise value: {np.mean(noise_map):.4f}")

    # You can visualize this noise map using libraries like matplotlib
    try:
        plt.imshow(noise_map, cmap='gray', origin='lower')
        plt.title('2D Simplex Noise')
        plt.colorbar(label='Noise Value')
        plt.show()
    except ImportError:
        print("\nMatplotlib not found. Install it with 'pip install matplotlib' to visualize the noise.")
        print("Here's a small sample of the generated noise values:")
        print(noise_map[:5, :5]) # Print a 5x5 corner of the noise map
