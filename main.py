# noqa: E111, E501

import requests
import datetime
import typing as t
import json
import os
from urllib.parse import urlencode

from mail import compose_email


BASE_URL = "https://api.stackexchange.com/2.3/questions"
TIME_OFFSET = 1701475200    # yesterday
_START_DAY = datetime.date(2023, 12, 2)
DAYS_PASSED = (datetime.date.today() - _START_DAY).days
_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.exists(_CONFIG_FILE) is False:
  print("warning      configs.json file does not exists")
  CONFIGS = {}
else:
  data: dict = json.load(open(_CONFIG_FILE, 'r'))
  CONFIGS = {}
  for key, value in data.items():
    if value is not None:
      CONFIGS.update({key: value})


class ValidParams:
  def __init__(self):
    self.page: int = None
    self.pagesize: int = None
    self.fromdate: int = TIME_OFFSET + ((DAYS_PASSED - 1) * 24 * 3600)
    self.todate: int = TIME_OFFSET + (DAYS_PASSED * 24 * 3600)
    self.order: t.Literal["desc", "asc"] = "desc"
    self.min: int = None
    self.max: int = None
    self.sort: t.Literal["activity", "votes", "creation", "hot", "week", "month"] = "activity"
    self.tagged: t.List[str] = [""]
    self.site: str = "stackoverflow"


class QuestionData:
  def __init__(self):
    self.user_reputation: int = 1
    self.is_answered: bool = False
    self.view_count: int = 0
    self.answer_count: int = 0
    self.score: int = 0
    self.title: str = ""
    self.link: str = ""


class StackExchangeNotifier():
  def __init__(self):
    self.valid_params: dict = ValidParams().__dict__
    self.valid_params.update(CONFIGS)    # config.json has more priority
    self.question_data = []

    url = self.form_url()
    response = requests.get(url)

    if response.status_code < 200 and response.status_code >= 300:
      print("error      request to {} failed".format(url))
      return

    data = json.loads(response.content)
    for question in data.get('items'):
      question_template = QuestionData().__dict__
      for key, value in question.items():
        question_template.update({key: value}) if key in question_template else None
      self.question_data.append(question_template)

    # print(self.question_data)
    compose_email(date=str(datetime.date.today()), message=self.question_data)

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
