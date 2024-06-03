import re
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
            # other type
            raise ValueError(f"Invalid file type: {self.file_type}")
    
    def extract_output_file_content(self, file_path):
        file_content = self.get_output_file_content(file_path)
        values = {}
        for line in self.lines:
            for word in line.split():
                if word.startswith('$'):
                    values[word[1:]] = None

        matched_line_index = 0
        for file_line in file_content.split('\n'):
            for line_index, line in enumerate(self.lines[matched_line_index:], start=matched_line_index):
                file_words = file_line.split()
                line_words = line.split()
                if len(file_words) < len(line_words):
                    continue
                match = True
                for file_word, line_word in zip(file_words, line_words):
                    if line_word != '?' and not line_word.startswith('$'):
                        if file_word != line_word:
                            match = False
                            break
                if match:
                    for word in line_words:
                        if word.startswith('$'):
                            values[word[1:]] = file_words[line_words.index(word)]
                    matched_line_index = line_index + 1
                    break
        return values