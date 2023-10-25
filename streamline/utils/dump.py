import pickle
import json
from pathlib import Path as plp

def dump_file(object,outfile):
  """Saves an object in both as pickled and json format"""
  output = plp(outfile)
  with open(output.with_suffix(".pickle"),"wb") as out:
    pickle.dump(object,out)
  with open(output.with_suffix(".json"),"w") as out:
    json.dump(object,out)
