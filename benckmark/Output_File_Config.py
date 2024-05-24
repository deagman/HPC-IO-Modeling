import os
import time
class Output_File_Config :
    def __init__(self, file_path, file_folder, lines, tag_line):
        self.file_path = file_path
        self.file_folder = file_folder
        self.lines = lines
        self.tag_line = tag_line
    
    def get_keys(self) :
        return self.file_path, self.file_folder, self.lines, self.tag_line
    
    def set_slurm_job_id(self, slurm_job_id):
        self.slurm_job_id = slurm_job_id
    
    # 如果是文件夹，搜索带有 slurm_job_id 的文件，提取内容，如果不是文件夹，直接提取内容
    def get_output_file_content(self):
        if self.file_path and self.file_folder:
            raise ValueError("Both file_path and file_folder are set. Only one should be set.")
        elif self.file_path:
            if not os.path.exists(self.file_path):
                raise ValueError(f"Invalid file path: {self.file_path}")
            with open(self.file_path, 'r') as output_file:
                output_content = output_file.read()
                return output_content
        # 文件生成和文件内容写入均有延迟，需要等待
        elif self.file_folder:
            if not os.path.isdir(self.file_folder):
                raise ValueError(f"Invalid directory path: {self.file_folder}")
            if self.slurm_job_id == -1:
                return None
            while True:
                try:
                    for root, dirs, files in os.walk(self.file_folder):
                        for file in files:
                            if self.slurm_job_id in file:
                                while True :
                                    with open(os.path.join(root, file), 'r') as output_file:
                                        output_content = output_file.read()
                                        if self.tag_line in output_content :
                                                return output_content
                                        else:
                                            time.sleep(2)
                    raise ValueError(f"No output file found for slurm_job_id: {self.slurm_job_id}")
                except ValueError:
                    time.sleep(1)
        else :
            raise ValueError("Neither file_path nor file_folder is set.")
        
    def extract_file_content(self, file_content):
        # 对values进行初始化，即生成所有key值，但是value为空
        values = {}
        for line in self.lines:
            for word in line.split():
                if word.startswith('$'):
                    values[word[1:]] = None
        # Extract values corresponding to placeholders
        # 对于line中有相同前缀的line，取最后一个
        for file_line in file_content.split('\n'):
            for line in self.lines:
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

# test
if __name__ == "__main__":
    lines =  [
        "IO_bandwith = $io_bw",
        "IO_runtime = $io_rt",
        "IO_throughput = $io_tp_1 ??? $io_tp_2"
    ]
    tag_line = "Summary of all tests:"
    output_file = Output_File_Config('output.txt', None, lines, tag_line)
    file_content = output_file.get_output_file_content()
    print(output_file.extract_file_content(file_content))
