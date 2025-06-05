
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def pink_noise(n_octaves=2, degrees_of_freedom=2, seed=2):
    random_generator = np.random.default_rng(seed)
    chi_precursor = random_generator.normal(0., 1., (n_octaves, n_octaves, degrees_of_freedom))
    chi = np.linalg.vector_norm(chi_precursor, axis=2)

    phi = random_generator.uniform(0, 2*np.pi, (n_octaves, n_octaves))
    u1d = np.arange(n_octaves) + 1
    v1d = np.arange(n_octaves) + 1
    v1d.shape = (n_octaves, 1)
    u = np.broadcast_to(u1d, (n_octaves, n_octaves))
    v = np.broadcast_to(v1d, (n_octaves, n_octaves))
    xs = np.arange(0, 1, 0.01)
    ys = np.arange(0, 1, 0.01)

    iter_object = (np.sum(chi / np.sqrt(u*u + v*v) * np.sin(2*np.pi*(u*x + v*y) + phi)) for x in xs for y in ys)
    print("Start the hard part.")
    ans = np.fromiter(iter_object, dtype=np.float32)
    print("Finished the hard part.")
    ans.shape = (100, 100)
    plt.pcolormesh(ans)
    plt.show()


def diamond_square(size_exponent=7, roughness=0.7, seed=2, normalize=True):
    # 1. set some variables WOW
    current_size = np.pow(2, size_exponent)
    size = current_size + 1
    deviation = 1.0     # Initial random displacement magnitude
    roughness_scaling_factor = 2 ** (-roughness)     # The factor by which 'deviation' is reduced each step.
    rng = np.random.default_rng(seed)
    # 2. set Initial map
    heightmap = np.zeros((size, size), dtype=np.float32)
    for i, j in [(0, 0), (0, current_size), (current_size, 0), (current_size, current_size)]:
        heightmap[i, j] = rng.uniform(-1, 1)
    # 3. Main loop: Iteratively refine the grid until squares are 1x1 pixels
    while current_size > 1:
        half_size = current_size // 2
        # 4. Diamond Step
        for x in range(0, size - 1, current_size):
            for y in range(0, size - 1, current_size):
                center_x = x + half_size
                center_y = y + half_size
                diamond_sum = (heightmap[x, y] + heightmap[x + current_size, y] + heightmap[x, y + current_size] +
                               heightmap[x + current_size, y + current_size])
                heightmap[center_x, center_y] = diamond_sum / 4.0 + rng.uniform(-deviation, deviation)
        # 5. Square Step
        for x in range(0, size, half_size):
            for y in range(0, size, half_size):
                # We are looking for the new center points.
                # The way to do that is to loop to all the possible points.
                # Then discard the ones we already have set.
                # This leaves you with the new center points.
                # I have written this comment because I still don't 100% get it.
                if heightmap[x, y] != 0:
                    continue
                # The majority of diamonds only have 3 neighbours.
                total_neighbors_sum = 0.0
                num_neighbors = 0
                if x - half_size >= 0:  # Left neighbor
                    total_neighbors_sum += heightmap[x - half_size, y]
                    num_neighbors += 1
                if x + half_size < size:  # Right neighbor
                    total_neighbors_sum += heightmap[x + half_size, y]
                    num_neighbors += 1
                if y - half_size >= 0:  # Top neighbor
                    total_neighbors_sum += heightmap[x, y - half_size]
                    num_neighbors += 1
                if y + half_size < size:  # Bottom neighbor
                    total_neighbors_sum += heightmap[x, y + half_size]
                    num_neighbors += 1
                # This if statement should be unnecessary, but gemini added it, so I will keep it for now.
                # Chesterton's fence and all.
                if num_neighbors > 0:
                    heightmap[x, y] = total_neighbors_sum / num_neighbors + rng.uniform(-deviation, deviation)
        # 6. Reduce the square size and random displacement for the next iteration
        current_size = half_size
        deviation *= roughness_scaling_factor
    if not normalize:
        return heightmap
    # 7. Normalize the heightmap to a [0, 1] range for better visualization
    min_h, max_h = heightmap.min(), heightmap.max()
    if max_h != min_h:  # Avoid division by zero if all values are identical (unlikely for noise)
        heightmap = (heightmap - min_h) / (max_h - min_h)
    else:  # If all values are the same (e.g., flat terrain), normalize to 0.5
        heightmap = np.full_like(heightmap, 0.5)
    return heightmap


def show_diamond_square(seed=2, save_img=False):
    print("start calc")
    heightmap = diamond_square(seed=seed)
    print("finish calc")
    if save_img:
        uint8_heightmap = (heightmap*255).astype(np.uint8)
        img_grayscale = Image.fromarray(uint8_heightmap, mode='L')
        img_grayscale.save(f"seed_{seed:02}.png")
    title = f"Generated Terrain from seed = {seed}"
    # plt.pcolormesh(heightmap)
    plt.figure(figsize=(10, 10))
    # 'terrain' colormap is good for heightmaps, 'origin='lower' means (0,0) is bottom-left
    plt.imshow(heightmap, cmap='terrain', origin='lower')
    plt.colorbar(label="Height (Normalized)")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def test_norm():
    a = np.arange(24) + 1
    a.shape = (2, 3, 4)
    b = a*a
    c = np.sum(b)
    d = np.sqrt(c)

    e = np.linalg.vector_norm(a, axis=0)
    f = np.linalg.vector_norm(a, axis=1)
    g = np.linalg.vector_norm(a, axis=2)

    my_list = [a, b, c, d, e, f, g]

    print(*my_list, sep="\n")


if __name__ == "__main__":
    # test_norm()
    # pink_noise(6, 3, 3)
    show_diamond_square(5, False)




"""

Good seeds: 5, 2, 0


"""



