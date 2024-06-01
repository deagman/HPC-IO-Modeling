import csv
import os
import subprocess
import time

from benchmark.Config_File import Config_File
from benchmark.Test import Test
class Experiment:

    def __init__ (self, config_file_path):
        self.config_file = Config_File(config_file_path)
        self.name = self.config_file.get_name()
        self.mode = self.config_file.get_mode()
        self.result_folder = self.config_file.get_result_folder()
        self.batchsize = self.config_file.get_batchsize()
        self.slurm_shell_config = self.config_file.get_slurm_shell_config()
        self.input_file_configs = self.config_file.get_input_file_configs()
        self.test_type, self.output_file_configs = self.config_file.get_output_file_configs()

    # 生成一些文件夹
    # 检查result_folder是否存在，如果不存在则创建
    # 在result_folder下创建一个以name命名的文件夹，如果result_folder中已有name文件夹，则创建name_1文件夹
    # 在name文件夹下创建test文件夹，其个数为batchsize，名字分别是tests_0，tests_1，...
    def generate_folders(self):
        # 检查result_folder是否存在，如果不存在则创建
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

        # 在result_folder下创建一个以name命名的文件夹，如果result_folder中已有name文件夹，则创建name_1文件夹，如果再有，则创建name_2文件夹
        name_folder = os.path.join(self.result_folder, self.name)
        if os.path.exists(name_folder):
            i = 1
            while os.path.exists(f"{name_folder}_{i}"):
                i += 1
            name_folder = f"{name_folder}_{i}"
            # 更新name
            self.name = f"{self.name}_{i}"
        os.makedirs(name_folder)

        # 在name文件夹下创建test文件夹，其个数为batchsize，名字分别是tests_0，tests_1，...
        for i in range(self.batchsize):
            test_folder = os.path.join(name_folder, f"tests_{i}")
            os.makedirs(test_folder)

    
    def get_all_combinations(self):
        # params_combinations_0是一个slurm_shell的字典列表。
        # parmas_combinations_0 = [{'N':1}, {'N':2}，{'N':3}]
        params_combinations_0 = self.slurm_shell_config.combinate_parameters()
        # params_combinations_list是一个字典列表的列表，即 [ [],[],[] ]，长度为input_file_config的个数
        # params_combinations_list = [ [{'striping_factor':1}, {'striping_factor':2}], [{'striping_unit':'1M'}, {'striping_unit':'2M'}], ... ]
        params_combinations_list = [input_file_config.combinate_parameters() for input_file_config in self.input_file_configs]

        # 假设params_combinations_list中列表长度构成 = [3, 2, 2]
        # 现在会生成3*2*2=12个实验，[0 , 0 , 0]表示从第一个字典列表中取第一个字典，第二个字典列表中取第一个字典，第三个字典列表中取第一个字典
        # [0 , 0 , 1]表示从第一个字典列表中取第一个字典，第二个字典列表中取第一个字典，第三个字典列表中取第二个字典
        # 以此类推，最后直到[2, 1, 1]
        len_0 = len(params_combinations_0)
        len_x_list = [len(params_combinations_x) for params_combinations_x in params_combinations_list]
        len_list = [len_0] + len_x_list
        total_experiments = 1
        all_combinations = []
        for length in len_list:
            total_experiments *= length
        for i in range(total_experiments):
            combination_index = []
            remainder = i
            for length in reversed(len_list):
                remainder, index = divmod(remainder, length)
                combination_index.insert(0, index)
            all_combinations.append(combination_index)
        return all_combinations, params_combinations_0, params_combinations_list

    def allocate_nodes(self):
        # not working to use salloc in pycode, don't know why
        # need to salloc in terminal
        pass

    def run(self, all_combinations, params_combinations_0, params_combinations_list):
        if self.mode == 'batch':
            # tests_i文件夹存放当前批次第i个test
            for batch_start in range(0, len(all_combinations), self.batchsize):
                print(batch_start)
                slurm_job_ids = [None] * self.batchsize
                for i in range(self.batchsize) :
                    iter = batch_start + i
                    folder_path = os.path.join(self.result_folder, self.name, f'tests_{i}')
                    if batch_start + i < len(all_combinations):
                        combination = all_combinations[batch_start + i]
                        params_combination_list = []
                        params_combination_0 = params_combinations_0[combination[0]]
                        # 添加slurm_shell的参数
                        params_combination_list.append(params_combination_0)
                        slurm_shell_path = self.slurm_shell_config.generate_shell_file(params_combination_0, folder_path)
                        print("slurm_shell_path", slurm_shell_path)
                        # 为所有的input_file_configs生成文件
                        for input_file_config, params_combinations_x, index in zip(self.input_file_configs, params_combinations_list, combination[1:]):
                            # 第x个input_file的第index个参数组合
                            params_combination_x = params_combinations_x[index]
                            params_combination_list.append(params_combination_x)
                            input_file_config.generate_input_file(params_combination_x, folder_path)
                        # run test
                        print(self.test_type)
                        test = Test(self.mode, slurm_shell_path, folder_path, iter, self.test_type)
                        print("开始执行")
                        test.execute_shell_file()
                        slurm_job_ids[i] = test.get_slurm_job_id()
                        print("id", slurm_job_ids[i])
                # 检查当前批次任务是否全部完成
                while True:
                    squeue = subprocess.run(['squeue'], stdout=subprocess.PIPE)
                    queue = squeue.stdout.decode()
                    lines = queue.split('\n')
                    job_ids = [line.split()[0] for line in lines[1:] if line]
                    if any(job_id in slurm_job_ids for job_id in job_ids):
                        time.sleep(5)
                    else:
                        break   
        elif self.mode == 'sequential':
            folder_path = os.path.join(self.result_folder, self.name, 'tests_0')
            iter = 0
            # 开始执行
            for combination in all_combinations:
                params_combination_0 = params_combinations_0[combination[0]]
                params_combination_list = []
                # 添加slurm_shell的参数
                params_combination_list.append(params_combination_0)
                slurm_shell_path = self.slurm_shell_config.generate_shell_file(params_combination_0, folder_path)
                print("slurm_shell_path",slurm_shell_path)
                # 为所有的input_file_configs生成文件
                for input_file_config, params_combinations_x, index in zip(self.input_file_configs, params_combinations_list, combination[1:]):
                    # 第x个input_file的第index个参数组合
                    params_combination_x = params_combinations_x[index]
                    params_combination_list.append(params_combination_x)
                    input_file_config.generate_input_file(params_combination_x, folder_path)
                # run test
                test = Test(self.mode, slurm_shell_path, folder_path, iter, self.test_type)
                print("开始执行")
                test.execute_shell_file()
                iter += 1
        else :
            raise ValueError("Invalid mode")
    # 读取self.result_folder/self.name中，tests或者tests_0,tests_1, ...文件夹中名为test_iter.out的文件中的结果
    # 其中iter为0,1,2,..
    # iter为0,1,2,...表示第几次实验，和all_combinations中的combinations对应
    def extract_data(self, all_combinations, params_combinations_0, params_combinations_list):
        params_combinations_list.insert(0,params_combinations_0)
        data = []
        for i, combination in enumerate(all_combinations):
            params_combination_list = []
            for params_combinations_x, index in zip(params_combinations_list, combination):
                params_combination_list.append(params_combinations_x[index])
            tests_folder = os.path.join(self.result_folder, self.name, f'tests_{i % self.batchsize}')
            values_list = []
            for output_file_config in self.output_file_configs:
                file_type, _ = output_file_config.get_keys()
                file_path = os.path.join(tests_folder, f'test_{i}.{file_type}')
                values = output_file_config.extract_output_file_content(file_path)
                values_list.append(values)
            row = {}
            for d in params_combination_list + values_list:
                row.update(d)
            data.append(row)
        return data
    
    # data为一个字典列表，将其写入csv文件
    def write_to_csv(self, data):
        pass
    
    
    def extract_output_file_content(self, file_path, file_type, lines):
        # 读取file_path中的内容
        file_content = None
        if file_type == 'out' :
            with open(file_path, 'r') as file:
                file_content = file.read()
        elif file_type == 'darshan' :
            parser_path = '/thfs3/home/xjtu_cx/hugo/darshan-main/bin/darshan-parser'
            parsed_file_path = file_path + '.txt'
            command = f'{parser_path} {file_path} > {parsed_file_path}'
            subprocess.run(command, shell=True)
            with open(parsed_file_path, 'r') as file:
                file_content = file.read()
        else:
            # 其他类型
            pass
        # 取出lines中所有的key
        values = {}
        for line in lines:
            for word in line.split():
                if word.startswith('$'):
                    values[word[1:]] = None
        # 取出所有key对应的value
        for file_line in file_content.split('\n'):
            for line in lines:
                line_prefix = line.split('$')[0]
                if file_line.startswith(line_prefix):
                    # Split file_line and line by whitespace
                    file_values = file_line.split()[len(line_prefix.split()):]
                    line_values = line.split()[len(line_prefix.split()):]
                    # Pair up placeholder keys with their corresponding values
                    for key, value in zip(line_values, file_values):
                        if key.startswith('$'):  # Check if the key is a placeholder key
                            values[key[1:]] = value  # Remove the '$' and add to values dictionary
                    break  # Move to the next line in file_content
        return values

                

                




    
