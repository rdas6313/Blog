from django import template

register = template.Library()


@register.filter
def get_like(session, comment_id):
    """ get value from session variable """
    comment_id = f'comment_{comment_id}'
    dic = session.get(comment_id, None)
    if not dic:
        return None
    return dic.get('like', None)
