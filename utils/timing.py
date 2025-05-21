
import time


# Timing function to compare two functions GROK
def compare_function_speed(func1, func2, args, func1_name="Function 1", func2_name="Function 2"):
    # Run in ABAB order
    times = []

    # Run func1 first time
    start = time.perf_counter()
    func1(*args)
    times.append(time.perf_counter() - start)

    # Run func2 first time
    start = time.perf_counter()
    func2(*args)
    times.append(time.perf_counter() - start)

    # Run func1 second time
    start = time.perf_counter()
    func1(*args)
    times.append(time.perf_counter() - start)

    # Run func2 second time
    start = time.perf_counter()
    func2(*args)
    times.append(time.perf_counter() - start)

    # Print results
    print(f"{func1_name} (Run 1): {times[0]:.6f} seconds")
    print(f"{func2_name} (Run 1): {times[1]:.6f} seconds")
    print(f"{func1_name} (Run 2): {times[2]:.6f} seconds")
    print(f"{func2_name} (Run 2): {times[3]:.6f} seconds")
    print(f"Average {func1_name}: {(times[0] + times[2]) / 2:.6f} seconds")
    print(f"Average {func2_name}: {(times[1] + times[3]) / 2:.6f} seconds")












