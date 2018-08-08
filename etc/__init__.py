import json


samples = ['sample_rh_quote']


for sample in samples:
    globals()[sample] = json.loads(open("etc/{}.json".format(sample), 'r').read())
