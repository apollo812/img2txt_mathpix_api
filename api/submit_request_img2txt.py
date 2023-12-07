import os
import gc
import time
import shutil
import random
import argparse
from pathlib import Path

from util.image_sender import ImageSender

def generate_test_list(test_dir):
    # Initialize
    input_list = []
    output_list = []

    # Iterate through each subfolder in the root directory
    for subdir in sorted(os.listdir(test_dir)):
        subdir_path = os.path.join(test_dir, subdir)

        # Check if it's a directory
        if os.path.isdir(subdir_path):
            # Construct paths for payload.json and output.png
            input_path = os.path.join(subdir_path, "input.jpg")
            output_path = os.path.join(subdir_path, "output.text")

            # Check if payload.json and output.png exist in the folder
            if os.path.isfile(input_path):
                input_list.append(input_path)

            # Add image path
            output_list.append(output_path)

    return input_list, output_list


def main(args):
    """
    main entry point
    """
    # Generate payload and image lists
    input_list, output_list = generate_test_list(args.test_dir)

    # Loop over number of requests
    for i in range(len(input_list)):
    
        # Timer
        start_time = time.time()

        # Instantiate class
        image_sender = ImageSender(args.api_url)

        # Send image
        image_sender.send_image(input_list[i])

        # Print time
        end_time = time.time()
        msg = f"Total processing time for payload no. {str(i)}: {end_time - start_time} seconds"
        print(msg)
    
    # Delete class objects and clean the buffer memory using the garbage collection
    gc.collect()


if __name__ == "__main__":
    """
    Form command lines
    """
    # Clean up buffer memory
    gc.collect()

    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Test directory
    test_dir = os.path.join(current_dir, "test", "regression_img2txt")

    # Output directory
    output_dir = os.path.join(current_dir, "results")
    
    # URL
    api_url = "http://localhost:5000/img2txt_url"

    parser = argparse.ArgumentParser(description="Convert image to text using MathPIX API.")
    parser.add_argument("--api_url", type=str, default=api_url, help="URL to send the POST request to")
    parser.add_argument("--test_dir", type=Path, default=test_dir, help="test directory")
    parser.add_argument("--output_dir", type=Path, default=output_dir, help="output images directory")
    args = parser.parse_args()

    # main call
    main(args)
