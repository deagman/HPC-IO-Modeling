'''
{
  "slurm_shell": {
    "file_path": "slurm_shell.sh",
    "partition": "thmt1",
    "parameters": {
      "t": ["1m", "4m"],
      "b": ["4m", "16m"]
    }
  },
  "input_file_1": {
    "file_path": "hintsFile",
    "parameters": {
        "striping_factor": [1, 2]
    }
  },
  "output_file_1": {
    "file_folder": "/thfs3/home/xjtu_cx/hugo/test/model1/" ,
    "lines": [
        "xfersize            : $t MiB",
        "blocksize           : $b MiB"
    ]
  },
  "output_file_2": {
    "file_path": "output.txt",
    "lines": [
        "IO_bandwith = $io_bw",
        "IO_runtime = $io_rt",
        "IO_throughput = $io_tp_1 300MB/s $io_tp_2"
    ]
  }
}
'''
import json

from Slurm_Shell_Config import Slurm_Shell_Config
from Input_File_Config import Input_File_Config
from Output_File_Config import Output_File_Config

class Config_File :
    def __init__ (self, config_file_path):
        self.config_file_path = config_file_path

    def get_slurm_shell_config(self):
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file)
            slurm_shell_config = Slurm_Shell_Config(config["slurm_shell"]["submit_cmd"],config["slurm_shell"]["file_path"], config["slurm_shell"]["parameters"])
            return slurm_shell_config
        
    def get_input_file_configs(self):
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file)
            input_file_configs = []
            for key in config:
                if key.startswith("input_file"):
                    input_file_onfig = Input_File_Config(config[key]["file_path"], config[key]["parameters"])
                    input_file_configs.append(input_file_onfig)
            return input_file_configs
    
    def get_output_file_configs(self):
        with open(self.config_file_path, 'r') as config_file:
            config = json.load(config_file)
            output_file_configs = []
            for key in config:
                if key.startswith("output_file"):
                    output_file_config = Output_File_Config(config[key].get("file_path",""), config[key].get("file_folder",""), config[key]["lines"],config[key].get("tag_line",""))
                    output_file_configs.append(output_file_config)
            return output_file_configs

# test
if __name__ == "__main__" :
	# config_path 为config_file.json
	# 打印所有get的部分
	config_path= "config.json"
	config_file = Config_File(config_path)
	slurm_shell_config = config_file.get_slurm_shell_config()
	input_file_configs = config_file.get_input_file_configs()
	output_file_configs = config_file.get_output_file_configs()
	print(slurm_shell_config.get_keys())
	print(input_file_configs[0].get_keys())
	print(output_file_configs[0].get_keys())
	print(output_file_configs[1].get_keys())
