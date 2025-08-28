import streamlit as st
import numpy as np
import plotly.graph_objs as go

# --- Custom CSS for Attractive UI ---
st.markdown('''
    <style>
    body, .stApp { background: linear-gradient(135deg,#181c2f 0%,#232946 100%) !important; color:#f3f6fa; }
    .stApp { font-family: 'Segoe UI', Arial, sans-serif; }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffb800 !important;
        text-shadow: 0 2px 16px #000a, 0 1px 0 #fff2;
        letter-spacing: 1.2px;
    }
    .stSidebar, .st-cg, .st-bb, .st-bf, .st-b8, .st-b7 {
        background: rgba(36,40,62,.95) !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 32px #0004, 0 1.5px 4px #0002 !important;
        border: 1.5px solid #2e335a !important;
    }
    .stButton>button, .stButton>button:focus {
        background: linear-gradient(90deg,#ffb800 0%,#ff6b6b 100%) !important;
        color: #232946 !important;
        font-weight: 700;
        border-radius: 8px;
        box-shadow: 0 2px 12px #ffb80033, 0 1.5px 4px #0002;
        border: none;
        transition: background .2s, box-shadow .2s, transform .1s;
        outline: none;
        width: 100% !important;
        min-width: 210px;
        max-width: 100%;
        padding: 14px 0 !important;
        margin-bottom: 14px !important;
        display: block;
        font-size: 1.18em !important;
        letter-spacing: 0.5px;
    }
    label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stSidebar label {
        font-size: 1.18em !important;
        color: #ffb800 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 8px !important;
        display: block !important;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg,#ff6b6b 0%,#ffb800 100%) !important;
        box-shadow: 0 4px 24px #ffb80055, 0 2px 8px #0003;
        transform: translateY(-2px) scale(1.03);
    }
    .stButton>button:active {
        background: linear-gradient(90deg,#ffb800 0%,#ff6b6b 100%) !important;
        box-shadow: 0 1px 2px #ffb80033;
        transform: translateY(1px) scale(.98);
    }
    .stCodeBlock, .stCodeBlock pre, .stCodeBlock code {
        background: rgba(36,40,62,.95) !important;
        color: #ffb800 !important;
        border-radius: 12px !important;
        border: 1.5px solid #2e335a !important;
        box-shadow: 0 2px 12px #0002 !important;
        font-family: 'Fira Mono', 'Consolas', monospace !important;
        font-size: 1.05em !important;
    }
    .stSelectbox>div>div, .stTextInput>div>div, .stNumberInput>div>div {
        background: #232946 !important;
        color: #f3f6fa !important;
        border-radius: 8px !important;
        border: 1.5px solid #2e335a !important;
        font-size: 17px !important;
    }
    .stSelectbox>div>div:focus, .stTextInput>div>div:focus, .stNumberInput>div>div:focus {
        border: 1.5px solid #ffb800 !important;
        box-shadow: 0 0 0 2px #ffb80044 !important;
    }
    .stInfo, .stAlert {
        background: rgba(36,40,62,.95) !important;
        color: #ffb800 !important;
        border-radius: 12px !important;
        border: 1.5px solid #2e335a !important;
        box-shadow: 0 2px 12px #0002 !important;
    }
    </style>
''', unsafe_allow_html=True)

# --- Quantum Gate Definitions ---
SQRT1_2 = 1 / np.sqrt(2)
GATES = {
    'h': np.array([[SQRT1_2, SQRT1_2], [SQRT1_2, -SQRT1_2]], dtype=complex),
    'x': np.array([[0, 1], [1, 0]], dtype=complex),
    'y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'z': np.array([[1, 0], [0, -1]], dtype=complex),
    'i': np.eye(2, dtype=complex)
}

# --- Helper Functions ---
def gate_matrix(type):
    return GATES.get(type, GATES['i'])

def apply_gate(state, target, control, U, n):
    N = len(state)
    tMask = 1 << (n - 1 - target)
    cMask = (1 << (n - 1 - control)) if control is not None else 0
    out = state.copy()
    for i in range(N):
        if (i & tMask) != 0:
            continue
        j = i ^ tMask
        controlOn = True if control is None else ((i & cMask) != 0)
        if controlOn:
            a, b = state[i], state[j]
            out[i] = U[0, 0] * a + U[0, 1] * b
            out[j] = U[1, 0] * a + U[1, 1] * b
    return out

def reduced_density(state, qubit, n):
    N = 1 << n
    kMask = 1 << (n - 1 - qubit)
    rho = np.zeros((2, 2), dtype=complex)
    for i in range(N):
        for j in range(N):
            if (i & ~kMask) == (j & ~kMask):
                ii = 1 if (i & kMask) else 0
                jj = 1 if (j & kMask) else 0
                rho[ii, jj] += state[i] * np.conj(state[j])
    return rho

def bloch_from_rho(rho):
    c = rho[0, 1]
    x = 2 * np.real(c)
    y = -2 * np.imag(c)
    z = np.real(rho[0, 0] - rho[1, 1])
    return np.array([x, y, z])

def create_bloch_sphere(x, y, z, qubit_idx):
    # Sphere surface
    u, v = np.mgrid[0:np.pi:31j, 0:2 * np.pi:31j]
    xs = np.sin(u) * np.cos(v)
    ys = np.sin(u) * np.sin(v)
    zs = np.cos(u)
    sphere = go.Surface(
        x=xs, y=ys, z=zs, opacity=0.18,
        colorscale=[[0, '#ffb800'], [1, '#6b6bff']], showscale=False,
        lighting=dict(ambient=0.7, diffuse=0.8, specular=0.5, roughness=0.5, fresnel=0.2),
        lightposition=dict(x=2, y=2, z=2), hoverinfo='skip', name='Sphere'
    )
    # Bloch vector
    arrow = go.Scatter3d(
        x=[0, 0.9 * x], y=[0, 0.9 * y], z=[0, 0.9 * z],
        mode='lines+markers', line=dict(width=8, color='#ff6b6b'),
        marker=dict(size=6, color='#ffb800'), name='State'
    )
    # Axes
    axes = [
        go.Scatter3d(x=[-1.1, 1.1], y=[0, 0], z=[0, 0], mode='lines', line=dict(width=2, color='#bfcbe6'), showlegend=False),
        go.Scatter3d(x=[0, 0], y=[-1.1, 1.1], z=[0, 0], mode='lines', line=dict(width=2, color='#bfcbe6'), showlegend=False),
        go.Scatter3d(x=[0, 0], y=[0, 0], z=[-1.1, 1.1], mode='lines', line=dict(width=2, color='#bfcbe6'), showlegend=False)
    ]
    layout = go.Layout(
        title=f'Qubit {qubit_idx}',
        scene=dict(
            xaxis=dict(title='X', range=[-1.2, 1.2], backgroundcolor='#232946', gridcolor='#444a6d', zerolinecolor='#ffb800'),
            yaxis=dict(title='Y', range=[-1.2, 1.2], backgroundcolor='#232946', gridcolor='#444a6d', zerolinecolor='#ffb800'),
            zaxis=dict(title='Z', range=[-1.2, 1.2], backgroundcolor='#232946', gridcolor='#444a6d', zerolinecolor='#ffb800'),
            aspectmode='cube', camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='rgba(36,40,62,0.95)',
        plot_bgcolor='rgba(36,40,62,0.95)'
    )
    fig = go.Figure(data=[sphere, arrow] + axes, layout=layout)
    return fig

def simulate_circuit(qubits, gates):
    n = qubits
    dim = 1 << n
    sv = np.zeros(dim, dtype=complex)
    sv[0] = 1.0
    for g in gates:
        U = gate_matrix(g['type'])
        sv = apply_gate(sv, g['target'], g['control'], U, n)
    return sv

def display_density_matrices(state, qubits):
    def fmt_num(val):
        a = 0.0 if abs(np.real(val)) < 1e-8 else np.real(val)
        b = 0.0 if abs(np.imag(val)) < 1e-8 else np.imag(val)
        if b == 0.0:
            return f"{a:.4f}"
        return f"{a:.4f}{'+' if b >= 0 else ''}{b:.4f}j"

    out = 'Full State Vector:\n[' + ', '.join([fmt_num(a) for a in state]) + ']\n\nReduced Density Matrices & Bloch Vectors:'
    for i in range(qubits):
        rho = reduced_density(state, i, qubits)
        x, y, z = bloch_from_rho(rho)
        # Format as a normal 2x2 matrix, one row per line
        rho_str = (
            f"[{fmt_num(rho[0,0])}, {fmt_num(rho[0,1])}]\n"
            f"[{fmt_num(rho[1,0])}, {fmt_num(rho[1,1])}]"
        )
        out += f"\n\nQubit {i} ρ:\n{rho_str}\nBloch: [{fmt_num(x)}, {fmt_num(y)}, {fmt_num(z)}]"
    return out

# --- Streamlit UI ---
st.set_page_config(page_title="Quantum Circuit Bloch Visualization", layout="wide")
st.title("Quantum Circuit Bloch Sphere Visualization")

if 'circuit' not in st.session_state:
    st.session_state.circuit = {'qubits': 4, 'gates': []}

circuit = st.session_state.circuit

with st.sidebar:
    st.header("Circuit Configuration")
    qubits = st.selectbox("Number of Qubits", [1,2,3,4,5,6], index=3)
    gate_type = st.selectbox("Gate Type", ["h", "x", "y", "z"])
    target = st.selectbox("Target Qubit", list(range(qubits)), format_func=lambda x: f"Qubit {x}")
    control = st.selectbox("Control Qubit (optional)", ["None"] + list(range(qubits)), format_func=lambda x: f"Qubit {x}" if x != "None" else "None")
    add_gate = st.button("Add Gate to Circuit")
    undo_gate = st.button("Undo Last Gate")
    run_circuit = st.button("Run Circuit & Visualize")
    reset_circuit = st.button("Reset Circuit")

if qubits != circuit['qubits']:
    circuit['qubits'] = qubits
    circuit['gates'] = []

if add_gate:
    ctrl = None if control == "None" else int(control)
    if ctrl is not None and ctrl == target:
        st.warning("Control and target must be different")
    else:
        circuit['gates'].append({'type': gate_type, 'target': target, 'control': ctrl})

if undo_gate and circuit['gates']:
    circuit['gates'].pop()

if reset_circuit:
    circuit['gates'] = []


# --- Main Layout ---
st.subheader("Circuit Diagram")
diagram = ""
for q in range(circuit['qubits']):
    diagram += f"Qubit {q}: "
    for g in circuit['gates']:
        is_cnot = g['type'] == 'x' and g['control'] is not None
        if is_cnot and g['control'] == q:
            diagram += "●──"
        elif g['target'] == q:
            diagram += "⊕──" if is_cnot else f"[{g['type'].upper()}]──"
        else:
            diagram += "───"
    diagram += "\n"
st.code(diagram)

st.subheader("Bloch Sphere Visualization")
if st.button("Show Bloch Spheres") or run_circuit:
    state = simulate_circuit(circuit['qubits'], circuit['gates'])
    cols = st.columns(min(3, circuit['qubits']))
    for i in range(circuit['qubits']):
        rho = reduced_density(state, i, circuit['qubits'])
        x, y, z = bloch_from_rho(rho)
        with cols[i % len(cols)]:
            st.plotly_chart(create_bloch_sphere(x, y, z, i), use_container_width=True)
    st.subheader("Reduced Density Matrices")
    st.code(display_density_matrices(state, circuit['qubits']))
else:
    st.info("Click 'Show Bloch Spheres' or 'Run Circuit & Visualize' to see results.")


import streamlit as st

# --- Initialize chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "new_message" not in st.session_state:
    st.session_state.new_message = ""

# --- Simple FAQ Knowledge Base ---
faq = {
    "qubit": "A qubit is the quantum version of a bit. It can exist in superpositions of |0> and |1>.",
    "bloch": "The Bloch sphere is a 3D representation of a single qubit's quantum state.",
    "h": "Hadamard (H) gate creates a superposition state from |0> or |1>.",
    "x": "Pauli-X gate flips a qubit state (like a NOT gate).",
    "y": "Pauli-Y gate rotates around Y-axis and adds a phase flip.",
    "z": "Pauli-Z gate flips the phase of |1> while leaving |0> unchanged.",
    "cnot": "Controlled-NOT flips the target qubit only if the control qubit is |1>.",
    "visualizer": "This app simulates quantum circuits and shows Bloch sphere visualizations.",
    "gate": "Quantum gates manipulate qubit states, similar to logic gates in classical computing.",
    "density matrix": "A density matrix describes the statistical state of a quantum system, useful for mixed states.", 
    "superposition": "Superposition allows a qubit to be in multiple states simultaneously until measured.",
    "entanglement": "Entanglement is a quantum phenomenon where qubits become correlated such that the state of one instantly influences the other, regardless of distance.",
    "measurement": "Measurement collapses a qubit's superposition to a definite state of |0> or |1>.",
    "control qubit": "A control qubit determines whether a quantum gate is applied to a target qubit in controlled operations like CNOT.",
    "target qubit": "A target qubit is the qubit that a quantum gate acts upon, potentially influenced by a control qubit.",
    "quantum circuit": "A quantum circuit is a sequence of quantum gates applied to qubits to perform computations.",   
    "quantum computing": "Quantum computing leverages quantum mechanics to perform computations that can be more efficient than classical methods for certain problems.",
    "quantum gate": "A quantum gate is a basic operation that changes the state of  qubits, analogous to logic gates in classical computing.",
    "quantum state": "A quantum state represents the state of a quantum system, often described by a wavefunction or state vector.",
    "visualization": "Visualization helps in understanding complex quantum states and operations through graphical representations like the Bloch sphere.",     
    "mixed state": "A mixed state is a statistical mixture of different quantum states, represented by a density matrix, as opposed to a pure state which is described by a single state vector.",  
    "pure state": "A pure state is a quantum state that can be described by a single state vector, representing maximum knowledge about the system, unlike a mixed state which is a statistical mixture of states.",    
    "full state vector": "The full state vector describes the complete quantum state of a multi-qubit system, encompassing all possible configurations and their amplitudes.",  
    "reduced density matrix": "A reduced density matrix is obtained by tracing out part of a larger quantum system, providing a description of a subsystem's state.",  
    "quantum simulation": "Quantum simulation involves using classical or quantum computers to model the behavior of quantum systems, aiding in understanding and predicting their properties.",  
    "quantum algorithm": "A quantum algorithm is a step-by-step procedure designed to run on a quantum computer, often exploiting quantum phenomena like superposition and entanglement to solve problems more efficiently than classical algorithms.", 
    "hii": "Hello! How can I assist you with quantum computing today?   🙂"     ,
    "hello": "Hi there! Feel free to ask me anything about quantum computing.   🙂",
    "bloch sphere": "The Bloch sphere is a 3D representation of a single qubit's quantum state.",
    "quantum": "Quantum computing leverages quantum mechanics to perform computations that can be more efficient than classical methods for certain problems.",
    "help": "I'm here to help! Ask me about qubits, gates, or the Bloch sphere.",
    "Thanks": "You're welcome! If you have more questions, just ask.   🙂",
    "process":" Quantum computing uses qubits and quantum gates to perform operations that can solve certain problems faster than classical computers.",

}

def chatbot_answer(user_input: str) -> str:
    text = user_input.lower()
    for key, ans in faq.items():
        if key in text:
            return ans
    return "I'm not sure 🤔. Try asking about qubits, gates, or the Bloch sphere."

with st.sidebar:
    st.markdown("## 🤖 Quantum Assistant")

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(
                f"<div style='text-align:right; "
                f"background-color:#dbeafe; color:#111; padding:8px; "
                f"border-radius:10px; margin:4px;'><b>You:</b> {msg}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align:left; "
                f"background-color:#f3f4f6; color:#111; padding:8px; "
                f"border-radius:10px; margin:4px;'><b>Bot:</b> {msg}</div>",
                unsafe_allow_html=True
            )

    st.session_state.new_message = st.text_input("Ask me about qubits...this chatbot not trained well.....", value=st.session_state.new_message)

    if st.button("Send"):
        user_input = st.session_state.new_message.strip()
        if user_input:
            reply = chatbot_answer(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))
            st.session_state.new_message = ""   
            st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.new_message = ""
        st.rerun()
    
    
