from modules.loganalyzer import process_file, print_info

models_1st = process_file("./testdata/result1.log")
models_2nd = process_file("./testdata/result2.log")

# print out the information of the 1st log file
#print_info(models_1st)

# print out the information between 1st log and 2nd log
print_info(models_1st, models_2nd)
