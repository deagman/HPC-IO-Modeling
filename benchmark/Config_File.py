import json
import os
import re

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
        if mode not in ["salloc", "sbatch"]:
            raise ValueError("Invalid mode, must be sbatch or salloc")
        return mode
    
    def get_test_type(self):
        test_type = self.config["test_type"]
        if test_type not in ["out", "out+darshan"]:
            raise ValueError("Invalid test type, must be 'out' or 'out+darshan'")
        return test_type
    
    def get_result_folder(self):
        result_folder = self.config["result_folder"]
        # 如果result_folder不是绝对路径，则报错
        if not os.path.isabs(result_folder):
            raise ValueError("Invalid result folder, must be an absolute path")
        return result_folder
    
    def get_batchsize(self):
        return self.config["batchsize"]
    
    def get_slurm_shell_config(self):
        slurm_shell_config = Slurm_Shell_Config(self.config["slurm_shell"]["file_path"], self.config["slurm_shell"]["parameters"])
        return slurm_shell_config
        
    def get_input_file_configs(self):
        input_file_configs = []
        for key in self.config:
            if key.startswith("input_file"):
                input_file_config = Input_File_Config(self.config[key]["file_path"], self.config[key]["parameters"])
                input_file_configs.append(input_file_config)
        return input_file_configs
    
    def get_output_file_configs(self):
        output_file_configs = []
        for key in self.config:
            if key.startswith("output_file"):
                output_file_config = Output_File_Config(self.config[key]["file_type"], self.config[key]["file_improc"], self.config[key]["lines"])
                output_file_configs.append(output_file_config)
        return output_file_configs
