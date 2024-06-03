# Wave Propagation Simulation

This repository contains code and simulations for various aspects of wave propagation analysis, including computational time analysis for FFTs, precision comparison, and solving pentadiagonal systems for radiowave propagation. The repository is structured into four main folders:

## Folder Structure

### 1. FFT_CPU_Computational_time
This folder contains code for analyzing the computational time of Fast Fourier Transforms (FFTs) based on system size. The results of this analysis are included in the appendix of the report.

#### Requirements:
- FFTW
- Eigen

### 2. FloatVsDouble
This folder contains code for comparing the use of single precision floats versus doubles in wave propagation simulations. The results of this comparison are excluded from the report.

#### Requirements:
- CUDA
- Eigen

### 3. PentaSolver_test
This folder contains code for simulations based on solving a pentadiagonal system for radiowave propagation. The results of these simulations are displayed in the report.

#### Requirements:
- CUDA
- Eigen

### 4. wavepropagation_simulation
This folder contains the main part of the code based on Levy's book for parabolic equation modelling. The main script runs the tests displayed in the report, but individual tests can also be run using the input arguments `--test1`, `--test2`, `--test3`, `--test4`, or `--test5`.

#### Requirements:
- CUDA
- FFTW
- Eigen

## Getting Started

### Prerequisites
Ensure you have the following libraries installed:

#### FFTW Installation
```bash
# On Ubuntu
sudo apt-get update
sudo apt-get install fftw3 fftw3-dev

# On macOS using Homebrew
brew install fftw
```

#### Eigen Installation
```bash
# On Ubuntu
sudo apt-get install libeigen3-dev

# On macOS using Homebrew
brew install eigen
```

#### CUDA Installation
Follow the instructions on the official [NVIDIA CUDA Toolkit website](https://developer.nvidia.com/cuda-downloads) to download and install CUDA for your operating system.

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install the required libraries for each folder as specified above.

### Running the Code
Navigate to the respective folder and follow the instructions to run the simulations or analyses.

#### Example:
To run the main wave propagation simulation:
```bash
cd wavepropagation_simulation/build
./bin/performance_test_v2 --test1
```

## Folder Details

### FFT_CPU_Computational_time
This folder includes scripts and functions to measure and analyze the computational time required for performing FFTs of varying system sizes.

### FloatVsDouble
This folder contains comparative studies on the performance and accuracy of single precision floats versus double precision in wave propagation simulations.

### PentaSolver_test
In this folder, you'll find simulations that solve pentadiagonal systems, a critical part of the radiowave propagation analysis. The results are documented in the report.

### wavepropagation_simulation
This is the core part of the project, implementing parabolic equation modelling for wave propagation as described in Levy's book. The main script allows for running different tests which are specified in the report.
