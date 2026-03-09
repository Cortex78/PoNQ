import os
import argparse
import yaml
import subprocess
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='compute all metrics')
    parser.add_argument('config', type=str, help='Path to config file.')
    parser.add_argument('-output_folder', type=str, default='out/', help='Path to test folder')
    parser.add_argument('-subd', type=int, default=0,
                        help='subdivision level.')
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        cfg = yaml.load(f, Loader=yaml.Loader)
    name = cfg["training"]["model_name"][5:-3]

    suffix = ""
    if args.subd == 1:
        suffix = "_lite"
    elif args.subd > 1:
        suffix = "_lite_{}".format(args.subd)

    python_executable = sys.executable or "python"

    subprocess.run([python_executable, "src/eval/eval_ABC.py", "{}/ABC_{}_32{}".format(args.output_folder, name, suffix)])
    subprocess.run([python_executable, "src/eval/eval_ABC.py", "{}/ABC_{}_64{}".format(args.output_folder, name, suffix)])
    subprocess.run([python_executable, "src/eval/eval_THINGI.py", "{}/Thingi_{}_32{}".format(args.output_folder, name, suffix)])
    subprocess.run([python_executable, "src/eval/eval_THINGI.py", "{}/Thingi_{}_64{}".format(args.output_folder, name, suffix)])
    subprocess.run([python_executable, "src/eval/eval_THINGI.py", "{}/Thingi_{}_128{}".format(args.output_folder, name, suffix)])
