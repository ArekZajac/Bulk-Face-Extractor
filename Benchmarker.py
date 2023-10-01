import time
from collections import defaultdict
from BulkFaceExtractor import BulkFaceExtractor
import os
import argparse

class TimingStats:
    def __init__(self):
        self.call_times = []

    def add_time(self, t):
        self.call_times.append(t)

    def get_stats(self):
        return {
            "min": round(min(self.call_times) * 1000) if self.call_times else 0,
            "max": round(max(self.call_times) * 1000) if self.call_times else 0,
            "avg": round((sum(self.call_times) / len(self.call_times)) * 1000) if self.call_times else 0
        }

class Benchmarker(BulkFaceExtractor):
    def __init__(self):
        super().__init__()
        self.timing_stats = defaultdict(TimingStats)

    def time_method(self, method, *args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        elapsed_time = time.time() - start_time
        self.timing_stats[method.__name__].add_time(elapsed_time)
        return result

    def hash_files(self, path_list, input_dir):
        return self.time_method(super().hash_files, path_list, input_dir)

    def get_image_paths(self, folder):
        return self.time_method(super().get_image_paths, folder)

    def process_image(self, image_path):
        return self.time_method(super().process_image, image_path)

    def write_file(self, folder, image, base_name, face_count, x, y, w, h):
        return self.time_method(super().write_file, folder, image, base_name, face_count, x, y, w, h)

    def move_file(self, folder, image_path):
        return self.time_method(super().move_file, folder, image_path)

    def process_dir(self, input_dir, output_dir, processed_dir, no_faces_dir):
        super().process_dir(input_dir, output_dir, processed_dir, no_faces_dir)
        print("Timing statistics (ms):")
        for method_name, stats in self.timing_stats.items():
            print(f"{method_name}: {stats.get_stats()}")

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

    Benchmarker().process_dir(args.input, args.output, args.processed, args.nofaces)
