from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
from django.utils import timezone

from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_to_html(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    template
    if html:
        return HttpResponse(html, content_type='application/html')
    return None


def fill_template(template_content, employee):
    template = Template(template_content)
    context = Context(employee)
    context.push({"today": timezone.now()})
    return template.render(context)
