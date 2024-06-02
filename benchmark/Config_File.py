import json
import os

from benchmark.Slurm_Shell_Config import Slurm_Shell_Config
from benchmark.Input_File_Config import Input_File_Config
from benchmark.Output_File_Config import Output_File_Config

class Config_File :
    def __init__ (self, config_file_path):
        self.config_file_path = config_file_path
        with open(self.config_file_path, 'r') as config_file:
            self.config = json.load(config_file)

    def get_name(self):
        return self.config["name"]

    def get_mode(self):
        mode = self.config["mode"]
        if mode not in ["sequential", "batch"]:
            raise ValueError("Invalid mode, must be batch or sequential")
        return mode
    
    def get_result_folder(self):
        result_folder = self.config["result_folder"]
        # 如果result_folder不是绝对路径，则报错
        if not os.path.isabs(result_folder):
            raise ValueError("Invalid result folder, must be an absolute path")
        return result_folder
    
    def get_batchsize(self):
        if self.config["mode"] == "sequential" :
            return 1
        return self.config.get("batchsize", 1)
    
    def get_slurm_shell_config(self):
        slurm_shell_config = Slurm_Shell_Config(self.config["slurm_shell"]["file_path"], self.config["slurm_shell"].get("parameters"))
        return slurm_shell_config
        
    def get_input_file_configs(self):
        input_file_configs = []
        for key in self.config:
            if key.startswith("input_file"):
                input_file_config = Input_File_Config(self.config[key]["file_path"], self.config[key].get("parameters"))
                input_file_configs.append(input_file_config)
        return input_file_configs
    
    # 获取所有的output_file_config的名字，例如output_file_1, output_file_2, ...
    def get_output_file_configs(self):
        output_file_configs = []
        file_types = []
        test_type = None
        for key in self.config:
            if key.startswith("output_file"):
                file_type = self.config[key]["file_type"]
                output_file_config = Output_File_Config(file_type, self.config[key]["lines"])
                output_file_configs.append(output_file_config)
                file_types.append(file_type)
        # 检查file_types, 如果只有out, 则返回test_type = "out", 如果有out+darshan, 则返回test_type = "out+darshan"
        if len(file_types) == 1 and file_types[0] == "out":
            test_type = "out"
        elif len(file_types) == 2 and file_types[0] == "out" and file_types[1] == "darshan":
            test_type = "out+darshan"
        else:
            raise ValueError("Invalid test type, must be 'out' or 'out + darshan' ")
        return test_type, output_file_configs
