from django import template

from fir_notifications.registry import registry

register = template.Library()


@register.inclusion_tag('fir_notifications/actions.html')
def notification_actions():
    actions = {
        method_name: method_object.verbose_name
        for method_name, method_object in registry.methods.items()
        if len(method_object.options)
    }

    return {'actions': actions}


@register.inclusion_tag('fir_notifications/actions_form.html', takes_context=True)
def notification_forms(context):
    actions = {
        method_name: method_object.form(user=context['user'])
        for method_name, method_object in registry.methods.items()
        if len(method_object.options)
    }

    return {'actions': actions}


@register.filter
def display_method(arg):
    method = registry.methods.get(arg, None)
    return 'Unknown' if method is None else method.verbose_name


@register.filter
def display_event(arg):
    event = registry.events.get(arg, None)
    return 'Unknown' if event is None else event.verbose_name


@register.filter
def display_event_section(arg):
    event = registry.events.get(arg, None)
    return 'Unknown' if event is None else event.section
