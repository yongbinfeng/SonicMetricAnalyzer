from modules.loganalyzer import process_file, print_info

# process_file will return a collection of results in that log file, each model with their counts and latency.
results_1st = process_file("./testdata/result1.log")
results_2nd = process_file("./testdata/result2.log")

# print out the information of the 1st log file
#print_info(results_1st)

# print out the information between 1st log and 2nd log
print_info(results_1st, results_2nd)
