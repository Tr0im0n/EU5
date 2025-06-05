import numpy as np
import matplotlib.pyplot as plt

"""
Written by: GEMINI
"""


class PerlinNoise2D:
    """
    Generates 2D Perlin Noise.
    Based on Ken Perlin's Improved Perlin Noise (2002).
    """

    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

        # Permutation table: A shuffled array of 0-255, duplicated to 512 for convenience
        # This is used to hash coordinates into indices for the gradient vectors.
        self.p = np.arange(256, dtype=int)
        self.rng.shuffle(self.p)
        self.p = np.stack([self.p, self.p]).flatten()  # Duplicate for faster modulo operations

        # Pre-defined 2D gradient vectors. These are 8 unit vectors or similar.
        # Perlin's original used (x,y) where x,y are from {-1, 0, 1} and not (0,0).
        # A common set (more efficient, avoids sqrt) are vectors to corners and mid-sides.
        self.gradients = np.array([
            [1, 1], [-1, 1], [1, -1], [-1, -1],
            [1, 0], [-1, 0], [0, 1], [0, -1]
        ], dtype=float)  # Note: These are not normalized, which is fine for gradient noise.

    def _fade(self, t):
        """
        Perlin's smoothstep function (6t^5 - 15t^4 + 10t^3).
        Ensures zero first and second derivatives at t=0 and t=1,
        preventing harsh grid artifacts.
        """
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a, b, t):
        """
        Linear interpolation.
        """
        return a + t * (b - a)

    def _get_gradient(self, hash_value):
        """
        Retrieves a gradient vector based on a hash value from the permutation table.
        """
        return self.gradients[hash_value % 8]  # % 8 because we have 8 distinct gradient vectors

    def noise(self, x, y):
        """
        Calculates the Perlin noise value for a given (x, y) coordinate.
        """
        # Determine grid cell coordinates
        xi = int(np.floor(x)) & 255  # & 255 (or % 256) maps to 0-255 for permutation table
        yi = int(np.floor(y)) & 255

        # Determine fractional parts of coordinates
        xf = x - np.floor(x)
        yf = y - np.floor(y)

        # Apply Perlin's fade curve to fractional parts
        u = self._fade(xf)
        v = self._fade(yf)

        # Get hash values for the 4 corners of the grid cell
        # (xi, yi), (xi+1, yi), (xi, yi+1), (xi+1, yi+1)
        aaa = self.p[self.p[xi] + yi]  # (0,0) corner
        aba = self.p[self.p[xi] + yi + 1]  # (0,1) corner
        baa = self.p[self.p[xi + 1] + yi]  # (1,0) corner
        bba = self.p[self.p[xi + 1] + yi + 1]  # (1,1) corner

        # Get gradient vectors for each corner
        grad_aaa = self._get_gradient(aaa)
        grad_aba = self._get_gradient(aba)
        grad_baa = self._get_gradient(baa)
        grad_bba = self._get_gradient(bba)

        # Calculate distance vectors from each corner to the point (xf, yf)
        v_aaa = np.array([xf, yf])
        v_aba = np.array([xf, yf - 1])
        v_baa = np.array([xf - 1, yf])
        v_bba = np.array([xf - 1, yf - 1])

        # Calculate dot products between gradient vectors and distance vectors
        # This projects the point's position onto the corner's gradient
        val_aaa = np.dot(grad_aaa, v_aaa)
        val_aba = np.dot(grad_aba, v_aba)
        val_baa = np.dot(grad_baa, v_baa)
        val_bba = np.dot(grad_bba, v_bba)

        # Interpolate along X axis
        x1 = self._lerp(val_aaa, val_baa, u)  # Interpolate between (0,0) and (1,0) projections
        x2 = self._lerp(val_aba, val_bba, u)  # Interpolate between (0,1) and (1,1) projections

        # Interpolate along Y axis
        # The final noise value is typically in the range [-1, 1]
        return self._lerp(x1, x2, v)

    def generate_2d_noise(self, width, height, frequency=16.0, normalize=True):
        """
        Generates a 2D array of Perlin noise.

        Args:
            width (int): The width of the output array.
            height (int): The height of the output array.
            frequency (float): How "zoomed in" the noise is. Higher frequency means more detail.
            normalize (bool): If True, normalize the output to the [0, 1] range.

        Returns:
            np.ndarray: A 2D NumPy array containing the Perlin noise values.
        """
        noise_map = np.zeros((height, width), dtype=np.float32)

        # Iterate over each pixel and calculate its noise value
        for y in range(height):
            for x in range(width):
                # Scale x, y by frequency to control zoom level
                noise_map[y, x] = self.noise(x / frequency, y / frequency)

        if normalize:
            # Normalize to [0, 1] for typical image display
            min_val = noise_map.min()
            max_val = noise_map.max()
            if max_val != min_val:
                noise_map = (noise_map - min_val) / (max_val - min_val)
            else:  # Handle flat noise (e.g., if frequency is too low for a small image)
                noise_map = np.full_like(noise_map, 0.5)  # Set to mid-gray

        return noise_map


# --- Example Usage ---
if __name__ == "__main__":
    # --- Parameters for noise generation ---
    image_width = 512
    image_height = 512

    # Frequency: Higher values make the noise "busier" or more detailed
    # Lower values make it smoother, like hills
    noise_frequency = 128.0

    # Seed for reproducibility
    noise_seed = 42

    # --- Generate and plot the noise ---
    print(f"Generating {image_width}x{image_height} Perlin noise with frequency {noise_frequency}...")
    perlin_gen = PerlinNoise2D(seed=noise_seed)
    perlin_map = perlin_gen.generate_2d_noise(image_width, image_height, frequency=noise_frequency)

    plt.figure(figsize=(8, 8))
    plt.imshow(perlin_map, cmap='terrain', origin='lower')  # 'gray' colormap for noise
    plt.colorbar(label="Noise Value (Normalized)")
    plt.title(f"2D Perlin Noise ({image_width}x{image_height}, Freq: {noise_frequency}, Seed: {noise_seed})")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

    # --- Experiment with different frequencies ---
    # perlin_gen_low_freq = PerlinNoise2D(seed=100)
    # perlin_map_low = perlin_gen_low_freq.generate_2d_noise(image_width, image_height, frequency=5.0)
    # plt.figure(figsize=(8, 8))
    # plt.imshow(perlin_map_low, cmap='gray', origin='lower')
    # plt.title("Low Frequency Perlin Noise (Freq: 5.0)")
    # plt.show()

    # perlin_gen_high_freq = PerlinNoise2D(seed=100)
    # perlin_map_high = perlin_gen_high_freq.generate_2d_noise(image_width, image_height, frequency=100.0)
    # plt.figure(figsize=(8, 8))
    # plt.imshow(perlin_map_high, cmap='gray', origin='lower')
    # plt.title("High Frequency Perlin Noise (Freq: 100.0)")
    # plt.show()