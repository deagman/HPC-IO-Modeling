import itertools
import os

class Input_File_Config :
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.parameters = parameters
        if not os.path.exists(self.file_path):
            raise ValueError(f"Invalid file path: {self.file_path}")
        with open(self.file_path, 'r') as template_file:
            self.template_content = template_file.read()
    
    def get_keys(self):
        return self.file_path, self.parameters
    
    def combinate_parameters(self):
        value_combinations = itertools.product(*self.parameters.values())
        params_combinations = []
        for combination in value_combinations:
            params = {}
            for key, value in zip(self.parameters.keys(), combination):
                subkeys = key.split(", ")
                subvalues = value.split(", ")
                for subkey, subvalue in zip(subkeys, subvalues):
                    params[subkey] = subvalue
            params_combinations.append(params)
        return params_combinations

    def generate_input_file(self, params_combination, folder_path):
        script_content = self.template_content

        for param, value in params_combination.items():
            script_content = script_content.replace(param, value)

        script_file_name = os.path.basename(self.file_path)
        script_file_path = os.path.join(folder_path, script_file_name)

        with open(script_file_path, 'w') as script_file:
            script_file.write(script_content)

        return script_file_path