import numpy as np

float64 = np.sin(2)
float = np.float64(float64).item()

print(str(type(float64)))
print(str(type(float)))

np.arccos(-1.01)