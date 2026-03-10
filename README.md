
# ⚛️ Project-Q

### Interactive Quantum State Visualizer

Project-Q is an interactive web-based visualization tool designed to help students and developers understand **quantum computing concepts through visual representations of quantum states**.

The application allows users to visualize how **qubits evolve under quantum gates**, observe **superposition and phase changes**, and explore quantum states using intuitive graphical interfaces.

This project aims to make **quantum mechanics and quantum computing concepts easier to understand through visual simulation**.

---

# 🎯 Objective

Quantum computing concepts are often difficult to understand because they rely heavily on mathematical representations such as complex amplitudes and probability distributions.

Project-Q solves this by providing:

* Visual representation of **quantum states**
* Interactive simulation of **quantum gates**
* Graphical demonstration of **qubit transformations**
* Educational tools for **learning quantum mechanics**

---

# ✨ Features

## 🔹 Quantum State Visualization

Visualizes qubit states in a graphical format, helping users understand:

* Superposition
* Probability amplitudes
* Phase information

---

## 🔹 Bloch Sphere Representation

Displays the quantum state on a **Bloch Sphere**, which is commonly used to represent single qubit states.

Users can observe how different quantum gates rotate the qubit on the sphere.

---

## 🔹 Quantum Gate Simulation

Supports simulation of common quantum gates:

* **Hadamard (H)**
* **Pauli-X**
* **Pauli-Y**
* **Pauli-Z**
* **Phase Gate**
* **Rotation Gates**

Each gate transforms the qubit state in real time.

---

## 🔹 Interactive UI

The interface allows users to:

* Apply quantum gates
* Reset quantum states
* Observe state transitions
* Experiment with quantum operations

---

# 🧠 Quantum Concepts Demonstrated

Project-Q visually demonstrates several key quantum computing concepts:

### Qubit

A quantum bit that can exist in a **superposition of |0⟩ and |1⟩ states**.

### Superposition

Unlike classical bits, qubits can exist in multiple states simultaneously.

### Phase

The relative phase between amplitudes affects interference patterns.

### Measurement

Observing a quantum state collapses it into a classical value.

---

# 🏗 System Architecture

```text
User Interface
     │
     ▼
Quantum Gate Controls
     │
     ▼
Quantum State Engine
(State Vector Simulation)
     │
     ▼
Visualization Engine
(Bloch Sphere / Graphs)
     │
     ▼
Rendering Layer
(Canvas / WebGL)
```

---

# 🛠 Tech Stack

### Programming Laanguage

* Python

### WEB Framework

* Streamlit

### Scientific Computing

* Numpy

### Visualization

* Plotly (3D Bloch Sphere)
* Quantum state rendering logic

### Development Tools

* Git
* GitHub

---

# 📂 Project Structure

```text
Project-Q
│
├── src
│   ├── components
│   │   ├── BlochSphere
│   │   ├── QuantumControls
│   │   └── StateVisualizer
│   │
│   ├── pages
│   │   └── Home
│   │
│   ├── utils
│   │   └── quantumMath.ts
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── public
│
├── package.json
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Syamkumar-I/Project-Q.git
```

Navigate into the project folder:

```bash
cd Project-Q
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

The project will run locally at:

```
http://localhost:5173
```

---

# 🧪 Example Usage

1. Open the application.
2. Initialize a qubit in the **|0⟩ state**.
3. Apply a **Hadamard gate**.
4. Observe the qubit move into **superposition** on the Bloch sphere.
5. Apply additional gates to observe state evolution.

---

# 📚 Educational Use Cases

Project-Q can be used for:

* Learning **quantum computing basics**
* Teaching **quantum mechanics visually**
* Demonstrating **quantum gate operations**
* Understanding **Bloch sphere transformations**

---

# 🚀 Future Improvements

Planned enhancements include:

* Multi-qubit visualization
* Quantum circuit builder
* Entanglement simulation
* Quantum algorithm demonstrations
* Measurement probability graphs
* Exportable simulation states

---

# 👨‍💻 Team

Developed for **Amaravathi Quantum Valley Hackathon(AQVH)**

Team Members:

* Syam Kumar
* Ismail
* Drakshayani
* Pushpa
* Shabena
* Akhila

---

# 👨‍💻 Author

**Syam Kumar**

GitHub
[https://github.com/Syamkumar-I](https://github.com/Syamkumar-I)

---
