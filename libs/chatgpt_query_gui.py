# worked with chatgpt on this

import tkinter as tk
from tkinter import ttk
import pandas as pd
import json

class FunctionParameterApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("Functions and Parameters to JSON")

        # DataFrames to store data
        # Functions DataFrame stores all added functions with their names and descriptions
        self.functions_df = pd.DataFrame(columns=["name", "description"])
        # Parameters DataFrame stores all parameters associated with functions
        self.parameters_df = pd.DataFrame(columns=["function", "name", "description"])

        # Left frame for the tables and controls
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for the JSON output
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ----- Functions Table -----
        # Label for the Functions table
        tk.Label(left_frame, text="Functions:").pack()

        # Treeview widget to display functions
        self.functions_tree = ttk.Treeview(left_frame, columns=("name", "description"), show="headings")
        self.functions_tree.heading("name", text="Name")
        self.functions_tree.heading("description", text="Description")
        self.functions_tree.pack(fill=tk.BOTH, expand=True)

        # Bind selection event to update Parameters table when a function is selected
        self.functions_tree.bind("<<TreeviewSelect>>", self.on_function_select)

        # Input frame for adding functions
        func_input_frame = tk.Frame(left_frame)
        func_input_frame.pack(fill=tk.X, pady=5)

        # Input fields for function name and description
        tk.Label(func_input_frame, text="Name:").grid(row=0, column=0)
        self.func_name_entry = tk.Entry(func_input_frame)
        self.func_name_entry.grid(row=0, column=1)

        tk.Label(func_input_frame, text="Description:").grid(row=0, column=2)
        self.func_desc_entry = tk.Entry(func_input_frame)
        self.func_desc_entry.grid(row=0, column=3)

        # Buttons to add and remove functions
        add_func_button = tk.Button(func_input_frame, text="Add Function", command=self.add_function)
        add_func_button.grid(row=0, column=4)

        remove_func_button = tk.Button(func_input_frame, text="Remove Function", command=self.remove_function)
        remove_func_button.grid(row=0, column=5)

        # ----- Parameters Table -----
        # Label for the Parameters table
        tk.Label(left_frame, text="Parameters for Selected Function:").pack()

        # Treeview widget to display parameters associated with the selected function
        self.params_tree = ttk.Treeview(left_frame, columns=("name", "description"), show="headings")
        self.params_tree.heading("name", text="Name")
        self.params_tree.heading("description", text="Description")
        self.params_tree.pack(fill=tk.BOTH, expand=True)

        # Input frame for adding parameters
        param_input_frame = tk.Frame(left_frame)
        param_input_frame.pack(fill=tk.X, pady=5)

        # Input fields for parameter name and description
        tk.Label(param_input_frame, text="Name:").grid(row=0, column=0)
        self.param_name_entry = tk.Entry(param_input_frame)
        self.param_name_entry.grid(row=0, column=1)

        tk.Label(param_input_frame, text="Description:").grid(row=0, column=2)
        self.param_desc_entry = tk.Entry(param_input_frame)
        self.param_desc_entry.grid(row=0, column=3)

        # Buttons to add and remove parameters
        add_param_button = tk.Button(param_input_frame, text="Add Parameter", command=self.add_parameter)
        add_param_button.grid(row=0, column=4)

        remove_param_button = tk.Button(param_input_frame, text="Remove Parameter", command=self.remove_parameter)
        remove_param_button.grid(row=0, column=5)

        # ----- JSON Output -----
        # Label for the JSON output area
        tk.Label(right_frame, text="JSON Output:").pack()

        # Textbox to display the generated JSON output
        self.json_text = tk.Text(right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.json_text.pack(fill=tk.BOTH, expand=True)

    # ----- Functions -----
    def add_function(self):
        """Add a new function to the Functions table and DataFrame."""
        name = self.func_name_entry.get().strip()
        description = self.func_desc_entry.get().strip()
        if name and description:  # Ensure both fields are not empty
            # Add the new function to the DataFrame
            new_row = {"name": name, "description": description}
            self.functions_df = pd.concat([self.functions_df, pd.DataFrame([new_row])], ignore_index=True)

            # Add the new function to the Treeview (GUI table)
            new_item_id = self.functions_tree.insert("", "end", values=(name, description))

            # Clear the input fields after adding
            self.func_name_entry.delete(0, tk.END)
            self.func_desc_entry.delete(0, tk.END)

            # Auto-select the newly added function
            self.functions_tree.selection_set(new_item_id)
            self.functions_tree.focus(new_item_id)

            # Trigger the on_function_select to refresh the Parameters table for the new function
            self.on_function_select(None)

            # Update the JSON view to reflect changes
            self.update_json_view()

    def remove_function(self):
        """Remove the selected function and its associated parameters."""
        selected_item = self.functions_tree.selection()
        if selected_item:
            # Get the index of the selected function
            row_index = self.functions_tree.index(selected_item[0])

            # Get the name of the selected function
            function_name = self.functions_df.iloc[row_index]["name"]

            # Remove the function from the DataFrame
            self.functions_df = self.functions_df.drop(index=row_index).reset_index(drop=True)

            # Remove the function from the Treeview (GUI table)
            self.functions_tree.delete(selected_item[0])

            # Remove all parameters associated with the function
            self.parameters_df = self.parameters_df[self.parameters_df["function"] != function_name].reset_index(drop=True)

            # Clear the Parameters Treeview since the function is removed
            self.params_tree.delete(*self.params_tree.get_children())

            # Update the JSON view to reflect changes
            self.update_json_view()

    def on_function_select(self, event):
        """Update the Parameters table when a function is selected."""
        selected_item = self.functions_tree.selection()
        if selected_item:
            # Get the index of the selected function
            row_index = self.functions_tree.index(selected_item[0])

            # Get the name of the selected function
            function_name = self.functions_df.iloc[row_index]["name"]

            # Clear the Parameters Treeview
            self.params_tree.delete(*self.params_tree.get_children())

            # Filter and display parameters for the selected function
            filtered_params = self.parameters_df[self.parameters_df["function"] == function_name]
            for _, param in filtered_params.iterrows():
                self.params_tree.insert("", "end", values=(param["name"], param["description"]))

    # ----- Parameters -----
    def add_parameter(self):
        """Add a new parameter to the Parameters table and DataFrame."""
        selected_item = self.functions_tree.selection()
        if selected_item:
            # Get the index of the selected function
            row_index = self.functions_tree.index(selected_item[0])

            # Get the name of the selected function
            function_name = self.functions_df.iloc[row_index]["name"]

            # Get the parameter name and description
            param_name = self.param_name_entry.get().strip()
            param_desc = self.param_desc_entry.get().strip()

            if param_name and param_desc:  # Ensure both fields are not empty
                # Add the new parameter to the DataFrame
                new_row = {"function": function_name, "name": param_name, "description": param_desc}
                self.parameters_df = pd.concat([self.parameters_df, pd.DataFrame([new_row])], ignore_index=True)

                # Add the new parameter to the Treeview (GUI table)
                self.params_tree.insert("", "end", values=(param_name, param_desc))

                # Clear the input fields after adding
                self.param_name_entry.delete(0, tk.END)
                self.param_desc_entry.delete(0, tk.END)

                # Update the JSON view to reflect changes
                self.update_json_view()

    def remove_parameter(self):
        """Remove the selected parameter."""
        selected_item = self.params_tree.selection()
        if selected_item:
            # Get the index of the selected parameter
            row_index = self.params_tree.index(selected_item[0])

            # Get the name of the selected parameter
            param_name = self.parameters_df.iloc[row_index]["name"]

            # Remove the parameter from the DataFrame
            self.parameters_df = self.parameters_df[self.parameters_df["name"] != param_name].reset_index(drop=True)

            # Remove the parameter from the Treeview (GUI table)
            self.params_tree.delete(selected_item[0])

            # Update the JSON view to reflect changes
            self.update_json_view()

    # ----- JSON Output -----
    def update_json_view(self):
        """Generate and display JSON output based on the current data."""
        # Build a nested JSON structure with functions and their parameters
        result = []

        for _, func in self.functions_df.iterrows():
            params = self.parameters_df[self.parameters_df["function"] == func["name"]]


            properties={}
            for _,param in params.iterrows():
                properties[param["name"]]= {
                            "description": param["description"]
                        }
                
                    

            result.append({
                "type":"function",
                "function": {
                "name": func["name"],
                "description": func["description"]},

                "parameters": {
                    "type": "object",
                    "properties":properties},
                }
            )

        # Convert the structure to JSON format
        json_output = json.dumps(result, indent=4)

        # Update the JSON display in the Textbox
        self.json_text.config(state=tk.NORMAL)
        self.json_text.delete("1.0", tk.END)
        self.json_text.insert(tk.END, json_output)
        self.json_text.config(state=tk.DISABLED)

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = FunctionParameterApp(root)  # Initialize the application
    root.mainloop()  # Start the GUI event loop
