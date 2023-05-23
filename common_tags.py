from django import template

register = template.Library()


@register.filter(name='hash')
def hash(h, key):
    return h[key]


@register.filter(name='list')
def list(l):
    return ",".join([t.name for t in l])


@register.filter(name='list_link')
def list_link(l):
    return ", ".join(["<a href='%s'>%s</a>" % (i.get_change_url(), i.name) for i in l])


@register.filter(name='list_user_link')
def list_user_link(l):
    return ", ".join(["<a href='%s'>%s</a>" % (i.get_change_url(), i) for i in l])


@register.filter(name='queryset_projectcategories')
def queryset_projectcategories(qs):
    return ", ".join(["<a href='%s'>%s</a>" % (pc.get_change_url(), pc.refer_category.name) for pc in qs])


@register.filter(name='dict')
def dict(h):
    return None


@register.filter(name='verbose_name')
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter(name='verbose_name_plural')
def verbose_name(obj):
    return obj._meta.verbose_name_plural


@register.filter(name='app_name')
def app_name(obj):
    return obj._meta.app_label
