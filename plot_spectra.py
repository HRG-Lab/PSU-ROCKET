#! /usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("Test Spectra.csv")

fig = plt.figure(figsize=(10, 6))

plt.plot(data['wavelen (nm)'], data['CIE F11 Fluor'], 'b', linewidth=3,
         label="CIE F11 Fluor")

plt.plot(data['wavelen (nm)'], data['LEDCube-11'], 'r', linewidth=3,
         label="LEDCube-11")

plt.title("Test Spectra", fontsize=22)
plt.xlabel("Wavelength [nm]", fontsize=18)
plt.ylabel("Relative magnitude", fontsize=18)
plt.grid(True, which="both")
plt.legend(fontsize=16)

plt.savefig("test_spectra.png")
