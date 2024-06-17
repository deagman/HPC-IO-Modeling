import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from benchmark.Experiment import Experiment

# test
if __name__ == "__main__":

    config_file_path = 'config.json'
    experiment = Experiment(config_file_path)
    all_combinations, params_combinations_0, params_combinations_list = experiment.get_all_combinations()
    # if sequential, experiment.allocate_nodes() # not implemented
    experiment.generate_folders()
    experiment.run(all_combinations, params_combinations_0, params_combinations_list)
    data = experiment.extract_data(all_combinations, params_combinations_0, params_combinations_list)
    experiment.write_to_csv(data)

    # # 如果试验意外中止了，想要继续试验，可以使用下面的代码
    # config_file_path = 'config.json'
    # experiment = Experiment(config_file_path)
    # all_combinations, params_combinations_0, params_combinations_list = experiment.get_all_combinations()
    # # 删去generate_folders()函数
    # experiment.run(all_combinations, params_combinations_0, params_combinations_list) # 输入测试新的起始
    # data = experiment.extract_data(all_combinations, params_combinations_0, params_combinations_list) # 输入测试新的起始
    # experiment.write_to_csv(data)

    # 如果试验中止，但是不想继续试验，而是只想提取数据，可以使用下面的代码
    # config_file_path = 'config.json'
    # experiment = Experiment(config_file_path)
    # all_combinations, params_combinations_0, params_combinations_list = experiment.get_all_combinations()
    # # 删去generate_folders()函数
    # # 删去run()函数
    # data = experiment.extract_data(all_combinations, params_combinations_0, params_combinations_list, 0, 75) # 输入测试的开始和结束
    # experiment.write_to_csv(data)