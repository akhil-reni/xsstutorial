from __future__ import absolute_import, unicode_literals

from lxml import html
import re


class ContextAnalyzer:

    def __init__(self, response_text, search_string):
        self.get_contexts(response_text, search_string)

    @staticmethod
    def get_contexts(response_text, search_string):
        page_html_tree = html.fromstring(response_text)
        results = dict()
        results["payload"] = search_string
        results["contexts"] = []

        # check in attribute name <x xxxINPUT=xxx>
        xpath = '//*[@' + search_string + ']'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'attribname'
            context['count'] = len(n)
            results['contexts'].append(context)

        # check in attribute value <x xxx=INPUTxxx>
        xpath = '//*[@*[contains(.,\'' + search_string + '\')]]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'attribval'
            context['count'] = len(n)
            results['contexts'].append(context)

        # payload inside HTML Tags <x> input </x>
        xpath = '//*[contains(text(),\'' + search_string + '\')]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'htmltag'
            context['count'] = len(n)
            results['contexts'].append(context)

        # HTML Comments <!---sadsadds dasdasdsa INPUT >
        xpath = '//*[comment()[contains(.,\'' + search_string + '\')]]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'comment'
            context['count'] = len(n)
            results['contexts'].append(context)

        # Style <style>INPUT</style>
        xpath = '//style[contains(text(),\'' + search_string + '\')]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'style'
            context['count'] = len(n)
            results['contexts'].append(context)

        # inside style attribute value <style>.test {INPUT}</style>
        xpath = '//*[@style[contains(.,\'' + search_string + '\')]]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'styleattribval'
            context['count'] = len(n)
            results['contexts'].append(context)

        # inside href <a href=INPUT>a</a>
        xpath = '//*[@href[contains(.,\'' + search_string + '\')]]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'href'
            context['count'] = len(n)
            results['contexts'].append(context)

        # inside <Script>INPUT</script>
        xpath = '//script[contains(text(),\'' + search_string + '\')]'
        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'jsnode'
            context['count'] = len(n)
            results['contexts'].append(context)

        # check for JS Single quote and double quotes  <Script>var x='x';</script> <Script>var x="x";</script>
        js_single_quote = 0
        js_double_quote = 0
        xpath = '//script[contains(text(),\'' + search_string + '\')]'
        n = page_html_tree.xpath(xpath)

        if len(n):
            for js_finding in n:
                js_string = js_finding.text

                # TODO below line is a mix of Javascript and Python, implement for some rare cases...
                #escaped_search = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

                sqre = re.compile('\'(?:[^\'\\\\]|\\\\.)*' + search_string + '(?:[^\'\\\\]|\\\\.)*\'')
                #sqre = re.compile('\'(?:[^\'\\\\]|\\\\.)*' + escaped_search + '(?:[^\'\\\\]|\\\\.)*\'')
                dqre = re.compile('"(?:[^"\\\\]|\\\\.)*' + search_string + '(?:[^"\\\\]|\\\\.)*"')
                #dqre = re.compile('(?:[^"\\\\]|\\\\.)*' + escaped_search + '(?:[^"\\\\]|\\\\.)*"')

                sq = sqre.findall(js_string)
                dq = dqre.findall(js_string)

                js_single_quote += len(sq)
                js_double_quote += len(dq)

            if js_single_quote:
                context = {}
                context['type'] = 'jssinglequote'
                context['count'] = js_single_quote
                results['contexts'].append(context)

            if js_double_quote:
                context = {}
                context['type'] = 'jsdoublequote'
                context['count'] = js_double_quote
                results['contexts'].append(context)

        # inside any onXXXX() attribute <a onxxx=INPUT>a</a>
        xpath = '//*[@onerror[contains(.,\'' + search_string \
                + '\')] or @onload[contains(.,\'' + search_string \
                + '\')] or @onclick[contains(.,\'' + search_string \
                + '\')] or @oncontextmenu[contains(.,\'' + search_string \
                + '\')] or @ondblclick[contains(.,\'' + search_string \
                + '\')] or @onmousedown[contains(.,\'' + search_string \
                + '\')] or @onmouseenter[contains(.,\'' + search_string \
                + '\')] or @onmouseleave[contains(.,\'' + search_string \
                + '\')] or @onmousemove[contains(.,\'' + search_string \
                + '\')] or @onmouseover[contains(.,\'' + search_string \
                + '\')] or @onmouseout[contains(.,\'' + search_string \
                + '\')] or @onmouseup[contains(.,\'' + search_string \
                + '\')] or @onkeydown[contains(.,\'' + search_string \
                + '\')] or @onkeypress[contains(.,\'' + search_string \
                + '\')] or @onkeyup[contains(.,\'' + search_string \
                + '\')] or @onabort[contains(.,\'' + search_string \
                + '\')] or @onbeforeunload[contains(.,\'' + search_string \
                + '\')] or @onhashchange[contains(.,\'' + search_string \
                + '\')] or @onpageshow[contains(.,\'' + search_string \
                + '\')] or @onpagehide[contains(.,\'' + search_string \
                + '\')] or @onresize[contains(.,\'' + search_string \
                + '\')] or @onscroll[contains(.,\'' + search_string \
                + '\')] or @onunload[contains(.,\'' + search_string \
                + '\')] or @onblur[contains(.,\'' + search_string \
                + '\')] or @onchange[contains(.,\'' + search_string \
                + '\')] or @onfocus[contains(.,\'' + search_string \
                + '\')] or @onfocusin[contains(.,\'' + search_string \
                + '\')] or @onfocusout[contains(.,\'' + search_string \
                + '\')] or @oninput[contains(.,\'' + search_string \
                + '\')] or @oninvalid[contains(.,\'' + search_string \
                + '\')] or @onreset[contains(.,\'' + search_string \
                + '\')] or @onsearch[contains(.,\'' + search_string \
                + '\')] or @onselect[contains(.,\'' + search_string \
                + '\')] or @ondrag[contains(.,\'' + search_string \
                + '\')] or @ondragend[contains(.,\'' + search_string \
                + '\')] or @ondragenter[contains(.,\'' + search_string \
                + '\')] or @ondragleave[contains(.,\'' + search_string \
                + '\')] or @ondragover[contains(.,\'' + search_string \
                + '\')] or @ondragstart[contains(.,\'' + search_string \
                + '\')] or @ondrop[contains(.,\'' + search_string \
                + '\')] or @oncopy[contains(.,\'' + search_string \
                + '\')] or @oncut[contains(.,\'' + search_string \
                + '\')] or @onpaste[contains(.,\'' + search_string \
                + '\')] or @onafterprint[contains(.,\'' + search_string \
                + '\')] or @onbeforeprint[contains(.,\'' + search_string \
                + '\')] or @onabort[contains(.,\'' + search_string \
                + '\')] or @oncanplay[contains(.,\'' + search_string \
                + '\')] or @oncanplaythrough[contains(.,\'' + search_string \
                + '\')] or @ondurationchange[contains(.,\'' + search_string \
                + '\')] or @onemptied[contains(.,\'' + search_string \
                + '\')] or @onended[contains(.,\'' + search_string \
                + '\')] or @onloadeddata[contains(.,\'' + search_string \
                + '\')] or @onloadedmetadata[contains(.,\'' + search_string \
                + '\')] or @onloadstart[contains(.,\'' + search_string \
                + '\')] or @onpause[contains(.,\'' + search_string \
                + '\')] or @onplay[contains(.,\'' + search_string \
                + '\')] or @onplaying[contains(.,\'' + search_string \
                + '\')] or @onprogress[contains(.,\'' + search_string \
                + '\')] or @onratechange[contains(.,\'' + search_string \
                + '\')] or @onseeked[contains(.,\'' + search_string \
                + '\')] or @onseeking[contains(.,\'' + search_string \
                + '\')] or @onstalled[contains(.,\'' + search_string \
                + '\')] or @onsuspend[contains(.,\'' + search_string \
                + '\')] or @ontimeupdate[contains(.,\'' + search_string \
                + '\')] or @onvolumechange[contains(.,\'' + search_string \
                + '\')] or @onwaiting[contains(.,\'' + search_string \
                + '\')] or @onopen[contains(.,\'' + search_string \
                + '\')] or @onmessage[contains(.,\'' + search_string \
                + '\')] or @onmousewheel[contains(.,\'' + search_string \
                + '\')] or @ononline[contains(.,\'' + search_string \
                + '\')] or @onoffline[contains(.,\'' + search_string \
                + '\')] or @onpopstate[contains(.,\'' + search_string \
                + '\')] or @onshow[contains(.,\'' + search_string \
                + '\')] or @onstorage[contains(.,\'' + search_string \
                + '\')] or @ontoggle[contains(.,\'' + search_string \
                + '\')] or @onwheel[contains(.,\'' + search_string \
                + '\')] or @ontouchcancel[contains(.,\'' + search_string \
                + '\')] or @ontouchend[contains(.,\'' + search_string \
                + '\')] or @ontouchmove[contains(.,\'' + search_string \
                + '\')] or @ontouchstart[contains(.,\'' + search_string \
                + '\')] or @onsubmit[contains(.,\'' + search_string + '\')]]'

        n = page_html_tree.xpath(xpath)
        if len(n):
            context = {}
            context['type'] = 'onattrib'
            context['count'] = len(n)
            results['contexts'].append(context)

        return results