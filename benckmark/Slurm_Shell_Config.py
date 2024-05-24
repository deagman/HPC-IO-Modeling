import itertools
import os
import re

class Slurm_Shell_Config :
    def __init__(self, submit_cmd, file_path, parameters):
        self.submit_cmd = submit_cmd
        self.file_path = file_path
        self.parameters = parameters
    
    def get_submit_cmd(self):
        return self.submit_cmd
    
    def get_keys(self):
        return self.submit_cmd, self.file_path, self.parameters
    
    # 独立参数
    # params_combination = {'t':['1M','4M'], 'b':['4M','16M']}
    # params_combinations = [{'t':'1M', 'b':'4M'}, {'t':'1M', 'b':'16M'}, {'t':'4M', 'b':'4M'}, {'t':'4M', 'b':'16]
    # 共轭参数
    # params_combination = {'t, b': ['1M, 4M', '4M, 16M']}
    # params_combinations = [{'t':'1M', 'b':'4M'}, {'t':'4M', 'b':'16M'}]
    '''
    parameters = {
        "t, b": ["1m, 4m", "4m, 16m"],
        "a" : ["1", "2"],
        "c, d": ["1, 2", "2, 3"]
    }
    '''
    '''
    params_combinations =
    [
        {'t': '1m', 'b': '4m', 'a': '1', 'c': '1', 'd': '2'},
        {'t': '1m', 'b': '4m', 'a': '1', 'c': '2', 'd': '3'},
        {'t': '1m', 'b': '4m', 'a': '2', 'c': '1', 'd': '2'},
        {'t': '1m', 'b': '4m', 'a': '2', 'c': '2', 'd': '3'},
        {'t': '4m', 'b': '16m', 'a': '1', 'c': '1', 'd': '2'},
        {'t': '4m', 'b': '16m', 'a': '1', 'c': '2', 'd': '3'},
        {'t': '4m', 'b': '16m', 'a': '2', 'c': '1', 'd': '2'},
        {'t': '4m', 'b': '16m', 'a': '2', 'c': '2', 'd': '3'}
    ]
    '''
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

    
    # 根据file_path指定的模板文件，生成脚本文件，脚本文件相比于模板文件，就是模板文件中用$标识的参数值被替换成了params_combination中的参数值
    def generate_shell_file(self, params_combination):
        # 检查是否存在文件
        if not os.path.exists(self.file_path):
            raise ValueError(f"Invalid file path: {self.file_path}")
        
        # Read the template file
        with open(self.file_path, 'r') as template_file:
            template_content = template_file.read()

        # Replace placeholders with actual parameter values
        # 仅修改slurm_shell_config中$标识的参数
        script_content = template_content
        for match in re.finditer(r'\$\w+', script_content):
            param = match.group()[1:]  # Remove the $ at the start
            if param in params_combination:
                value = params_combination[param]
                script_content = script_content.replace('$' + param, value)

        # Generate the script file
        script_file_path = self.file_path + "_generated"
        with open(script_file_path, 'w') as script_file:
            script_file.write(script_content)

        return script_file_path
    
# test
if __name__ == "__main__":
    
    parameters = {
      "transfersize, blocksize": ["512k, 2m", "1m, 8m", "2m, 32m", "4m, 128m"],
      "segment": ["1", "4", "16"],
      "direct_read" : ["true", "false"],
      "direct_write" : ["true", "false"],
      "striping_unit" : ["1048576", "2097152", "4194304", "8388608"],
      "striping_factor" : ["1", "2", "4", "8"]
    }

    slurm_shell = Slurm_Shell_Config('sbathc -p thcp3','/thfs3/home/xjtu_cx/hugo/test/model/experiment1/tests/slurm_shell-1.sh', parameters)
    params_combinations = slurm_shell.combinate_parameters()
    print(params_combinations)
    # 打印params_combinations的数量
    print(len(params_combinations))
    print(slurm_shell.generate_shell_file(params_combinations[2]))