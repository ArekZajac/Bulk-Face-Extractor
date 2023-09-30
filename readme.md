# Bulk Face Extractor

Bulk Face Extractor utilizes OpenCV and MTCNN to detect and extract faces from a bulk of images. The project processes images in a given directory, extracts faces, and saves the cropped faces in an output directory. Additionally, it organizes the processed images by moving them to specific folders based on whether faces are detected in those images. Each processed image is renamed to the hash value of itself for easy identification and tracking.

## Dependencies

- Python 3.7 or higher
- OpenCV
- MTCNN

Install dependencies by running:
```bash
pip install -r requirements.txt
```

## Usage
```bash
$ python BulkImageExtractor.py -i INPUT_DIR -o OUTPUT_DIR -p PROCESSED_DIR -n NO_FACES_DIR
```

- `-i`, `--input`: (Required) Path to the input directory containing images to process.
- `-o`, `--output`: (Optional) Path to the output directory where the cropped faces will be stored. Default is output.
- `-p`, `--processed`: (Optional) Path to the directory where images with detected faces are moved after processing. Default is processed.
- `-n`, `--nofaces`: (Optional) Path to the directory where images with no detected faces are moved after processing. Default is No Faces.

## Functionality

- Processes images in the specified input directory.
- Extracts and saves faces in the output directory.
- Moves processed images to "processed" or "No Faces" directories based on face detection results.
- Renames the images using their SHA-256 for easy identification and tracking.