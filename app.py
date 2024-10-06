import tkinter as tk
import numpy as np
import re
from cartesian_plan import CartesianPlan
from utils import generate_random_color
import matplotlib.pyplot as plt



total_vector = 0
total_points = 0

def plot_graph():
    # Definir as funções de acordo com as equações fornecidas
    def g(x):
        return np.where((-4.24 <= x) & (x <= -1.29), 0.3 * x**2 - 0.7171357114461 * x - 9.3517145743126, np.nan)

    def h(x):
        return np.where((-6.85 <= x) & (x <= 1.07), -0.3 * x**2 - 2.420254606549625 * x - 2.5707541879086, np.nan)

    def p(x):
        return np.where((-10 <= x) & (x <= -4.24), 0.7 * x**2 + 9.8235918524086 * x + 28.1356134992317, np.nan)

    def q(x):
        return np.where((-10 <= x) & (x <= 10), -0.1 * x**2 + 10, np.nan)

    def q_2(x):
        x_adj = x + 0.0680917115144
        return np.where((-6.87 <= x_adj) & (x_adj <= 6.85), -0.1 * x_adj**2 + 4.6845713673334, np.nan)

    def r(x):
        return np.where((-1.31 <= x) & (x <= 10), (0.5 * (0.73 * (x + 3.3991894174067) + 2.9408717431496) - 3.3609962778853)**2 - 9.1729560397548, np.nan)

    def s(x):
        return np.where((1.09 <= x) & (x <= 6.85), (0.5 * (0.73 * (x + 4.7359493006565) + 2.9408717431496) - 3.3609962778853)**2 - 5.5446077852195, np.nan)

    # Intervalo de x para o gráfico
    x = np.linspace(-10, 10, 1000)

    # Criar a figura e os eixos
    plt.figure(figsize=(10, 6))

    # Plotar as funções dentro dos seus respectivos intervalos
    plt.plot(x, g(x), label='g(x)', color='blue')
    plt.plot(x, h(x), label='h(x)', color='green')
    plt.plot(x, p(x), label='p(x)', color='red')
    plt.plot(x, q(x), label='q(x)', color='purple')
    plt.plot(x, q_2(x), label='q_2(x)', color='orange')
    plt.plot(x, r(x), label='r(x)', color='brown')
    plt.plot(x, s(x), label='s(x)', color='pink')

    # Adicionar título e rótulos aos eixos
    plt.title("Gráfico das funções definidas por intervalos")
    plt.xlabel("x")
    plt.ylabel("y")

    # Adicionar legenda
    plt.legend()

    # Mostrar o gráfico
    plt.grid(True)
    plt.show()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vectors Race")

        # Input box for entering items
        self.input_frame = tk.Frame(self)
        self.input_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

        self.label = tk.Label(self.input_frame, text="Enter Item:")
        self.label.pack(pady=10)

        # Entry box for input (where the user enters the point or vector)
        self.input_entry = tk.Entry(self.input_frame)
        self.input_entry.pack(pady=10)

        # Button to draw the item based on the input above
        self.draw_button = tk.Button(self.input_frame, text="Draw Item", command=self.draw_point_from_input)
        self.draw_button.pack(pady=10)

        # Bind the Enter key to trigger draw_point_from_input, which means pressing Enter will draw the item as if the button was clicked
        self.input_entry.bind("<Return>", lambda event: self.draw_point_from_input())

        # Listbox to display points
        self.point_list_label = tk.Label(self.input_frame, text="Items List:")
        self.point_list_label.pack(pady=10)

        # Where the items are being displayed
        self.point_listbox = tk.Listbox(self.input_frame)
        self.point_listbox.pack(pady=10)

        self.delete_button = tk.Button(self.input_frame, text="Delete Selected Item", command=self.delete_item)
        self.delete_button.pack(pady=10)

        # Button to display the graph
        self.graph_button = tk.Button(self.input_frame, text="Show Graph", command=plot_graph)
        self.graph_button.pack(pady=10)

        # Create the canvas for the Cartesian plane
        self.cartesian_plane = CartesianPlan(self, self.point_listbox)
        self.cartesian_plane.place(relx=0, rely=0, relwidth=0.8, relheight=1)

        # Label to display error messages
        self.error_label = tk.Label(self.input_frame, text="", fg="red")
        self.error_label.pack(pady=10)

    def draw_point_from_input(self):
        """
        Handles drawing the point or vector based on the input from the entry box.
        The formats are:
            - Point: Letter in uppercase followed by '(' and the x and y coordinates separated by a comma and closed with ')'. Example: A(0,1)
            - Vector from origin: Letter in lowercase followed by the x and y coordinates separated by a comma. Example: u(1,3)
            - Vector between two points: Two uppercase letters representing the points. The vector will be from the first point to the second point. Example: AB
        """

        global total_points  # Declare global variable for total points
        global total_vector  # Declare global variable for total vectors

        input_text = self.input_entry.get()

        # Check if the input is for two existing points (e.g., "AB")
        if re.match(r"^[A-Z]{2}$", input_text):
            start_label = input_text[0]
            end_label = input_text[1]

            # Ensure both points exist
            if start_label in self.cartesian_plane.items and end_label in self.cartesian_plane.items:

                # Check if this vector already exists
                existing_items = self.point_listbox.get(0, tk.END)  # Get all vectors in this format
                vector_label = f"{start_label}{end_label} vector from {start_label} to {end_label}"  # Current vector

                if vector_label in existing_items:
                    self.error_label.config(text=f"Error: Vector {start_label}{end_label} already exists.")
                    return

                else:
                    # Check if there is already 4 vectors
                    if total_vector == 4:
                        self.error_label.config(text="Error: Exceeded 4 vectors")
                        return
                    else: 
                        total_vector += 1                
                    # Get the coordinates of both points
                    start_coords = self.cartesian_plane.items[start_label]["coords"]
                    end_coords = self.cartesian_plane.items[end_label]["coords"]

                    # Draw the vector from start to end
                    self.cartesian_plane.draw_vector_between_points(start_coords, end_coords, start_label, end_label,
                                                                    input_text)
                    self.point_listbox.insert(tk.END, f"{input_text} vector from {start_label} to {end_label}")
                    self.error_label.config(text="")  # Clear any previous error
            else:
                self.error_label.config(text=f"Error: Points {start_label} and/or {end_label} do not exist.")
            return

        # Check if the input is for a point (e.g., "A(0,1)")
        match = re.match(r"([A-Z])\((-?\d+),\s*(-?\d+)\)", input_text)
        if match:

            label = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))

            # Check if the label already exists for both points and vectors
            if label in self.cartesian_plane.items:
                self.error_label.config(text=f"Error: Label {label} already exists.")
                return

            # Ensure that the coordinates are within the predefined range
            if -6 <= x <= 6 and -6 <= y <= 6:
                # Check if there is already 5 points
                if total_points == 5:
                    self.error_label.config(text="Error: Exceeded 5 points")
                    return
                else: 
                    total_points += 1
                # Checks if it is a point or a vector to be drawn
                if label.isupper():
                    self.cartesian_plane.draw_point(x, y, label)
                    # Add point's notation to the listbox
                    self.point_listbox.insert(tk.END, f"{label}({x},{y})")
                # else:
                #     self.cartesian_plane.draw_vector(x, y, label)
                #     # Add vector's notation to the listbox
                #     self.point_listbox.insert(tk.END, f"{label} vector (0,0) to ({x},{y})")

                # Clear the input box after drawing the point or vector in case of any errors present
                self.error_label.config(text="")
                return
            else:
                self.error_label.config(text="Coordinates out of range (-6 to 6).")
                return
            
        # Check if the input is for a vector from the origin (e.g., "u=(1,3)")
        match = re.match(r"([a-z])=\((-?\d+),\s*(-?\d+)\)", input_text)
        if match:
            
            label = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))

            if label in self.cartesian_plane.items:
                self.error_label.config(text=f"Error: Label {label} already exists.")
                return

            if -6 <= x <= 6 and -6 <= y <= 6:
                # Check if there is already 4 vectors
                if total_vector == 4:
                    self.error_label.config(text="Error: Exceeded 4 vectors")
                    return
                else: 
                    total_vector += 1
                self.cartesian_plane.draw_vector(x, y, label)
                # Add vector's notation to the listbox
                self.point_listbox.insert(tk.END, f"{label} vector (0,0) to ({x},{y})")
                self.error_label.config(text="")
            else:
                self.error_label.config(text="Coordinates out of range (-6 to 6).")
        else:
            self.error_label.config(text="Invalid input format. Please enter in the format A(0,1), u=(1,3), or AB.")

    def delete_item(self):
        global total_points
        global total_vector
        """
        Deletes the selected point or vector from the canvas and the list.
        The item deleted can be a point or a vector, and to delete just select the item from the listbox and click on the delete button.
        If the item is:
            - A vector (of any kind): only the item will be deleted
            - A point: if the point is deleted, all vectors that involve this point will also be deleted
        """
        selected_index = self.point_listbox.curselection()
        if selected_index:
            item_info = self.point_listbox.get(selected_index)

            # Extract the label from the item_info and check if it's a point or a vector
            if 'vector' in item_info:
                total_vector -= 1 # Decrease the global variable of vectors
                label = item_info.split(' ')[0]
                self.cartesian_plane.delete_vector(label)
            else:
                total_points -= 1 # Decrease the global variable of points
                label = item_info.split('(')[0]

                # Create a list of vectors to delete that involve this point
                vectors_to_delete = [
                    vec_label for vec_label, vec_data in list(self.cartesian_plane.items.items())
                    if vec_data["type"] == "vector" and
                       (
                               "points" in vec_data and label in vec_data["points"]  # Vectors between points
                               or "points" not in vec_data and vec_data["coords"] == (0, 0)  # Vector from origin
                       )
                ]

                # Delete the vectors that involve this point
                for vec_label in vectors_to_delete:
                    total_vector -= 1 # Decrease the global variable of vectors
                    self.cartesian_plane.delete_vector(vec_label)

                self.cartesian_plane.delete_point(label)

            # Update the listbox after deleting the item(s)
            self.update_listbox()

            self.error_label.config(text="")

    def update_listbox(self):
        """Updates the listbox to show the current points and vectors."""
        self.point_listbox.delete(0, tk.END)

        # Insert all points and vectors into the listbox again
        for label, item in self.cartesian_plane.items.items():
            if item["type"] == "point":
                x, y = item["coords"]
                self.point_listbox.insert(tk.END, f"{label}({x},{y})")
            elif item["type"] == "vector":
                if "points" in item:
                    # Vectors between two points
                    start_label, end_label = item["points"]
                    self.point_listbox.insert(tk.END, f"{label} vector from {start_label} to {end_label}")
                else:
                    # Vector from the origin (0,0)
                    x, y = item["coords"]
                    self.point_listbox.insert(tk.END, f"{label} vector (0,0) to ({x},{y})")


if __name__ == "__main__":
    app = App()
    app.geometry("1000x600")
    app.mainloop()
