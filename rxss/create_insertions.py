from __future__ import absolute_import, unicode_literals

import copy


class GetInsertionPoints:

    def __init__(self, request):
        self.request = request
        self.requests = []
        self.params(append=True)
        self.body(append=True)

    def params(self, append: bool = False) -> None:
        if self.request.params:
            for q in self.request.params:
                request = copy.deepcopy(self.request)
                if append:
                    request.params[q] = str(request.params[q])+" teyascan"
                else:
                    request.params[q] = "teyascan"
                request.insertion = q
                request.iplace = 'params'
                self.requests.append(request)

    def body(self, append: bool = False) -> None:
        if self.request.data:
            for q in self.request.data:
                request = copy.deepcopy(self.request)
                if append:
                    request.data[q] = str(request.data[q])+" teyascan"
                else:
                    request.data[q] = "teyascan"
                request.insertion = q
                request.iplace = 'body'
                self.requests.append(request)