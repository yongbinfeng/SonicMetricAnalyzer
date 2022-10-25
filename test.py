from modules.loganalyzer import process_file, print_info
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--log', help='foo help')
parser.add_argument('--log2', help='Path to output log2 file', default=None)
args = parser.parse_args()


# process_file will return a collection of results in that log file, each model with their counts and latency.
results_1st = process_file(args.log)

if args.log2:
    results_2nd = process_file(args.log2)
    # print out the information between 1st and 2nd log file
    print_info(results_1st, results_2nd)

else:
    # print out the information of the 1st log file
    print_info(results_1st)