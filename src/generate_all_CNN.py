import os
import argparse
import subprocess
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='evaluate CNN')
    parser.add_argument('config', type=str, help='Path to config file.')
    parser.add_argument('-subd', type=int, default=0, help='Subdivision level')
    args = parser.parse_args()

    python_executable = sys.executable or "python"

    subprocess.run([python_executable, "src/utils/generate_mesh_CNN.py", args.config, "-grid_n", "33", "-subd", str(args.subd)])
    subprocess.run([python_executable, "src/utils/generate_mesh_CNN.py", args.config, "-grid_n", "65", "-subd", str(args.subd)])
    subprocess.run([python_executable, "src/utils/generate_mesh_CNN.py", args.config, "-dataset", "Thingi", "-grid_n", "33", "-subd", str(args.subd)])
    subprocess.run([python_executable, "src/utils/generate_mesh_CNN.py", args.config, "-dataset", "Thingi", "-grid_n", "65", "-subd", str(args.subd)])
    subprocess.run([python_executable, "src/utils/generate_mesh_CNN.py", args.config, "-dataset", "Thingi", "-grid_n", "129", "-subd", str(args.subd)])
