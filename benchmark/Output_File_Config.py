import subprocess


class Output_File_Config :
    def __init__(self, file_type, lines):
        self.file_type = file_type
        self.lines = lines
    
    def get_keys(self) :
        return self.file_type, self.lines
    
    def get_output_file_content(self, file_path):
        if self.file_type == "out":
            file_content = None
            with open(file_path, 'r') as file:
                file_content = file.read()
            return file_content
        elif self.file_type == "darshan":
            parser_path = '/thfs3/home/xjtu_cx/hugo/darshan-main/bin/darshan-parser'
            parsed_file_path = file_path + '.txt'
            command = f'{parser_path} {file_path} > {parsed_file_path}'
            subprocess.run(command, shell=True)
            file_content = None
            with open(parsed_file_path, 'r') as file:
                file_content = file.read()
            return file_content
        else :
            # othermode
            pass
    
    
    def extract_output_file_content(self, file_path):
        file_content = self.get_output_file_content(file_path)
        values = {}
        for line in self.lines:
            for word in line.split():
                if word.startswith('$'):
                    values[word[1:]] = None
        # 取出所有key对应的value
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