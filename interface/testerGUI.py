import tkinter as tk
from tkinter import scrolledtext
import sys
from core.tester import Tester

class RedirectStdoutToTkinter:
    def __init__(self, widget):
        self.widget = widget

    def write(self, msg):
        self.widget.configure(state='normal')  # Make the widget editable
        self.widget.insert(tk.END, msg)
        self.widget.configure(state='disabled')  # Disable editing after inserting text
        self.widget.yview(tk.END)  # Auto scroll to the bottom

    def flush(self):
        pass  # No need to flush for Tkinter widget output


class TesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Tester")

        # Initialize the tester object
        self.tester = Tester(root)

        # Configure root window grid
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Left frame for buttons
        left_frame = tk.Frame(root)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Arm/Disarm Button
        self.toggle_button = tk.Button(left_frame, text="Arm", command=self.toggle_arm_disarm, width=15)
        self.toggle_button.pack(pady=5)

        # Right frame for target input (10 static fields)
        right_frame = tk.Frame(root)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.target_entries = []
        for i in range(10):
            entry = tk.Entry(right_frame, width=30)
            entry.grid(row=i, column=0, padx=5, pady=2)
            self.target_entries.append(entry)

        # Scrolled text box for log at the bottom
        self.log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state='disabled')
        self.log_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Redirect stderr and stdout to the scroll box
        sys.stdout = RedirectStdoutToTkinter(self.log_box)
        sys.stderr = RedirectStdoutToTkinter(self.log_box)

    def get_targets(self):
        """Return a list of entered target IPs."""
        # Filter out empty entries
        targets = [entry.get().strip() for entry in self.target_entries if entry.get().strip()]
        return targets

    def toggle_arm_disarm(self):
        """Toggle the system between armed and disarmed states."""
        if self.tester.get_armed():
            self.disarm_system()  # Disarm the system
        else:
            self.arm_system()  # Arm the system

    def arm_system(self):
        """Arm the tester with the targets."""
        try:
            targets = self.get_targets()
            if not targets:
                print("Error arming system: Please add at least one target IP")
                return
            self.tester.flush_targets(targets)  # Use flush_targets to replace old targets
            self.tester.arm()  # Arm the system
            self.update_toggle_button()
            print("System armed.")
        except Exception as e:
            print(f"Error arming system: {e}")

    def disarm_system(self):
        """Disarm the tester."""
        try:
            self.tester.disarm()
            self.update_toggle_button()
            print("System disarmed.")
        except Exception as e:
            print(f"Error disarming system: {e}")

    def update_toggle_button(self):
        """Update the toggle button based on the armed state."""
        if self.tester.get_armed():
            self.toggle_button.config(text="Disarm")  # Change button to "Disarm"
        else:
            self.toggle_button.config(text="Arm")  # Change button back to "Arm"