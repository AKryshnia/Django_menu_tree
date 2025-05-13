from django import template
from menu_app.models import MenuItem

register = template.Library()


@register.simple_tag
def get_menu_names():
    return (
        MenuItem.objects
        .values_list('menu_name', flat=True)
        .order_by('menu_name')
        .distinct()
    )


@register.inclusion_tag('menu_app/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('position')
    item_dict = {item.id: item for item in menu_items}
    menu_tree = []
    active_item = None

    for item in menu_items:
        item.children_list = []
        item.is_active = item.get_url() == current_url
        if item.is_active:
            active_item = item

    for item in menu_items:
        if item.parent_id:
            parent = item_dict.get(item.parent_id)
            if parent:
                parent.children_list.append(item)
        else:
            menu_tree.append(item)

    active_path = []
    if active_item:
        current = active_item
        while current:
            active_path.append(current)
            current = current.parent

    def mark_expanded(item, active_path):
        item.is_expanded = item in active_path or (active_path and active_path[-1].parent == item)
        for child in item.children_list:
            mark_expanded(child, active_path)

    for item in menu_tree:
        mark_expanded(item, active_path)

    return {'menu_items': menu_tree}
