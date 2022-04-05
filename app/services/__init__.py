# -*- coding: utf-8 -*-
import html
import requests
from typing import Union


class BaseService:

    @staticmethod
    def http(method: str, url: str = "", res_type: str = "json", timeout: int = 2, **kwargs) -> Union[dict, str]:
        response = requests.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
        if res_type == "text":
            return response.text
        elif res_type == "html":
            return html.unescape(response.text)
        else:
            return dict(response.json())

    @staticmethod
    def http_get(url: str, **kwargs) -> Union[dict, str]:
        return BaseService.http("get", url, **kwargs)

    @staticmethod
    def http_post(url: str, **kwargs) -> Union[dict, str]:
        return BaseService.http("post", url, **kwargs)
