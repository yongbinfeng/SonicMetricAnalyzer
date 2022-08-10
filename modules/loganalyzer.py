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
        return objn

        
def process_file(fname):
    assert os.path.isfile(fname), f"file {fname} does not exist."

    formated = text_string_to_metric_families(fname)
    metrics = list(formated)

    models = OrderedDict()

    for metric in metrics:
        #print("metric name ", metric.name)

        # collect all the models first
        if "nv_inference_request_success" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]] = TritonModel(samp.labels["model"])

        # collect all the infer counts
        if "nv_inference_request_success" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].nreq = samp.value

        if "nv_inference_count" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].ninfer = samp.value

        if "nv_inference_exec_count" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].nexec = samp.value

        # collect all latency information
        # unit in ms (1e-3 second)
        if "nv_inference_request_duration_us" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].treq = samp.value / 1.0e3

        if "nv_inference_queue_duration_us" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].tqueue = samp.value / 1.0e3

        if "nv_inference_compute_input_duration_us" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].tinput = samp.value / 1.0e3

        if "nv_inference_compute_infer_duration_us" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].tinfer = samp.value / 1.0e3

        if "nv_inference_compute_output_duration_us" in metric.name:
            for samp in metric.samples:
                models[samp.labels["model"]].toutput = samp.value / 1.0e3

    return models


def print_info(models1, models2 = None):
    if models2:
        # if models2 exist, take the difference
        assert models1.keys() == models2.keys(), "the 2 log files should have the same models"
        for modelname in models1.keys():
            models1[modelname] = models1[modelname] - models2[modelname]
    models = models1

    print("******\nDumped results\n******")

    # list all models
    print("all served models: ")
    for modelname in models.keys():
        print("model ", modelname)
    print()

    for modelname, model in models.items():
        print("model name {:15s}, total inference requests {:.0f}".format(model.name, abs(model.nreq)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, total inference counts {:.0f}".format(model.name, abs(model.ninfer)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, total execution requests {:.0f}".format(model.name, abs(model.nexec)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, total request time {:.2f}".format(model.name, model.treq / (model.ninfer + 1e-6)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, total queue time {:.2f}".format(model.name, model.tqueue / (model.ninfer + 1e-6)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, computing input time {:.2f}".format(model.name, model.tinput / (model.ninfer + 1e-6)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, infer time {:.2f}".format(model.name, model.tinfer / (model.ninfer + 1e-6)))
    print()

    for modelname, model in models.items():
        print("model name {:15s}, computing output time {:.2f}".format(model.name, model.toutput / (model.ninfer + 1e-6)))
    print()
