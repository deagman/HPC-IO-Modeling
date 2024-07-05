import re
import subprocess


class Output_File_Config :
    def __init__(self, file_type, file_improc, lines):
        self.file_type = file_type
        self.file_improc = file_improc
        self.lines = lines
    
    def get_keys(self) :
        return self.file_type, self.file_improc, self.lines
    
    def get_output_file_content(self, file_path):
        if self.file_type == "out":
            file_content = None
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
            except FileNotFoundError:
                error_message = f"Error: The file '{file_path}' was not found."
                print(error_message)
            return file_content
        elif self.file_type == "darshan":
            file_content = None
            command = None
            if self.file_improc == "darshan-parser":
                parser_path = '/thfs3/home/xjtu_cx/hugo/darshan-main/bin/darshan-parser'
                parsed_file_path = file_path + '.txt'
                command = f'{parser_path} {file_path} > {parsed_file_path}'
            elif self.file_improc == "darshan-parser --total":
                parser_path = '/thfs3/home/xjtu_cx/hugo/darshan-main/bin/darshan-parser'
                parsed_file_path = file_path + '.total'
                command = f'{parser_path} --total {file_path} > {parsed_file_path}'
            elif self.file_improc == "darshan-parser --perf":
                parser_path = '/thfs3/home/xjtu_cx/hugo/darshan-main/bin/darshan-parser'
                parsed_file_path = file_path + '.perf'
                command = f'{parser_path} --perf {file_path} > {parsed_file_path}'
            else :
                raise ValueError(f"Invalid file intermediate processing: {self.file_improc}")
            subprocess.run(command, shell=True)
            with open(parsed_file_path, 'r') as file:
                 file_content = file.read()
            return file_content
        else :
            # other type
            raise ValueError(f"Invalid file type: {self.file_type}")
    
    def extract_output_file_content(self, file_path):
        file_content = self.get_output_file_content(file_path)
        values = {}
        if file_content is None:
            return values
        for line in self.lines:
            for word in line.split():
                if word.startswith('$'):
                    values[word[1:]] = None

        matched_line_index = 0
        for file_line in file_content.split('\n'):
            if matched_line_index >= len(self.lines):
                break
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