import itertools
import os

class Input_File_Config :
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.parameters = parameters
    
    def get_keys(self):
        return self.file_path, self.parameters
    
    def combinate_parameters(self):
        value_combinations = itertools.product(*self.parameters.values())
        # 组装成参数字典
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

    def generate_input_file(self, params_combination):
        # 检查是否存在文件
        if not os.path.exists(self.file_path):
            raise ValueError(f"Invalid file path: {self.file_path}")
        
        # Read the template file
        with open(self.file_path, 'r') as template_file:
            template_content = template_file.read()

        # Replace placeholders with actual parameter values
        script_content = template_content
        for param_name, param_values in self.parameters.items():
            param_names = param_name.split(', ')
            for name in param_names:
                placeholder = f"${name}"
                if placeholder in script_content:
                    script_content = script_content.replace(placeholder, str(params_combination[name]))

        # Generate the script file
        script_file_path = self.file_path + "_generated"
        with open(script_file_path, 'w') as script_file:
            script_file.write(script_content)

        return script_file_path

# test
if __name__ == "__main__":
    parameters = {
            "striping_factor": [1, 2]
        }
    input_file = Input_File_Config('hintsFile', parameters)
    params_combinations = input_file.combinate_parameters()
    print(params_combinations)
    print(input_file.generate_input_file(params_combinations[0]))