# TritonMetricAnalyzer

Some simplified code to process and print the Triton server-side metrics to help understand the performances.

## dump the server-side metrics

The server-side metrics can be curled and saved with e.g.,
```
curl localhost:8022/metrics > run.log
```

The output follows the prometheus format and should look like [this log file](testdata/result2.log).

## analyze and print the metrics

Analyze the metrics and print out the information by
```
python3 test.py
```
in which if two parameters are passed to `print_info`, it will take the difference and print out the information. This is very useful in the cases where the first few inferences are very slow. One could log the first few slow ones first. Then log the 2nd time with all the inferences. `print_info` will calculate the difference and print out the 2nd part which should be faster. Otherwise if one log file is passed it will process and print out the information saved in the that log file.
