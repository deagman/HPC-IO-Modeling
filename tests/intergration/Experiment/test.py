import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from benchmark.Experiment import Experiment

# test
if __name__ == "__main__":
    config_file_path = 'config.json'
    result_file_path = 'result.csv'
    experiment = Experiment(config_file_path)
    all_combinations, params_combinations_0, params_combinations_list = experiment.get_all_combinations()
    # experiment.allocate_nodes() # not implemented
    experiment.generate_folders()
    experiment.run(all_combinations, params_combinations_0, params_combinations_list)
    data = experiment.extract_data(all_combinations, params_combinations_0, params_combinations_list)
    print(data)