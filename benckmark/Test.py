import shlex
import subprocess
from Output_File_Config import Output_File_Config

class Test :
    def __init__(self, submit_cmd, shell_file_path, params_combination_list, output_file_configs):
        self.submit_cmd = submit_cmd
        self.shell_file_path = shell_file_path
        self.params_combination_list = params_combination_list
        self.output_file_configs = output_file_configs
        self.slurm_job_id = 0

    def execute_shell_file(self):
        command = shlex.split(self.submit_cmd) + [self.shell_file_path]
        mission_submited = subprocess.run(command, capture_output=True, text=True)
        # sbatch: error: Batch job submission failed: No partition specified or system default partition
        # Submitted batch job 2598002
        # 如果包含error字段，返回-1，表示提交失败
        if "error" in mission_submited.stderr:
            self.slurm_job_id = -1
        # 返回slurm job id
        else:
            self.slurm_job_id = mission_submited.stdout.split()[-1]

    def get_slurm_job_id(self):
        return self.slurm_job_id

    def extract_output_files_content(self):
        id = self.get_slurm_job_id()
        # 为每个config设置id
        for output_file_config in self.output_file_configs:
            output_file_config.set_slurm_job_id(id)
        # 获取每个config对应的文件内容
        output_files_content = [output_file_config.get_output_file_content() for output_file_config in self.output_file_configs]
        # 存入文件中的$值
        values_list = []
        for output_file_content, output_file_config in zip(output_files_content, self.output_file_configs):
            values = output_file_config.extract_file_content(output_file_content)
            values_list.append(values)
        return values_list
    
    def merge_params_and_values(self, values_list):
        data = {}
        for params_combination in self.params_combination_list:
            data.update(params_combination)
        for values in values_list:
            data.update(values)
        return data

# 测试test
if __name__ == "__main__":
    params_combination = {'t':'1m', 'b':'4m'}
    config = {
        "file_folder": "/thfs3/home/xjtu_cx/hugo/test/model1/",
        "lines": [
            "xfersize            : $transfersize MiB",
            "blocksize           : $blocksize MiB"
        ]
    }
    output_file_configs = [Output_File_Config(None, config['file_folder'], config['lines'])]
    test = Test('sbatch -p thcp3','slurm_shell.sh_generated', [params_combination], output_file_configs)
    test.execute_shell_file()
    print("slurm_job_id", test.get_slurm_job_id())
    values_list = test.extract_output_files_content()
    print("values_list", values_list)
    data = test.merge_params_and_values(values_list)
    print("data", data)

    
    
