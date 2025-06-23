import os
import re

def split_m3u_playlist(input_m3u_file, output_directory="individual_m3u_files"):
    """
    Splits a master M3U playlist into individual M3U files for each stream.

    Each stream, defined by an '#EXTINF' tag followed by its URL, will be
    extracted into its own .m3u file within the specified output directory.
    The filename for each individual M3U will be derived from the title
    found in the '#EXTINF' line, with sanitization for valid filenames.

    Args:
        input_m3u_file (str): The path to the input master M3U playlist file.
        output_directory (str): The directory where individual M3U files will be saved.
                                Defaults to "individual_m3u_files".
    """
    print(f"Starting the process of splitting M3U playlist: '{input_m3u_file}'.")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: '{output_directory}'")

    file_count = 0
    try:
        with open(input_m3u_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_extinf = None
        stream_url = None

        for i, line in enumerate(lines):
            line = line.strip()

            if line.startswith('#EXTINF:'):
                current_extinf = line
                # Extract title from the EXTINF line for use as a filename.
                # The regex captures text after the last comma.
                match = re.search(r'#EXTINF:.*?\,(.*?)$', line)
                if match:
                    title = match.group(1).strip()
                    # Sanitize the title to remove characters invalid for filenames.
                    title = re.sub(r'[\\/:*?"<>|]', '', title)
                    if not title: # Fallback if title is empty after sanitization
                        title = f"unknown_stream_{file_count}"
                else:
                    title = f"unknown_stream_{file_count}"
                
                # Check the next line for the stream URL.
                if i + 1 < len(lines):
                    next_line = lines[i+1].strip()
                    if not next_line.startswith('#'): # Assuming URL is the next non-comment line
                        stream_url = next_line
                        
                        # If both EXTINF and URL are found, write the individual M3U file.
                        base_output_filename = os.path.join(output_directory, f"{title}.m3u")
                        output_filename = base_output_filename
                        
                        # Ensure a unique filename if a file with the same name already exists.
                        counter = 1
                        while os.path.exists(output_filename):
                            output_filename = os.path.join(output_directory, f"{title}_{counter}.m3u")
                            counter += 1

                        with open(output_filename, 'w', encoding='utf-8') as outfile:
                            outfile.write("#EXTM3U\n") # Standard M3U header
                            outfile.write(f"{current_extinf}\n")
                            outfile.write(f"{stream_url}\n")
                        
                        print(f"Created individual M3U file: '{os.path.basename(output_filename)}'")
                        file_count += 1
                        
                        # Reset variables for the next stream entry.
                        current_extinf = None
                        stream_url = None
                
    except FileNotFoundError:
        print(f"Error: The input M3U file '{input_m3u_file}' was not found. Please verify the file path.")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")

    print(f"M3U playlist splitting complete. Total individual files created: {file_count}.")

if __name__ == "__main__":
    master_playlist_name = input("Please enter the name of your master M3U playlist file (e.g., my_master_playlist.m3u): ")
    split_m3u_playlist(master_playlist_name)
    print("\nOperation concluded. Ready for the next task.")