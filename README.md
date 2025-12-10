# Smart Grid Simulator

A smart electric grid simulator developed in C++ with a PyQt GUI.

## Functionalities

- Energy Producers/Consumers Simulation
- Dynamique managements of the batteries
- GUI in PyQt
- Modularity and extensibility (A vérifier)

*TODO:* Mettre une image

## Getting Started

### Prerequistes

- C++17 or higher
- CMake ≥ 3.10
- Python 3.8+ (for the PyQt GUI)

### Installation

#### 1. Clone the repo

```bash
git clone https://github.com/Remi971/SmartGridSimulator.git
```

#### 2. Compilation (C++)

Into the project folder follow those instructions :

```bash
mkdir build && cd build
cmake ..
make
```

#### 3. Launch the GUI (Python)

```bash
cd python
pip -m venv .venv
pip -m install -r requirements.txt
python python/app.py
```

## Example

Use case of the application.

## Authors

**Rémi Bhagalou** - *Initial work* - [Github](https://github.com/Remi971)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details

## Acknowledgments

Ideal for educational purposes, energy system prototyping, or smart grid research.
