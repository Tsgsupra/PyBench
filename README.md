# PyBench
PyBench is an opensource GPU CPU Benchmark Tool using psutil, pillow, pygame and python. It writes 30MB of data to the folder where the app is located. It reads it and deletes it. It executes 250000 floating point operations p/sec(Mostly Trig problems). It spawns 550 circles of random color, shape, and size and applies a Gaussian Blur to them. Goto Readme
Once the target threshold is reached of circles, it deletes them at a 6 p/sec rate while moving them, and doing all of the other calculations and read/write tests at the same time. It repeats this 2 times. The python console gives you all of the details you would need to know.

IMPORTANT!!!
YOU NEED ALL OF THE LIBRARYS LISTED ABOVE. YOU CAN RUN "PIP INSTALL PILLOW" && "PIP INSTALL PSUTIL" && "PIP INSTALL PYGAME" TO INSTALL THEM. IF YOU HAVE LESS THAN 500MB OF STORAGE, DO NOT RUN THIS. IF YOU HAVE LESS THAN 1GB OF MEMORY, DO NOT RUN THIS. MAKE SURE TO NEVER UNPLUG THE COMPUTER OR TURN IT OFF. THE WRITING TO THE DISK COULD OVERWRITE IMPORTANT SYSTEM FILES IF YOU TURN OFF THE COMPUTER. 

Where to install Python: Python.org/Downloads

If you wish to contribute, fork the project and submit a pull request once done. Copying the repository doesn't help. 

Download PyBench.py, and install all libs, then put PyBench in a folder called PyBench and run. This Program was made for x64 computers.

Made with love from TSG.
