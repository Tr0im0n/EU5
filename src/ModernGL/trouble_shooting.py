import moderngl
import sys
import os

print("ModernGL version currently running:", moderngl.__version__)
print("\n--- sys.path ---")
for p in sys.path:
    print(p)
print("----------------")

# Also, try to find where ModernGL thinks it's installed
print(f"ModernGL module location: {moderngl.__file__}")

# Your problematic line will still follow this:
# vao.multi_draw(...)
