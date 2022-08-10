# TritonMetricAnalyzer

Some simplified code to process and print the Triton server-side metrics to help understand the performances.

## dump the server-side metrics

The server-side metrics can be curled and saved with e.g.,
```
curl localhost:8022/metrics > run.log
```

The output follows the prometheus format and should look like [this log file](testdata/result2.log).

Sometimes the first few inferences can be very slow, due to some initialization or warm-up processes. In these cases dump the first few inference metrics first and save them into one log file; wait till the end, dump all the inference metrics 2nd time and save them into another log file. [test.py](test.py) can substract and calculate the difference.

## analyze and print the metrics

Analyze the metrics and print out the information by
```
python3 test.py
```
in which if two parameters are passed to `print_info`, it will take the difference and print out the information. Otherwise if one log file is passed it will process and print out the information saved in the that log file.
