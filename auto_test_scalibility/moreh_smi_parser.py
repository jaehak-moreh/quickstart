import re



def process_lines_containing_python(input_filename):
    # List to hold all lines containing 'python'
    relevant_lines = []
    sda_lines = []
    # Open the input file for reading
    with open(input_filename, 'r') as file:
        # Read through each line in the input file
        tmp_sda_line = '-1|-1|-1|-1|-1|-1|-1'
        for line in file:
            # Check if 'python' is in the line
            if 'xlarge' in line.lower():
                tmp_sda_line = line.strip()
            if 'python' in line.lower():  # This makes the search case-insensitive
                sda_lines.append(tmp_sda_line)
                relevant_lines.append(line.strip())
    return sda_lines, relevant_lines


def export_info(sda_lines, relevant_lines):
    datas = {}
    for s, l in zip(sda_lines, relevant_lines):
        tmp_s = s.split('|')
        sda_model = tmp_s[3]
        tmp_l = l.split('|')
        ops = tmp_l[4].split(' ')
        batch_size = ops[7]
        block_size = ops[9]
        mem_usage = int(tmp_l[5].replace('MiB', ''))

        distinct_name = f"{sda_model}_{batch_size}_{block_size}"
        if distinct_name not in datas:
            datas[distinct_name] = mem_usage
        elif datas[distinct_name] < mem_usage:
            datas[distinct_name] = mem_usage
    return datas


def print_info(datas):
    for k in datas:
        print(f"{k}'s max mem usage is {datas[k]}")




# Example usage
if __name__ == "__main__":
    # Path to the log file
    log_file = 'logs/moreh-smi-data.logs'

    # Call the function to process the file
    sda_lines, relevant_lines = process_lines_containing_python(log_file)
    datas = export_info(sda_lines, relevant_lines)
    print_info(datas)