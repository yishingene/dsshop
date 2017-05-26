from django import template
from django.template import Context
from django.utils.safestring import mark_safe

from other_pages.models import Event
from other_pages.forms import EventForm

register = template.Library()

@register.tag
def event_form(parser, token):

	tokens = token.split_contents()	

	event = tokens[1]

	return EventFormNode(event)

class EventFormNode(template.Node):

	def __init__(self, event):

		self.event = template.Variable(event)

	def render(self, context):

		form = self.get_form(context)

		#print('°°°°°°°°°°°°° %s' % form)

		t = context.template.engine.get_template('events/partials/event_form.html')

		return t.render(Context({'update_form': form}, autoescape=context.autoescape))

	def get_form(self, context):

		event = self.event.resolve(context)

		print(' yyyyyyyyyyy %s' % event)

		return EventForm(instance=event)



