import tkinter as tk
from tkinter import ttk
import pandas as pd
import json


class FunctionParameterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Functions and Parameters to JSON")

        # DataFrames to store data
        self.functions_df = pd.DataFrame(columns=["name", "description"])
        self.parameters_df = pd.DataFrame(columns=["function", "name", "description", "type", "required"])

        # Left frame for the tables and controls
        left_frame = tk.Frame(root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right frame for the JSON output
        right_frame = tk.Frame(root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ----- Functions Table -----
        tk.Label(left_frame, text="Functions:").pack()

        self.functions_tree = ttk.Treeview(left_frame, columns=("name", "description"), show="headings")
        self.functions_tree.heading("name", text="Name")
        self.functions_tree.heading("description", text="Description")
        self.functions_tree.pack(fill=tk.BOTH, expand=True)

        self.functions_tree.bind("<<TreeviewSelect>>", self.on_function_select)

        func_input_frame = tk.Frame(left_frame)
        func_input_frame.pack(fill=tk.X, pady=5)

        tk.Label(func_input_frame, text="Name:").grid(row=0, column=0)
        self.func_name_entry = tk.Entry(func_input_frame)
        self.func_name_entry.grid(row=0, column=1)

        tk.Label(func_input_frame, text="Description:").grid(row=0, column=2)
        self.func_desc_entry = tk.Entry(func_input_frame)
        self.func_desc_entry.grid(row=0, column=3)

        add_func_button = tk.Button(func_input_frame, text="Add Function", command=self.add_function)
        add_func_button.grid(row=0, column=5)

        remove_func_button = tk.Button(func_input_frame, text="Remove Function", command=self.remove_function)
        remove_func_button.grid(row=0, column=6)

        # ----- Parameters Table -----
        tk.Label(left_frame, text="Parameters for Selected Function:").pack()

        self.params_tree = ttk.Treeview(
            left_frame, columns=("name", "description", "type", "required"), show="headings"
        )
        self.params_tree.heading("name", text="Name")
        self.params_tree.heading("description", text="Description")
        self.params_tree.heading("type", text="Type")
        self.params_tree.heading("required", text="Required")
        self.params_tree.pack(fill=tk.BOTH, expand=True)

        param_input_frame = tk.Frame(left_frame)
        param_input_frame.pack(fill=tk.X, pady=5)

        tk.Label(param_input_frame, text="Name:").grid(row=0, column=0)
        self.param_name_entry = tk.Entry(param_input_frame)
        self.param_name_entry.grid(row=0, column=1)

        tk.Label(param_input_frame, text="Description:").grid(row=0, column=2)
        self.param_desc_entry = tk.Entry(param_input_frame)
        self.param_desc_entry.grid(row=0, column=3)

        tk.Label(param_input_frame, text="Type:").grid(row=1, column=0)
        self.param_type_entry = tk.Entry(param_input_frame)
        self.param_type_entry.grid(row=1, column=1)

        tk.Label(param_input_frame, text="Required:").grid(row=1, column=2)
        self.param_required_var = tk.BooleanVar()
        tk.Checkbutton(param_input_frame, variable=self.param_required_var).grid(row=1, column=3)

        add_param_button = tk.Button(param_input_frame, text="Add Parameter", command=self.add_parameter)
        add_param_button.grid(row=1, column=5)

        remove_param_button = tk.Button(param_input_frame, text="Remove Parameter", command=self.remove_parameter)
        remove_param_button.grid(row=1, column=6)

        # ----- JSON Output -----
        tk.Label(right_frame, text="JSON Output:").pack()

        self.json_text = tk.Text(right_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.json_text.pack(fill=tk.BOTH, expand=True)

    def add_function(self):
        name = self.func_name_entry.get().strip()
        description = self.func_desc_entry.get().strip()
        if name and description:
            new_row = {"name": name, "description": description}
            self.functions_df = pd.concat([self.functions_df, pd.DataFrame([new_row])], ignore_index=True)
            new_item_id = self.functions_tree.insert("", "end", values=(name, description))
            self.func_name_entry.delete(0, tk.END)
            self.func_desc_entry.delete(0, tk.END)
            self.functions_tree.selection_set(new_item_id)
            self.functions_tree.focus(new_item_id)
            self.on_function_select(None)
            self.update_json_view()

    def remove_function(self):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            self.functions_df = self.functions_df.drop(index=row_index).reset_index(drop=True)
            self.functions_tree.delete(selected_item[0])
            self.parameters_df = self.parameters_df[self.parameters_df["function"] != function_name].reset_index(
                drop=True
            )
            self.params_tree.delete(*self.params_tree.get_children())
            self.update_json_view()

    def on_function_select(self, event):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            self.params_tree.delete(*self.params_tree.get_children())
            filtered_params = self.parameters_df[self.parameters_df["function"] == function_name]
            for _, param in filtered_params.iterrows():
                self.params_tree.insert("", "end", values=(param["name"], param["description"], param["type"], param["required"]))

    def add_parameter(self):
        selected_item = self.functions_tree.selection()
        if selected_item:
            row_index = self.functions_tree.index(selected_item[0])
            function_name = self.functions_df.iloc[row_index]["name"]
            param_name = self.param_name_entry.get().strip()
            param_desc = self.param_desc_entry.get().strip()
            param_type = self.param_type_entry.get().strip()
            param_required = self.param_required_var.get()
            if param_name and param_desc and param_type:
                new_row = {
                    "function": function_name,
                    "name": param_name,
                    "description": param_desc,
                    "type": param_type,
                    "required": param_required,
                }
                self.parameters_df = pd.concat([self.parameters_df, pd.DataFrame([new_row])], ignore_index=True)
                self.params_tree.insert("", "end", values=(param_name, param_desc, param_type, param_required))
                self.param_name_entry.delete(0, tk.END)
                self.param_desc_entry.delete(0, tk.END)
                self.param_type_entry.delete(0, tk.END)
                self.param_required_var.set(False)
                self.update_json_view()

    def remove_parameter(self):
        selected_item = self.params_tree.selection()
        if selected_item:
            row_index = self.params_tree.index(selected_item[0])
            param_name = self.parameters_df.iloc[row_index]["name"]
            self.parameters_df = self.parameters_df[self.parameters_df["name"] != param_name].reset_index(drop=True)
            self.params_tree.delete(selected_item[0])
            self.update_json_view()

    def update_json_view(self):
        result = []
        for _, func in self.functions_df.iterrows():
            params = self.parameters_df[self.parameters_df["function"] == func["name"]]
            properties = {}
 
            for _, param in params.iterrows():
                properties[param["name"]] = {
                    "type": param["type"],
                    "description": param["description"],
                }
            
            # list of required parameters
            required_params = list(params[params["required"]]["name"])
            # add params list to func for each func
            result.append(
                {
                    "type": "function",
                    "function": {"name": func["name"], "description": func["description"]},
                    "parameters": {"type": "object", "properties": properties,"required":required_params},
                }
            )
        json_output = json.dumps(result, indent=4)
        self.json_text.config(state=tk.NORMAL)
        self.json_text.delete("1.0", tk.END)
        self.json_text.insert(tk.END, json_output)
        self.json_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionParameterApp(root)
    root.mainloop()
