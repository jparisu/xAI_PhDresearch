# This script check every .qmd file and check if there are any image that is got from the internet.
# This is when appears ![](http://....) in the .qmd file.
# In these cases, it dowloads the image by wget, save it in the images folder and replace the ![](http://....) by ![](images/....)

import os
import re
import wget


# Find every .qmd file with its path
def find_files():
    result = []
    for root, dirs, files in os.walk("../"):
        for file in files:
            if file.endswith(".qmd"):
                result.append((root, file))
    return result


# Return the URL if the line contains an image to download
def extract_image_url(markdown_line):
    # Check if the line is an image markdown with optional {} {}
    image_pattern = re.compile(r'!\[.*\]\(.*\)(\{.*\})?(\{.*\})?')
    url_pattern = re.compile(r'\((http[s]?://[^)]+)\)')

    if not image_pattern.match(markdown_line):
        return None

    # Extract the URL part
    url_match = url_pattern.search(markdown_line)

    if not url_match:
        return None

    return url_match.group(1)


# Download the image and save it in the images folder
def download_image(url, path, image_name):

    # If images folder does not exist, create it
    if not os.path.exists(path + "/images"):
        os.makedirs(path + "/images")

    image_path = path + "/images/" + image_name
    print(f"Downloading image: <{url}> in <{image_path}>")

    # Save the image in the images folder
    os.system(f"wget -O {image_path} {url}")
    # wget.download(url, out=image_path)


# Go line by line in the .qmd file and check if there is any image to download
def check_images(path, file):
    with open(path + "/" + file, 'r') as f:
        lines = f.readlines()

    result_lines = []
    for line in lines:
        # Check if there is an image to download
        url = extract_image_url(line)
        if url:
            image_name = url.split("/")[-1]
            download_image(url, path, image_name)
            line = line.replace(url, "images/" + image_name)
        result_lines.append(line)

    with open(path + "/" + file, 'w') as f:
        for line in result_lines:
            f.write(line)


# Main function
def main():
    files = find_files()
    for file in files:
        check_images(file[0], file[1])

if __name__ == "__main__":
    main()
