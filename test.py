from modules.loganalyzer import process_file, print_info

models_1st = process_file("./testdata/result1.log")
models_2nd = process_file("./testdata/result2.log")

print_info(models_1st, models_2nd)
