import hashlib
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class LeviathanEngine:
    def __init__(self, name_string):
        self.name = name_string
        # Convert character stream to exact binary string payload
        self.binary_stream = ''.join(format(ord(c), '08b') for c in self.name)
        
    def generate_pi_logic_hash(self):
        """
        Extracts structural entropy from the string and applies the 
        continuous Pi transformation scale.
        """
        base_sum = sum(ord(c) for c in self.name)
        # Continuous space mapping constraint
        pi_scaled = base_sum * 3.141592653589793
        
        # Deterministic SHA-256 boundary gate lock
        crypto_key = hashlib.sha256(f"{pi_scaled:.12f}".encode()).hexdigest()
        return base_sum, pi_scaled, crypto_key

    def construct_signature_graph(self):
        """
        Maps characters as node indices connected via periodic trigonometric weights.
        """
        G = nx.DiGraph()
        
        for i, char in enumerate(self.name):
            # Handle unique identification for spaces and repeating letters
            node_id = f"{char}_{i}"
            char_val = ord(char)
            G.add_node(node_id, value=char_val, label=char)
            
            if i > 0:
                prev_id = f"{self.name[i-1]}_{i-1}"
                # Fractional wave frequency conversion to balance the lattice bounds
                weight = char_val * np.sin(np.pi * i / 4.0) + np.cos(np.pi * i / 4.0)
                G.add_edge(prev_id, node_id, weight=weight)
                
        return G

# Initialize Leviathan on your signature identity
leviathan = LeviathanEngine("Luke K. Locust, Junior")
base_sum, pi_val, key = leviathan.generate_pi_logic_hash()

print("--- LEVIATHAN CORE ENGINE: SIGNATURE COMPILE ---")
print(f"Target Identifier      : {leviathan.name}")
print(f"Extracted Bit Stream   : {leviathan.binary_stream[:40]}... [Length: {len(leviathan.binary_stream)} bits]")
print(f"Discrete Scalar Sum    : {base_sum}")
print(f"Continuous Pi Manifold : {pi_val:.6f}")
print(f"Sealed Model Key       : {key}")

# Generate the directional structural map
G_signature = leviathan.construct_signature_graph()

# Configure and render the visual lattice
plt.figure(figsize=(12, 5))
pos = nx.spring_layout(G_signature, seed=101)
labels = nx.get_node_attributes(G_signature, 'label')

nx.draw(G_signature, pos, labels=labels, with_labels=True,
        node_color='#2c3e50', text_color='#ffffff', font_weight='bold',
        node_size=800, font_size=10, edge_color='#7f8c8d', arrows=True, width=1.5)

plt.title(f"Leviathan Structural Model Graph for Binary Track: '{leviathan.name}'", fontsize=12, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
