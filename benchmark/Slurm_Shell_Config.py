import itertools
import os

class Slurm_Shell_Config :
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.parameters = parameters
    
    def get_keys(self):
        return self.file_path, self.parameters
    
    # 首先生成所有value的组合，然后赋值给对应的parameters
    def combinate_parameters(self):
        value_combinations = itertools.product(*self.parameters.values())
        params_combinations = []
        for combination in value_combinations:
            params_combination = {}
            for key, value in zip(self.parameters.keys(), combination):
                subkeys = key.split(", ")
                subvalues = value.split(", ")
                for subkey, subvalue in zip(subkeys, subvalues):
                    params_combination[subkey] = subvalue
            params_combinations.append(params_combination)
        return params_combinations
    
    # 将模板文件中为key的字符串替换成params_combination中对应的value
    def generate_shell_file(self, params_combination, folder_path):
        if not os.path.exists(self.file_path):
            raise ValueError(f"Invalid file path: {self.file_path}")

        with open(self.file_path, 'r') as template_file:
            template_content = template_file.read()
        script_content = template_content

        for param, value in params_combination.items():
            script_content = script_content.replace(param, value)

        script_file_name = os.path.basename(self.file_path)
        script_file_path = os.path.join(folder_path, script_file_name)

        with open(script_file_path, 'w') as script_file:
            script_file.write(script_content)

        return script_file_path