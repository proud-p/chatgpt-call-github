import tkinter as tk
from tkinter import ttk
import pandas as pd
import json

class FunctionParameterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Functions and Parameters to JSON")

        # DataFrames to store data
        self.functions_df = pd.DataFrame(columns=["name", "description"])  # Functions table
        self.parameters_df = pd.DataFrame(columns=["function", "name", "description"])  # Parameters table

        # Frames for the layout
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ----- Functions Table -----
        tk.Label(left_frame, text="Functions:").pack()
        self.functions_tree = ttk.Treeview(left_frame, columns=("name", "description"), show="headings")
        self.functions_tree.heading("name", text="Name")
        self.functions_tree.heading("description", text="Description")
        self.functions_tree.pack(fill=tk.BOTH, expand=True)
        self.functions_tree.bind("<<TreeviewSelect>>", self.on_function_select)  # Update Parameters Table on selection

        # Add Function controls
        func_input_frame = tk.Frame(left_frame)
        func_input_frame.pack(fill=tk.X, pady=5)
        tk.Label(func_input_frame, text="Name:").grid(row=0, column=0)
        self.func_name_entry = tk.Entry(func_input_frame)
        self.func_name_entry.grid(row=0, column=1)

        tk.Label(func_input_frame, text="Description:").grid(row=0, column=2)
        self.func_desc_entry = tk.Entry(func_input_frame)
        self.func_desc_entry.grid(row=0, column=3)

        add_func_button = tk.Button(func_input_frame, text="Add Function", command=self.add_function)
        add_func_button.grid(row=0, column=4)

        remove_func_button = tk.Button(func_input_frame, text="Remove Function", command=self.remove_function)
        remove_func_button.grid(row=0, column=5)

        # ----- Parameters Table -----
        tk.Label(left_frame, text="Parameters for Selected Function:").pack()
        self.params_tree = ttk.Treeview(left_frame, columns=("name", "description"), show="headings")
        self.params_tree.heading("name", text="Name")
        self.params_tree.heading("description", text="Description")
        self.params_tree.pack(fill=tk.BOTH, expand=True)

        # Add Parameter controls
        param_input_frame = tk.Frame(left_frame)
        param_input_frame.pack(fill=tk.X, pady=5)
        tk.Label(param_input_frame, text="Name:").grid(row=0, column=0)
        self.param_name_entry = tk.Entry(param_input_frame)
        self.param_name_entry.grid(row=0, column=1)

        tk.Label(param_input_frame, text="Description:").grid(row=0, column=2)
        self.param_desc_entry = tk.Entry(param_input_frame)
        self.param_desc_entry.grid(row=0, column=3)

        add_param_button = tk.Button(param_input_frame, text="Add Parameter", command=self.add_parameter)
        add_param_button.grid(row=0, column=4)

        remove_param_button = tk.Button(param_input_frame, text="Remove Parameter", command=self.remove_parameter)
        remove_param_button.grid(row=0, column=5)

        # ----- JSON View -----
        tk.Label(right_frame, text="JSON Output:").pack()
        self.json_text = tk.Text(right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.json_text.pack(fill=tk.BOTH, expand=True)

    # ----- Functions -----
    def add_function(self):
        name = self.func_name_entry.get().strip()
        description = self.func_desc_entry.get().strip()
        if name and description:
            new_row = {"name": name, "description": description}
            self.functions_df = pd.concat([self.functions_df, pd.DataFrame([new_row])], ignore_index=True)
            self.functions_tree.insert("", "end", values=(name, description))
            self.func_name_entry.delete(0, tk.END)
            self.func_desc_entry.delete(0, tk.END)
            self.update_json_view()

    def remove_function(self):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            self.functions_df = self.functions_df.drop(index=row_index).reset_index(drop=True)
            self.functions_tree.delete(selected_item[0])
            # Remove parameters linked to the function
            self.parameters_df = self.parameters_df[self.parameters_df["function"] != function_name].reset_index(drop=True)
            self.params_tree.delete(*self.params_tree.get_children())
            self.update_json_view()

    def on_function_select(self, event):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            # Filter parameters for the selected function
            self.params_tree.delete(*self.params_tree.get_children())
            filtered_params = self.parameters_df[self.parameters_df["function"] == function_name]
            for _, param in filtered_params.iterrows():
                self.params_tree.insert("", "end", values=(param["name"], param["description"]))

    # ----- Parameters -----
    def add_parameter(self):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            param_name = self.param_name_entry.get().strip()
            param_desc = self.param_desc_entry.get().strip()
            if param_name and param_desc:
                new_row = {"function": function_name, "name": param_name, "description": param_desc}
                self.parameters_df = pd.concat([self.parameters_df, pd.DataFrame([new_row])], ignore_index=True)
                self.params_tree.insert("", "end", values=(param_name, param_desc))
                self.param_name_entry.delete(0, tk.END)
                self.param_desc_entry.delete(0, tk.END)
                self.update_json_view()

    def remove_parameter(self):
        selected_item = self.params_tree.selection()
        if selected_item:
            row_index = self.params_tree.index(selected_item[0])
            param_name = self.parameters_df.iloc[row_index]["name"]
            self.parameters_df = self.parameters_df[self.parameters_df["name"] != param_name].reset_index(drop=True)
            self.params_tree.delete(selected_item[0])
            self.update_json_view()

    # ----- JSON Output -----
    def update_json_view(self):
        # Combine functions and their parameters into nested JSON
        result = []
        for _, func in self.functions_df.iterrows():
            params = self.parameters_df[self.parameters_df["function"] == func["name"]]
            result.append({
                "name": func["name"],
                "description": func["description"],
                "parameters": params[["name", "description"]].to_dict(orient="records")
            })
        json_output = json.dumps(result, indent=4)
        self.json_text.config(state=tk.NORMAL)
        self.json_text.delete("1.0", tk.END)
        self.json_text.insert(tk.END, json_output)
        self.json_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionParameterApp(root)
    root.mainloop()
