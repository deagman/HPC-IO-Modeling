import csv

from Config_File import Config_File
from Slurm_Shell_Config import Slurm_Shell_Config
from Input_File_Config import Input_File_Config
from Output_File_Config import Output_File_Config
from Test import Test

class Experiment:
    def __init__ (self, config_file_path, result_file_path):
        self.config_file = Config_File(config_file_path)
        self.result_file_path = result_file_path
    
    def get_slurm_shell_config(self):
        return self.config_file.get_slurm_shell_config()
    
    def get_input_file_configs(self):
        return self.config_file.get_input_file_configs()

    def get_output_file_configs(self):
        return self.config_file.get_output_file_configs()
    
    def write_to_csv(result_file_path, slurm_job_id, values):
        # 创建表头
        fieldnames = ['slurm_job_id'] + list(values.keys())

        # 检查文件是否已存在，如果不存在则写入表头
        try:
            with open(result_file_path, 'x', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass

        # 写入数据
        with open(result_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            row = {'slurm_job_id': slurm_job_id}
            row.update(values)
            writer.writerow(row)
    
    def run(self):
        slurm_shell_config = self.get_slurm_shell_config()
        input_file_configs = self.get_input_file_configs()
        output_file_configs = self.get_output_file_configs()
        print('slurm_shell_config: ', slurm_shell_config.get_keys())
        print('input_file_configs: ', [input_file_config.get_keys() for input_file_config in input_file_configs])
        print('output_file_configs: ', [output_file_config.get_keys() for output_file_config in output_file_configs])
        
        # params_combinations_0是一个字典列表。
        # parmas_combinations_0 = [{'N':1}, {'N':2}，{'N':3}]
        params_combinations_0 = slurm_shell_config.combinate_parameters()
        # params_combinations_list是一个字典列表的列表，即 [ [],[],[] ]
        # params_combinations_list = [ [{'striping_factor':1}, {'striping_factor':2}], [{'striping_unit':'1M'}, {'striping_unit':'2M'}], ... ]
        params_combinations_list = [input_file_config.combinate_parameters() for input_file_config in input_file_configs]
        # 现在要依次取出每一个字典列表中的一个字典，然后生成对应的文件
        # 即{'N':1}和{'striping_factor':1}和{'striping_unit':'1M'}
        # 以上构成一次总的参数组合，下一次为
        # {'N':1}和{'striping_factor':1}和{'striping_unit':'2M'}
        len_0 = len(params_combinations_0)
        len_x_list = [len(params_combinations_x) for params_combinations_x in params_combinations_list]
        len_list = [len_0] + len_x_list
        # 假设len_list = [3, 2, 2]
        # 现在会生成6*2*2=24个实验，[0 , 0 , 0]表示从第一个字典列表中取第一个字典，第二个字典列表中取第一个字典，第三个字典列表中取第一个字典
        # [0 , 0 , 1]表示从第一个字典列表中取第一个字典，第二个字典列表中取第一个字典，第三个字典列表中取第二个字典
        # [0 , 1 , 0]表示从第一个字典列表中取第一个字典，第二个字典列表中取第二个字典，第三个字典列表中取第一个字典
        # 以此类推，最后直到[2, 1, 1]
        # 如果len_list = [4,3,3]，则会生成4*3*3=36个实验
        # 使用一个计数方法，从[0,0,0]开始，每次加1，直到[3,2,2]，即可生成所有的实验
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
        
        # 开始执行
        for combination in all_combinations:
            params_combination_0 = params_combinations_0[combination[0]]
            params_combination_list = []
            # 添加0
            params_combination_list.append(params_combination_0)
            # 为slurm_shell_config生成脚本文件
            slurm_shell_path = slurm_shell_config.generate_shell_file(params_combination_0)
            # 为所有的input_file_configs生成文件
            for input_file_config, params_combinations_x, index in zip(input_file_configs, params_combinations_list, combination[1:]):
                params_combination_x = params_combinations_x[index]
                params_combination_list.append(params_combination_x)
                input_file_config.generate_input_file(params_combination_x)

            # run test
            test = Test(slurm_shell_config.get_submit_cmd(), slurm_shell_path, params_combination_list, output_file_configs)
            test.execute_shell_file()
            slurm_job_id = test.get_slurm_job_id()
            print('slurm_job_id: ', slurm_job_id)
            values_list = test.extract_output_files_content()
            data = test.merge_params_and_values(values_list)

            # write data to csv
            fieldnames = ['slurm_job_id'] + list(data.keys())
            # 检查文件是否已存在，如果不存在则写入表头
            try:
                with open(self.result_file_path, 'x', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
            except FileExistsError:
                pass

            # 写入单次test数据
            with open(self.result_file_path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                row = {'slurm_job_id': slurm_job_id}
                row.update(data)
                writer.writerow(row)

# test
if __name__ == "__main__":
    config_file_path = '/thfs3/home/xjtu_cx/hugo/test/model/experiment1/tests-1/config-1.json'
    result_file_path = '/thfs3/home/xjtu_cx/hugo/test/model/experiment1/tests-1/result-1.csv'
    experiment = Experiment(config_file_path, result_file_path)
    experiment.run()

            

                

                




    
