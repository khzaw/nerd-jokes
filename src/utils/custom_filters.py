from google.appengine.ext.webapp import template
import re

register = template.create_template_register()
linkify_regex = re.compile(r'(([a-zA-Z]+)://[^ \t\n\r]+)', re.MULTILINE)
hashify_regex = re.compile(r"(#\w.+)")

@register.filter
def linkify(value, arg=''):
    def _spacify(s, chars=40):
        if len(s) <= chars:
            return s
        for k in range(len(s) / chars):
            pos = (k + 1) * chars
            s = s[:pos] + '' + s[pos:]
        return s
    def _replace(match):
        href = match.group(0)
        cls = arg and (' class="%s"' % arg) or ''
        return '<a href="%s"%s>%s</a>' % (href, cls, _spacify(href))
    return linkify_regex.sub(_replace, value)

@register.filter
def hashify(value):
    return hashify_regex.sub('<a href="#" class="hashtag">%s</a>' % hashify_regex.search(value).group(0), value)

