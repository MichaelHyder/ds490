import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import pandas as pd
import numpy as np



def cdf(array,i):
        ans = 0
        for pdf in array[i:]:
            ans += pdf
        
        return ans

def Theta(distribution,type_space,i):
    f= np.array(distribution)
    t= np.array(type_space)
    virt_val = t[0]/f[0]
    if i == 0:
        return virt_val
    else:
        return ((t[i]-t[i-1])*cdf(f, i))/f[i]

def Virtual_Values(distribution, type_space):
    
    virt_values = np.array([])
    for i in range(len(distribution)):
        virt_values = np.append(virt_values, Theta(distribution, type_space, i))
        
    return virt_values


class InteractiveGraph:
    def __init__(self, G, positions):
        self.G = G
        self.positions = positions
        self.node_list = list(self.G.nodes) 
        self.adjacency_matrix = self.create_adjacency_matrix() 
        self.selected_node = None
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.omega_values = self.compute_omega_values()
        self.draw_graph()

        # Connect event handlers
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def draw_graph(self):
        """Draws the graph with edge weights."""

        self.ax.set_position([0.05, 0.05, 0.65, 0.9])

        self.ax.clear()
        nx.draw(
            self.G,
            pos=self.positions,
            with_labels=True,
            ax=self.ax,
            node_size=500,
            node_color="black",
            font_color="white"
        )
        # Draw edge labels for weights
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(
            self.G,
            pos=self.positions,
            edge_labels=edge_labels,
            ax=self.ax,
            font_color="red"
        )

       
        omega_df = pd.DataFrame(self.omega_values, columns=["Node", "Virtual Value"])
        table_ax = self.fig.add_axes([0.72, 0.2, 0.25, 0.6])  # [left, bottom, width, height]
        table_ax.axis("off")
        table = table_ax.table(
            cellText=omega_df.values,
            colLabels=omega_df.columns,
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)


        self.fig.canvas.draw()

    def compute_omega_values(self):
        """Compute omega values dynamically based on graph's adjacency matrix."""
        omega_values = [(node, round(np.sum(self.adjacency_matrix[idx]), 4)) for idx, node in enumerate(self.G.nodes)]
        return omega_values

    def update_omega_values(self):
        """Update omega values after a graph modification."""
        self.omega_values = self.compute_omega_values()
        self.draw_graph()

    def create_adjacency_matrix(self):
        """Creates and returns the adjacency matrix for the graph."""
        # Generate the adjacency matrix as a dense NumPy array
        sparse_matrix = nx.adjacency_matrix(self.G, nodelist=self.node_list, weight="weight")
        matrix = sparse_matrix.toarray()  # Convert sparse matrix to dense NumPy array
        return matrix

    def update_adjacency_matrix(self):
        """Updates the adjacency matrix."""
        self.adjacency_matrix = self.create_adjacency_matrix()
        print("\nUpdated Adjacency Matrix:")
        print(self.adjacency_matrix)
        

    def on_click(self, event: MouseEvent):
        """Handles mouse click events."""
        if event.inaxes != self.ax:
            return
        
        if event.button == 3:  # Right-click
            for edge in self.G.edges:
                source_pos = self.positions[edge[0]]
                target_pos = self.positions[edge[1]]

            # Check if the double-click is close to the edge
                mid_x = (source_pos[0] + target_pos[0]) / 2
                mid_y = (source_pos[1] + target_pos[1]) / 2
                if abs(event.xdata - mid_x) < 0.5 and abs(event.ydata - mid_y) < 0.5:
                    self.G.remove_edge(edge[0], edge[1])  # Remove the edge
                    self.update_adjacency_matrix()
                    self.update_omega_values()
                    self.draw_graph()  # Update the graph
                    break

        elif event.button == 1:
        # Check if the click is near an edge
            for edge in self.G.edges:
                source_pos = self.positions[edge[0]]
                target_pos = self.positions[edge[1]]

            # Check if the click is close to the edge
                mid_x = (source_pos[0] + target_pos[0]) / 2
                mid_y = (source_pos[1] + target_pos[1]) / 2
                if abs(event.xdata - mid_x) < 0.5 and abs(event.ydata - mid_y) < 0.5:
                # Ask for a new weight in the terminal
                    try:
                        new_weight = round(eval(input(f"Enter new weight for edge {edge}: ")), 4)
                        self.G[edge[0]][edge[1]]['weight'] = new_weight
                        print(f"Updated weight for edge {edge} to {new_weight}")
                        self.update_adjacency_matrix()
                        self.update_omega_values()
                        self.draw_graph()
                    except ValueError:
                        print("Invalid weight. Please enter a numeric value.")
                    return

        # Check if the click is near a node to select it
            for node, pos in self.positions.items():
                if abs(event.xdata - pos[0]) < 0.5 and abs(event.ydata - pos[1]) < 0.5:
                    self.selected_node = node
                    return

    def on_release(self, event: MouseEvent):
        """Handles mouse release events to add or modify edges."""
        if event.inaxes != self.ax or not self.selected_node:
            self.selected_node = None
            return

        # Identify the target node
        for node, pos in self.positions.items():
            if abs(event.xdata - pos[0]) < 0.5 and abs(event.ydata - pos[1]) < 0.5:
                if node != self.selected_node:
                    # Prompt for a weight in the terminal
                    try:
                        if self.G.has_edge(self.selected_node, node):
                            weight = float(input(f"Enter weight for edge ({self.selected_node}, {node}): "))
                            self.G[self.selected_node][node]['weight'] = weight
                        else:
                            self.G.add_edge(self.selected_node, node, weight=1)
                                
                        self.update_adjacency_matrix()
                        self.update_omega_values()
                        self.draw_graph()
                    except ValueError:
                        print("Invalid weight. Please enter a numeric value.")
                        
                break

        self.selected_node = None



def create_grid_graph_with_source_and_pairs(vertices):
    """Creates the graph with a source node and all grid pairs."""
    G = nx.DiGraph()
    
    # Create a source node and a sink node
    source_node = "Source"
    sink_node = "Sink"
    G.add_node(source_node)
    G.add_node(sink_node)
    
    # Set positions for nodes
    positions = {source_node: (-1, -1), sink_node: (max(vertices) + 1, max(vertices) + 1)}  # Source and sink positions
    
    # Add grid nodes and positions
    for i in vertices:
        for j in vertices:
            node = (i, j)
            G.add_node(node)
            positions[node] = (i, j)
    
    # Add edges from the source node to all grid nodes
    for i in vertices:
        for j in vertices:
            G.add_edge(source_node, (i, j), weight=round((f_1[i-1]*f_2[j-1]), 4))
    
    # Add edges from all grid nodes to the sink node with weight 1
    for i in vertices:
        for j in vertices:
            G.add_edge((i, j), sink_node, weight=round((f_1[i-1]*f_2[j-1]), 4))
    
    return G, positions


# Example usage
vertices = [1, 2, 3, 4, 5]  # Define grid dimensions
f_1=[0.2,0.2,0.2,0.2,0.2]
f_2=[0.2,0.2,0.2,0.2,0.2]
x = [0,1]
G, positions = create_grid_graph_with_source_and_pairs(vertices)  # Create the graph
omega = [(node, round(np.random.random(), 4)) for node in G.nodes]
interactive_graph = InteractiveGraph(G, positions)  # Initialize interactive graph
plt.show()

