# Smart Grid Simulator

A smart electric grid simulator developed in C++ with a PyQt GUI.

## Functionalities

- Energy Producers/Consumers Simulation
- Dynamique managements of the batteries
- GUI in PyQt
- Modularity and extensibility (A vérifier)

*TODO:* Mettre une image

## Pre-request (A vérifier)

- C++17 or higher
- CMake ≥ 3.10
- Python 3.8+ (for the PyQt GUI)

### Compilation (C++)

```bash
mkdir build && cd build
cmake ..
make
```

### Launch the GUI (Python)

```bash
cd python
pip -m venv .venv
pip -m install -r requirements.txt
python python/app.py
```
