import subprocess
from benchmark.Output_File_Config import Output_File_Config

class Test :
    def __init__(self, mode, shell_file_path, result_folder, iteration, test_type):
        self.mode = mode
        self.shell_file_path = shell_file_path
        self.result_folder = result_folder
        self.iteration = iteration
        self.slurm_job_id = '0'
        self.test_type = test_type
    
    # slurm_job_id的唯一用处是检测某一批次中的任务是否执行完毕
    def get_slurm_job_id(self):
        return self.slurm_job_id
    
    def execute_shell_file(self):
        switch = {
            'batch': ["sbatch"],
            'sequential': ["sh"]
            # 其他模式
        }
        if self.mode not in switch:
            raise ValueError("Invalid mode")
        elif self.mode == 'batch':
            if self.test_type == "out":
                sbatch_options = ["--output", f"test_{self.iteration}.out"]
                # 因为要转移到result_folders，所以不必加上{self.result_folder}
                # 因为shell_file_path是和resul_folder相关，所以result_floder必须为绝对路径，不然shell_file_path只能是名称，而非路径
                # 这一点可以在intergration/Experiment中的congfig.json中验证
                command = switch[self.mode] + sbatch_options + [self.shell_file_path]
                # run in result_folders to avoid the same temp-files generated in program execution causing chaos
                submited_job = subprocess.run(command, capture_output=True, text=True, cwd=self.result_folder)
                if 'error' in submited_job.stderr:
                    self.slurm_job_id = '-1'
                    print(submited_job.stderr)
                else :
                    self.slurm_job_id = submited_job.stdout.split()[-1]
            elif self.test_type == "out+darshan" :
                sbatch_options = ["--output", f"test_{self.iteration}.out"]
                # ALL保证超算module相关环境能够加载进去
                export_options = [
                    "--export=ALL,"
                    "LD_PRELOAD=/thfs3/home/xjtu_cx/hugo/darshan-main/lib/libdarshan.so,"
                    f"DARSHAN_LOGFILE=test_{self.iteration}.darshan"
                    ]
                command = switch[self.mode] + export_options + sbatch_options + [self.shell_file_path]
                print(command)
                submited_job = subprocess.run(command, capture_output=True, text=True, cwd=self.result_folder)
                if 'error' in submited_job.stderr:
                    self.slurm_job_id = '-1'
                    print(submited_job.stderr)
                else :
                    self.slurm_job_id = submited_job.stdout.split()[-1]
            else :
                # 其他test_type
                pass
        elif self.mode == 'sequential':
            if self.test_type == "out":
                command = ' '.join(switch[self.mode] + [self.shell_file_path]) + f' > test_{self.iteration}.out'
                submited_job = subprocess.run(command, shell=True, text=True, cwd=self.result_folder)
            elif self.test_type == "out+darshan" :
                env_var = [f"LD_PRELOAD=/thfs3/home/xjtu_cx/hugo/darshan-main/lib/libdarshan.so",
                    f"DARSHAN_LOGFILE=test_{self.iteration}.darshan"
                    ]
                command = ' '.join(env_var + switch[self.mode] + [self.shell_file_path]) + f' > test_{self.iteration}.out'
                submited_job = subprocess.run(command, shell=True, text=True, cwd=self.result_folder)
            else :
                # 其他test_type
                pass
        else :
            # 其他模式
            pass