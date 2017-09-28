import datetime

from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

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

		ctx = {}
		ctx['update_form'] = form
		ctx['event'] = self.event.resolve(context)

		return render_to_string('events/partials/event_form.html', ctx)

	def get_form(self, context):

		event = self.event.resolve(context)

		return EventForm(instance=event)

class FooterEventsNode(template.Node):

	def __init__(self, user):

		self.user = template.Variable(user)

	def render(self, context):

		events = Event.objects.order_by('date').filter(date__gte=datetime.date.today())[:2]
		user = self.user.resolve(context)

		ctx = {}
		ctx['events'] = events 
		ctx['user'] = user

		return render_to_string('events/partials/footer_events.html', ctx)
