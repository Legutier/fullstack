# -*- coding: utf-8 -*-
import pytest
import requests


def test_hello_world():
    response = requests.get('http://localhost:8000')
    dom = response.content
    assert dom == b'Hello, world!'
