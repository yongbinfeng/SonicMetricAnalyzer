import os.path
from collections import OrderedDict
from .parser import text_string_to_metric_families

class TritonModel:
    """
    Model class to document relevant information:
    model name, count, latency.
    Currently count only support successeful counts
    """

    def __init__(self,
                 name: str,
                 nreq: int = 0, ninfer: int = 0, nexec: int = 0,
                 treq: float = 0, tqueue: float = 0, tinput: float = 0, tinfer: float = 0, toutput: float = 0,
                 nevt: int = 0,
                 ):
        self.name = name

        self.nreq = nreq
        self.ninfer = ninfer
        self.nexec = nexec

        self.treq = treq
        self.tqueue = tqueue
        self.tinput = tinput
        self.tinfer = tinfer
        self.toutput = toutput

        self.nevt = nevt

    def __add__(self, obj2):
        objn = TritonModel(self.name)
        objn.nreq    = self.nreq    + obj2.nreq
        objn.ninfer  = self.ninfer  + obj2.ninfer
        objn.nexec   = self.nexec   + obj2.nexec
        objn.treq    = self.treq    + obj2.treq
        objn.tqueue  = self.tqueue  + obj2.tqueue
        objn.tinput  = self.tinput  + obj2.tinput
        objn.tinfer  = self.tinfer  + obj2.tinfer
        objn.toutput = self.toutput + obj2.toutput
        objn.nevt    = self.nevt    + obj2.nevt
        return objn

    def __sub__(self, obj2):
        objn = TritonModel(self.name)
        objn.nreq    = self.nreq    - obj2.nreq
        objn.ninfer  = self.ninfer  - obj2.ninfer
        objn.nexec   = self.nexec   - obj2.nexec
        objn.treq    = self.treq    - obj2.treq
        objn.tqueue  = self.tqueue  - obj2.tqueue
        objn.tinput  = self.tinput  - obj2.tinput
        objn.tinfer  = self.tinfer  - obj2.tinfer
        objn.toutput = self.toutput - obj2.toutput
        objn.nevt    = self.nevt    - obj2.nevt
        return objn

        
def process_file(fname, nevt = 0):
    assert os.path.isfile(fname), f"file {fname} does not exist."

    formated = text_string_to_metric_families(fname)
    metrics = list(formated)

    results = OrderedDict()

    for metric in metrics:
        #print("metric name ", metric.name)

        # collect all the results first
        if "nv_inference_request_success" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]] = TritonModel(samp.labels["model"])

        # collect all the infer counts
        if "nv_inference_request_success" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].nreq = samp.value

        if "nv_inference_count" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].ninfer = samp.value

        if "nv_inference_exec_count" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].nexec = samp.value

        if nevt > 0:
            for samp in metric.samples:
                results[samp.labels["model"]].nevt = nevt

        # collect all latency information
        # unit in ms (1e-3 second)
        if "nv_inference_request_duration_us" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].treq = samp.value / 1.0e3

        if "nv_inference_queue_duration_us" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].tqueue = samp.value / 1.0e3

        if "nv_inference_compute_input_duration_us" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].tinput = samp.value / 1.0e3

        if "nv_inference_compute_infer_duration_us" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].tinfer = samp.value / 1.0e3

        if "nv_inference_compute_output_duration_us" in metric.name:
            for samp in metric.samples:
                results[samp.labels["model"]].toutput = samp.value / 1.0e3

    return results


def print_info(results1, results2 = None):
    if results2:
        # if results2 exist, take the difference
        assert results1.keys() == results2.keys(), "the 2 log files should have the same results"
        for modelname in results1.keys():
            results1[modelname] = results1[modelname] - results2[modelname]
    results = results1

    print("******\nDumped results\n******")

    # list all results
    print("all served results: ")
    for modelname in results.keys():
        print("model ", modelname)
    print()

    for modelname, model in results.items():
        print("model name {:15s}, total inference requests {:.0f}".format(model.name, abs(model.nreq)))
    print()

    for modelname, model in results.items():
        print("model name {:15s}, total inference counts {:.0f}".format(model.name, abs(model.ninfer)))
    print()

    for modelname, model in results.items():
        print("model name {:15s}, total execution requests {:.0f}".format(model.name, abs(model.nexec)))
    print()

    for modelname, model in results.items():
        # units in ms (1e-3 s)
        tavg = model.treq / (model.ninfer + 1e-6) 
        if model.nevt > 0:
            tavg = model.treq / (model.nevt + 1e-6)
        print("model name {:15s}, total request time {:.2f}".format(model.name, tavg))
    print()

    for modelname, model in results.items():
        tavg = model.tqueue / (model.ninfer + 1e-6)
        if model.nevt > 0:
            tavg = model.tqueue / (model.nevt + 1e-6)
        print("model name {:15s}, total queue time {:.2f}".format(model.name, tavg))
    print()

    for modelname, model in results.items():
        tavg = model.tinput / (model.ninfer + 1e-6)
        if model.nevt > 0:
            tavg = model.tinput / (model.nevt + 1e-6)
        print("model name {:15s}, computing input time {:.2f}".format(model.name, tavg))
    print()

    for modelname, model in results.items():
        tavg = model.tinfer / (model.ninfer + 1e-6)
        if model.nevt > 0:
            tavg = model.tinfer / (model.nevt + 1e-6)
        print("model name {:15s}, infer time {:.2f}".format(model.name, tavg))
    print()

    for modelname, model in results.items():
        tavg = model.toutput / (model.ninfer + 1e-6)
        if model.nevt > 0:
            tavg = model.toutput / (model.nevt + 1e-6)
        print("model name {:15s}, computing output time {:.2f}".format(model.name, tavg))
    print()
