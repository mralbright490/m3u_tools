import os
import argparse

def combine_m3u_files(input_directory="individual_m3u_files", output_file="combined_master_playlist.m3u"):
    """
    Combines all individual M3U files from a specified directory into a single master M3U playlist.

    The function iterates through the given input directory, identifies all files
    ending with '.m3u', and appends their content to a new master playlist file.
    It automatically adds the '#EXTM3U' header to the combined file and
    skips existing '#EXTM3U' headers from the individual files to prevent duplication.

    Args:
        input_directory (str): The path to the directory containing the individual M3U files.
                               Defaults to "individual_m3u_files".
        output_file (str): The name and path of the new combined master M3U playlist file.
                           Defaults to "combined_master_playlist.m3u".
    """
    print(f"Initiating combination of M3U files from '{input_directory}' into '{output_file}'.")

    if not os.path.exists(input_directory):
        print(f"Error: The input directory '{input_directory}' does not exist. Please ensure the directory is valid and contains M3U files.")
        return

    combined_content = []
    # Ensure the new combined file starts with the standard M3U header.
    combined_content.append("#EXTM3U\n")

    m3u_found = False
    
    try:
        # Traverse the input directory to locate all .m3u files.
        for root, _, files in os.walk(input_directory):
            for filename in files:
                if filename.lower().endswith('.m3u'):
                    m3u_file_path = os.path.join(root, filename)
                    m3u_found = True
                    print(f"Processing file: '{filename}'")
                    with open(m3u_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            stripped_line = line.strip()
                            # Skip blank lines and the '#EXTM3U' header from individual files
                            # to avoid redundant headers in the combined file.
                            if stripped_line and stripped_line.lower() != '#extm3u':
                                combined_content.append(line) # Preserve original line endings.

        if not m3u_found:
            print(f"No .m3u files were found in the directory '{input_directory}'. Ensure that the directory contains M3U files for combination.")
            return

        # Write the aggregated content to the specified output file.
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(combined_content)

        print(f"\nSuccessfully combined all M3U files into: '{output_file}'")
        print("Master playlist creation complete.")

    except Exception as e:
        print(f"An error occurred during the file combination process: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combines multiple M3U files into a single master M3U playlist.")
    parser.add_argument("--input_dir", default="individual_m3u_files",
                        help="The directory containing the individual M3U files (default: individual_m3u_files)")
    parser.add_argument("--output_file", default="combined_master_playlist.m3u",
                        help="The name of the new combined master M3U playlist file (default: combined_master_playlist.m3u)")

    args = parser.parse_args()

    combine_m3u_files(args.input_dir, args.output_file)
    print("\nOperation concluded. The script is ready for further tasks.")