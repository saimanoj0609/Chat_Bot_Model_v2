import pdfplumber
import os
import re
from difflib import get_close_matches


def pdf_data_extractor(pdf_path, input_file_path, output_file_path):
    # Open the PDF file and the output text file
    with pdfplumber.open(pdf_path) as pdf, open(input_file_path, 'w', encoding='utf-8') as output_file:
        for i in range(23, 192):
            tables = pdf.pages[i].extract_tables()
            if tables:
                output_file.write(f"Page {i + 1} Tables:\n")
                for table in tables:
                    for row in table:
                        output_file.write("\t".join(map(str, row)) + "\n")  # Join row elements with a tab
                    output_file.write("\n")  # Add a newline for better separation between tables
            else:
                output_file.write(f"Page {i + 1} has no tables.\n")

    commands_dict = {}

    # Read the content of the text file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize variables to hold the current key and its associated value
    current_key = None
    current_value = []

    # Process each line in the file
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith("Page"):  # Skip page headers
            continue
        if line.endswith('None'):  # If the line is a command
            if current_key is not None:  # If we already have a key
                # Append the current value to the dictionary
                if current_key in commands_dict:
                    commands_dict[current_key].extend(current_value)
                else:
                    commands_dict[current_key] = current_value
            # Set the new key and reset the value list
            current_key = line.replace("None", "").replace("\t", " ")
            current_value = []
        else:
            # If the line is not a command, add it to the current value
            current_value.append(line)

    # Don't forget to save the last command after the loop
    if current_key and current_value:
        if current_key in commands_dict:
            commands_dict[current_key].extend(current_value)
        else:
            commands_dict[current_key] = current_value

    # Join the values into a single string for readability
    for key, value in commands_dict.items():
        commands_dict[key] = '\n'.join(value)


    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for key, value in commands_dict.items():
            output_file.write(f"{key}:\n")
            output_file.write(value)
            output_file.write("\n\n")

    print(f"Parsed commands have been saved to {output_file_path}.")
    return commands_dict