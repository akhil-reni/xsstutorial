from __future__ import absolute_import, unicode_literals

import requests
import copy
from lxml import html

from rxss.request_parser import RequestParser
from rxss.create_insertions import GetInsertionPoints
from rxss.context_analyzer import ContextAnalyzer
from rxss.payload_generator import payload_generator


class MakeRawHTTP:

    def __init__(self, request: object):
        self.rawRequest = self.makeRequest(request)

    def makeRequest(self, request: object) -> str:
        request.http_version = "HTTP/1.1"
        try:
            rawRequest = ''
            rawRequest += str(request.method)+' '+str(request.path)+' '+str(request.http_version)
            for k, v in request.headers.items():
                rawRequest += '\n'
                rawRequest += str(k)+': '+str(v)

            if request.data:
                rawRequest += '\n\n'
                for data in request.data:
                    rawRequest += str(data) + '=' + str(request.data[data]) + "&"

            return rawRequest
        except Exception as e:
            raise Exception(e)


def send_request(request, scheme):
    url = "{}://{}{}".format(scheme, request.headers.get("host"), request.path)
    req = requests.Request(request.method, url, params=request.params, data=request.data, headers=request.headers)
    r = req.prepare()
    s = requests.Session()
    response = s.send(r, allow_redirects=False, verify=False, proxies={"http": "http://127.0.0.1:8080"})
    return response


with open("requests.txt", "rb") as f:
    parser = RequestParser(f.read())
    i_p = GetInsertionPoints(parser.request)

    for request in i_p.requests:
        response = send_request(request, "http")
        if "teyascan" in response.text:
            print("probe reflection found in "+request.insertion)
            contexts = ContextAnalyzer.get_contexts(response.text, "teyascan")
            for context in contexts["contexts"]:
                payloads = payload_generator(context['type'])
                for payload in payloads:
                    dup = copy.deepcopy(request)
                    dup.replace("teyascan", payload['payload'])
                    response = send_request(dup, "http")
                    page_html_tree = html.fromstring(response.text)
                    count = page_html_tree.xpath(payload['find'])
                    if len(count):
                        print("VULNERABLE TO XSS")
                        http = MakeRawHTTP(dup)
                        print(http.rawRequest)