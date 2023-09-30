import argparse
import os
import shutil
import cv2
import hashlib
from mtcnn.mtcnn import MTCNN

class BulkFaceExtractor:
    def __init__(self):
        self.detector = MTCNN()

    @staticmethod
    def hash_files(path_list, input_dir):
        for path in path_list:
            extension = os.path.splitext(path)[1]
            sha256 = hashlib.sha256()
            with open(path, "rb") as f:
                while chunk := f.read(8192):  # 8k chunks
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()
            os.rename(path, os.path.join(input_dir, file_hash + extension))

    @staticmethod
    def get_image_paths(folder):
        return [os.path.join(folder, image_name) for image_name in os.listdir(folder) if image_name.lower().endswith((".jpg", ".jpeg", ".png"))]

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        faces = self.detector.detect_faces(image)
        return [image[y:y+h, x:x+w] for face in faces for (x, y, w, h) in [face['box']]]

    @staticmethod
    def write_file(folder, image, base_name, face_count):
        file_name = f"{base_name}_{face_count}.jpg"
        cv2.imwrite(os.path.join(folder, file_name), image)

    def move_file(self, folder, image_path):
        shutil.move(image_path, os.path.join(folder, os.path.basename(image_path)))

    def process_dir(self, input_dir, output_dir, processed_dir, no_faces_dir):
        path_list = self.get_image_paths(input_dir)
        no_faces_detected = []

        if not path_list:
            print("Input directory is empty.")
            return

        print(f"{len(path_list)} images to process...")
        self.hash_files(path_list, input_dir)
        path_list = self.get_image_paths(input_dir)
        for image_path in path_list:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            faces = self.process_image(image_path)
            if not faces:
                no_faces_detected.append(base_name)
                self.move_file(no_faces_dir, image_path)
            else:
                for i, face in enumerate(faces, start=1):
                    self.write_file(output_dir, face, base_name, i)
                self.move_file(processed_dir, image_path)

        if no_faces_detected:
            print("No faces were detected in the following images:")
            for image_name in no_faces_detected:
                print(image_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path to input directory.")
    parser.add_argument("-o", "--output", default="Output", help="Path to output directory.")
    parser.add_argument("-p", "--processed", default="Processed", help="Path to processed directory.")
    parser.add_argument("-n", "--nofaces", default="No Faces", help="Path to No Faces directory.")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    if not os.path.exists(args.processed):
        os.makedirs(args.processed)
    if not os.path.exists(args.nofaces):
        os.makedirs(args.nofaces)

    BulkFaceExtractor().process_dir(args.input, args.output, args.processed, args.nofaces)
