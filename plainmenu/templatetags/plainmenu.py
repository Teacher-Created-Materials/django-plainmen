from __future__ import absolute_import
from django import template
import swapper

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context, menu_name, group_name=None, **kwargs):
    Menu = swapper.load_model('plainmenu', 'Menu')
    Group = swapper.load_model('plainmenu', 'Group')

    template_name = kwargs.get('template', 'plainmenu/menu.html')

    if isinstance(group_name, Group):
        group = group_name
    elif group_name is not None:
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            group = None
    else:
        group = None

    if isinstance(menu_name, Menu):
        menu = menu_name
    else:
        try:
            menu = Menu.objects.get(identifier=menu_name, group=group)
        except Menu.DoesNotExist:
            menu = None

    context['items'] = menu.get_items() if menu else []

    return template.loader.render_to_string(
        template_name, context.flatten(), request=context['request']
    )


@register.inclusion_tag('admin/tree_change_list_results.html', takes_context=True)
def result_tree_pm(context, cl, request):
    from treebeard.templatetags.admin_tree import result_tree as orig

    res = orig(context, cl, request)
    res['filtered'] = False
    return res
