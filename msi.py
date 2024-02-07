import tkinter as tk

class MSICache:
    def __init__(self, name):
        self.name = name
        self.state = 'I'  # Initial state: Invalid
        self.data = None

    def read(self):
        if self.state in ['M', 'S']:
            return self.data
        else:
            return None

    def write(self, data):
        self.data = data
        if self.state != 'M':  # Only change state if not already Modified
            self.state = 'M'

    def process_read(self, other_cache):
        if self.state == 'I':
            if other_cache.state == 'M':
                self.state = 'S'
                self.data = other_cache.data  # Read data from the other cache
            elif other_cache.state == 'S':
                self.state = 'S'
            elif other_cache.state == 'I':
                self.state = 'S'  # Shared if no other cache has the data
        # No need to handle 'E' state here

    def process_write(self, other_cache):
        if self.state in ['S', 'I']:
            self.state = 'M'  # Moving to Modified state regardless of other cache
        other_cache.invalidate()  # Invalidate the other cache

    def invalidate(self):
        if self.state != 'I':  # Invalidate if not already Invalid
            self.state = 'I'
            self.data = None

class MSIProtocol:
    def __init__(self):
        self.cache_A = MSICache('A')
        self.cache_B = MSICache('B')

    def display_state_table(self):
        print(f"{'Cache':<5}{'State':<10}{'Data':<10}")
        print(f"{'A':<5}{self.cache_A.state:<10}{self.cache_A.data}")
        print(f"{'B':<5}{self.cache_B.state:<10}{self.cache_B.data}")
        print()

    def simulate_read(self, cache, other_cache, data):
        print(f"{cache.name} reads data: {data}")
        cache.process_read(other_cache)
        if cache.state in ['E', 'S']:
            cache.data = data  # Update data on successful read
        self.display_state_table()

    def simulate_write(self, cache, other_cache, data):
        print(f"{cache.name} writes data: {data}")
        cache.write(data)
        cache.process_write(other_cache)
        self.display_state_table()

def simulate_gui_read():
    selected_cache = cache_var.get()
    data = data_entry.get()
    if selected_cache == "A":
        mesi_protocol.simulate_read(mesi_protocol.cache_A, mesi_protocol.cache_B, data)
    else:
        mesi_protocol.simulate_read(mesi_protocol.cache_B, mesi_protocol.cache_A, data)
    update_cache_labels()

def simulate_gui_write():
    selected_cache = cache_var.get()
    data = data_entry.get()
    if selected_cache == "A":
        mesi_protocol.simulate_write(mesi_protocol.cache_A, mesi_protocol.cache_B, data)
    else:
        mesi_protocol.simulate_write(mesi_protocol.cache_B, mesi_protocol.cache_A, data)
    update_cache_labels()

def update_cache_labels():
    state_colors = {'M': 'blue', 'S': 'green', 'I': 'red'}
    cache_A_state = mesi_protocol.cache_A.state
    cache_B_state = mesi_protocol.cache_B.state

    cache_A_label.config(text=f"Cache A: {cache_A_state} - {mesi_protocol.cache_A.data or 'None'}",
                         bg=state_colors.get(cache_A_state, 'white'))
    cache_B_label.config(text=f"Cache B: {cache_B_state} - {mesi_protocol.cache_B.data or 'None'}",
                         bg=state_colors.get(cache_B_state, 'white'))

root = tk.Tk()
root.title("MSI Cache Coherence Protocol Simulation")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=20)

cache_A_label = tk.Label(frame, text="Cache A: I - None", font=("Arial", 12), width=20)
cache_A_label.pack(side=tk.LEFT, padx=10, pady=10)

cache_B_label = tk.Label(frame, text="Cache B: I - None", font=("Arial", 12), width=20)
cache_B_label.pack(side=tk.LEFT, padx=10, pady=10)

cache_var = tk.StringVar(value="A")
tk.Radiobutton(root, text="Cache A", variable=cache_var, value="A", font=("Arial", 12)).pack()
tk.Radiobutton(root, text="Cache B", variable=cache_var, value="B", font=("Arial", 12)).pack()

tk.Label(root, text="Data:", font=("Arial", 12)).pack()
data_entry = tk.Entry(root, font=("Arial", 12))
data_entry.pack(pady=5)

read_button = tk.Button(root, text="Simulate Read", font=("Arial", 12), command=simulate_gui_read)
read_button.pack(pady=5)

write_button = tk.Button(root, text="Simulate Write", font=("Arial", 12), command=simulate_gui_write)
write_button.pack(pady=5)

mesi_protocol = MSIProtocol()
update_cache_labels()

root.mainloop()
