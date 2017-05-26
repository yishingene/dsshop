import datetime

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

@register.tag
def render_footer_events(parser, token):

	tokens = token.split_contents()	

	user = tokens[1]

	return FooterEventsNode(user)


class EventFormNode(template.Node):

	def __init__(self, event):

		self.event = template.Variable(event)

	def render(self, context):

		form = self.get_form(context)

		t = context.template.engine.get_template('events/partials/event_form.html')

		return t.render(Context({'update_form': form, 'event': self.event.resolve(context)}, autoescape=context.autoescape))

	def get_form(self, context):

		event = self.event.resolve(context)

		return EventForm(instance=event)

class FooterEventsNode(template.Node):

	def __init__(self, user):

		self.user = template.Variable(user)

	def render(self, context):

		events = Event.objects.order_by('date').filter(date__gte=datetime.date.today())[:2]
		user = self.user.resolve(context)

		t = context.template.engine.get_template('events/partials/footer_events.html')

		return t.render(Context({'events': events, 'user': user}, autoescape=context.autoescape))

