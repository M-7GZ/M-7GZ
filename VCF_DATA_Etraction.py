# final code

import os
import re  # Added for regex support

def ask_for_file_location():
    while True:
        input_file_location = input("Enter the location of the input file: ")

        # Check if the file exists
        if os.path.isfile(input_file_location):
            print(f"File found at: {input_file_location}")
            return input_file_location  # Return the valid file location
        else:
            print("Invalid file location. Please try again.")


def starting_line(prompt="What is the first line of data? "):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if value > 0:  # Ensure the line number is positive
                return value
            else:
                print("Line number must be positive. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def extract_data():
    # Get the starting line number from the user
    line_number = starting_line()
    # Skip lines until reaching the specified starting line
    for _ in range(line_number-1):
        next(f_in)

    # Iterate through each line starting from the specified line
    for line in f_in:
        # Check if the line is empty or does not contain enough fields
        if not line.strip() or len(line.strip().split('\t')) < 8:
            print("Skipping line:", line.strip())
            continue

        # Extract relevant information from the line
        parts = line.strip().split('\t')
        chromosome = parts[0]
        position = parts[1]
        ref_allele = parts[3]
        alt_allele = parts[4]
        quality_score = parts[5]
        filter_status = parts[6]

        # Try to split the annotation field
        annotation_field = parts[7]
        annotations_list = annotation_field.split(',')

        # Process the first annotation
        first_annotation = annotations_list[0]
        annotation_parts = first_annotation.split('|')

        # If the annotation parts don't have enough data, search for "ANN="
        if len(annotation_parts) < 4:
            ann_index = annotation_field.find('ANN=')
            if ann_index != -1:
                # Start splitting from the "ANN=" position
                annotations_list = annotation_field[ann_index:].split(',')
                first_annotation = annotations_list[0]
                annotation_parts = first_annotation.split('|')

        # Extract annotation data
        annotations = annotation_parts[1:4]  # Fields after the first pipe

        # Write the extracted information to the output file
        output_line = '\t'.join(
            [chromosome, position, ref_allele, alt_allele, quality_score, filter_status] + annotations)
        f_out.write(output_line + '\n')
        print("Extracted:", output_line)


def remove_lines_with_keywords(input_file_path, keywords):
    output_file_path = os.path.splitext(input_file_path)[0] + "_filtered.txt"  # New file in the same directory with "_filtered" suffix
    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    # Filter out lines containing any keyword or word starting with 'PY00'
    filtered_lines = [
        line for line in lines
        if not any(keyword in line for keyword in keywords) and not re.search(r'\bPY00\w*', line)
    ]

    with open(output_file_path, 'w') as output_file:
        output_file.writelines(filtered_lines)

    return output_file_path


if __name__ == "__main__":
    # Call the function
    file_location = ask_for_file_location()

    # Extract the directory path from the input file location
    input_directory = os.path.dirname(file_location)

    # Define the output file path in the same directory as the input file
    output_file_path = os.path.join(input_directory, 'output_file.txt')

    # Open the input file for reading and the output file for writing
    with open(file_location, 'r', encoding='utf-16') as f_in, open(output_file_path, 'w') as f_out:
        print("Input file:", file_location)
        print("Output file:", output_file_path)
        extract_data()

    # Part 2: Remove specified keywords and lines with words starting with "PY00"
    input_file_path = output_file_path
    keywords_input = input("Enter the keywords to remove (separated by commas): ")
    keywords = [keyword.strip() for keyword in keywords_input.split(",")]

    # Remove lines containing keywords or starting with "PY00" and save to the output file
    output_file_path = remove_lines_with_keywords(input_file_path, keywords)

    print("Lines containing the specified keywords or words starting with 'PY00' removed from the input file and saved into the output file")
