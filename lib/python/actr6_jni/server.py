# -*- coding:	utf-8 -*-
#===============================================================================
# This file is part of ACTR6_JNI.
# Copyright (C) 2012-2013 Ryan Hope <rmh3093@gmail.com>
#
# ACTR6_JNI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ACTR6_JNI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ACTR6_JNI.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory
import json

class ACTR_Protocol(LineReceiver):

	def connectionMade(self):
		for d in self.factory.dispatchers:
			d.trigger(e="connectionMade", model=None, params=None)

	def connectionLost(self, reason):
		self.clearLineBuffer()
		for d in self.factory.dispatchers:
			d.trigger(e="connectionLost", model=None, params=None)

	def lineReceived(self, string):
		obj = json.loads(string)
		if obj['method'] == 'set-mp-time':
			if self.factory.clock:
				self.factory.clock.setTime(float(params[0]))
		elif obj['method'] == 'disconnect':
			self.factory.p.transport.loseConnection()
		else:
			if obj['method'] == 'reset':
				if self.factory.clock:
					self.factory.clock.setTime(0.0)
			for d in self.factory.dispatchers:
				d.trigger(e=obj['method'],
						  model=obj['model'],
						  params=obj['params'])
		self.sendCommand(obj['model'], "sync")

	def sendCommand(self, model, method, **params):
		self.sendLine(json.dumps({"model": model, "method": method, "params": params}))

class JNI_Server(Factory):

	model = None

	def __init__(self, env, clock=None):
		self.env = env
		self.clock = clock
		self.dispatchers = []

	def addDispatcher(self, dispatcher):
		self.dispatchers.append(dispatcher)

	def buildProtocol(self, addr):
		self.p = ACTR_Protocol()
		self.p.factory = self
		return self.p
	
	def add_dm(self, chunk):
		self.p.sendCommand(self.model, "add-dm", chunk=chunk.get_chunk())

	def update_display(self, chunks, clear=False):
		visual_locations = [chunk.get_visual_location() for chunk in chunks]
		visual_objects = [chunk.get_visual_object() for chunk in chunks]
		args = {"loc-chunks": visual_locations, 
				"obj-chunks": visual_objects,
				"clear": clear}
		self.p.sendCommand(self.model, "update-display", **args)

	def display_new(self, chunks):
		visual_locations = [chunk.get_visual_location() for chunk in chunks]
		visual_objects = [chunk.get_visual_object() for chunk in chunks]
		args = {"loc-chunks": visual_locations, 
				"obj-chunks": visual_objects}
		self.p.sendCommand(self.model, "display-new", **args)
		
	def display_add(self, chunk):
		visual_location = chunk.get_visual_location()
		visual_object = chunk.get_visual_object()
		args = {"loc-chunk": visual_location, 
				"obj-chunk": visual_object}
		self.p.sendCommand(self.model, "display-add", **args)

	def display_remove(self, chunk=None, name=None):
		if chunk:
			name = chunk.name
		if name:
			args = {"loc-chunk-name": name}
			self.p.sendCommand(self.model, "display-remove", **args)
		
	def display_update(self, chunks, clear=False):
		chunks = [chunk.get_visual_location() for chunk in chunks] + [chunk.get_visual_object() for chunk in chunks]
		self.p.sendCommand(self.model, "display-update", chunks=chunks, clear=clear)
		
	def set_cursor_location(self, loc):
		self.p.sendCommand(self.model, "set-cursor-loc", loc=loc)

	def digit_sound(self, digit):
		self.p.sendCommand(self.model, "new-digit-sound", digit=digit)

	def tone_sound(self, freq, duration):
		self.p.sendCommand(self.model, "new-tone-sound", frequency=freq, duration=duration)

	def word_sound(self, words):
		self.p.sendCommand(self.model, "new-word-sound", words=words)

	def other_sound(self, content, onset, delay, recode):
		self.p.sendCommand(self.model, "new-other-sound", content=content, onset=onset, delay=delay, recode=recode)

	def trigger_reward(self, reward):
		self.p.sendCommand(self.model, "trigger-reward", reward=reward)

	def disconnect(self):
		self.p.sendCommand(self.model, "disconnect")
		
	def setup(self, width, height):
		self.p.sendCommand(self.model, "setup", width=width, height=height)
		
	def trigger_event(self, event, *args):
		self.p.sendCommand(self.model, "trigger-event", event=event, args=args)