from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import os
import sys


token = os.getenv("ADS_DEV_KEY", "")


def get_metrics(clobber=False):
    if clobber or not os.path.exists("metrics.json"):
        url = "https://api.adsabs.harvard.edu/v1/metrics"
        bibcodes = []
        with open("bibcodes.txt", "r") as f:
            for line in f.readlines():
                bibcodes.append(line.replace("\n", ""))
        bibcodes = '"' + '", "'.join(bibcodes) + '"'
        data = '{"bibcodes": [%s], "types":["timeseries"]}' % bibcodes
        req = Request(url, data.encode("ascii"))
        req.add_header("Authorization", "Bearer %s" % token)
        req.add_header("Content-Type", "application/json")
        content = urlopen(req).read()
        metrics = json.loads(content)
        with open("metrics.json", "w") as json_file:
            json.dump(metrics, json_file)
    else:
        print("Using cached metrics.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clobber":
        clobber = True
    else:
        clobber = False
    get_metrics(clobber=clobber)

