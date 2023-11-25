# flake8: noqa

import requests
import datetime
from attributedict.collections import AttributeDict
import typing as t
import json
import os
from urllib.parse import urlencode


BASE_URL = "https://api.stackexchange.com/2.3/questions"
TIME_OFFSET = 1700524800    # today
_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "configs.json")
if os.path.exists(_CONFIG_FILE) is False:
  print("warning      configs.json file does not exists")
  CONFIGS = {}
else:
  CONFIGS = json.load(open(_CONFIG_FILE, 'r'))


class ValidParams(AttributeDict):
  page: int = None
  pagesize: int = None
  fromdate: int = TIME_OFFSET - (24 * 3600)   # yesterday
  todate: int = TIME_OFFSET   # today
  order: t.Literal["desc", "asc"] = "desc"
  min: int = None
  max: int = None
  sort: t.Literal["activity", "votes", "creation", "hot", "week", "month"] = "activity"
  tagged: t.List[str] = [""]
  site: str = "stackoverflow"


class StackExchangeNotifier():
  def __init__(self):
    self.valid_params: dict = ValidParams()
    self.valid_params.update(CONFIGS)    # configs.json has more priority

    url = self.form_url()
    response = requests.get(url)

    #TODO: handle the response

    data = json.loads(response.content)

  def form_url(self):
    non_null_params = {}
    for key, value in self.valid_params.items():
      if value is None or value == "":
        continue
      value = ';'.join(value) if isinstance(value, list) else value   # tagged

      non_null_params.update({key: value})
    url = f"{BASE_URL}?{urlencode(non_null_params)}"
    return url


if __name__ == '__main__':
  StackExchangeNotifier()
