import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from benchmark.Slurm_Shell_Config import Slurm_Shell_Config
from benchmark.Input_File_Config import Input_File_Config
from benchmark.Output_File_Config import Output_File_Config
from benchmark.Test import Test

if __name__ == "__main__":
    # file_path = "./templates/slurm_shell_template"
    # parameters = {
    #     "transfersize, blocksize": ["1m, 4m", "4m, 16m"],
    #     "segment" : ["1", "4"],
    #     "nodes, ntasks": ["1, 16", "2, 32"]
    # }
    # slurm_shell_config = Slurm_Shell_Config(file_path, parameters)
    # params_combinations = slurm_shell_config.combinate_parameters()
    # print(params_combinations)
    # slurm_shell = slurm_shell_config.generate_shell_file(params_combinations[1],"./")

    # file_path = "./templates/input_file_template"
    # parameters = {
    #     "__striping_unit" : ["1048576","2097152"],
    #     "__striping_factor" : ["1", "2"]
    # }
    # input_file_config = Input_File_Config(file_path, parameters)
    # params_combinations = input_file_config.combinate_parameters()
    # print(params_combinations)
    # input_file = input_file_config.generate_input_file(params_combinations[3], "./")

    file_type = "out"
    lines = [
        "IO_bandwith = $io_bw",
        "IO_runtime = $io_rt1",
        "IO_runtime = $io_rt2",
        "IO_throughput = $io_tp_1 ? $io_tp_2"
    ]
    output_file_config = Output_File_Config(file_type, lines)
    file_content = output_file_config.get_output_file_content("./templates/output_file_template")
    values = output_file_config.extract_output_file_content("./templates/output_file_template")
    print(values)

    # file_type = "darshan"
    # lines = [
    #     "MPI-IO -1 ? MPIIO_INDEP_OPENS $mpiio_indep_opens",
    #     "MPI-IO -1 ? MPIIO_COLL_OPENS $mpiio_coll_opens",
    #     ]
    # output_file_config = Output_File_Config(file_type, lines)
    # file_content = output_file_config.get_output_file_content("./templates/test_0.darshant")
    # values = output_file_config.extract_output_file_content1("/thfs3/home/xjtu_cx/hugo/test/HPC-IO-Modeling/tests/unit/Config_and_Test/templates/test_0.darshan.txt")
    # print(values)

    # mode = 'sbatch'
    # shell_file = "./templates/slurm_shell"
    # test = Test(mode,shell_file,'./',1,"out")
    # test.execute_shell_file()
    # print(test.get_slurm_job_id())
