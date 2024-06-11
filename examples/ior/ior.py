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

    # 如果试验中止，只跑了部分测试，则重新执行上述代码，并且在generate_folders提示输入new name时press enter，以继续上次试验
    # 同时在run函数和extrac_data函数中指定star和end