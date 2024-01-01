from django import template


register = template.Library()

@register.filter
def replaceBlank(value,stringVal = ""):
  value = str(value).replace(stringVal, '')
  return value