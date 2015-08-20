# ==========================================================================================================
# Erl - A Sublime Text 3 Plugin for Erlang Integrated Testing & Code Completion
#
# Copyright (C) 2013, Roberto Ostinelli <roberto@ostinelli.net>.
# All rights reserved.
#
# BSD License
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided
# that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this list of conditions and the
#        following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
#        the following disclaimer in the documentation and/or other materials provided with the distribution.
#  * Neither the name of the authors nor the names of its contributors may be used to endorse or promote
#        products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ==========================================================================================================

# imports
import sublime, sublime_plugin
import os, threading, re
import Erl.erl_core as GLOBALS
from .erl_core import ErlProjectLoader


# update command (used to edit the view content)
class UpdateCommand(sublime_plugin.TextCommand):
	def run(self, edit, buffer=None):
		self.view.insert(edit, self.view.size(), buffer)

# test runner
class ErlAutocompiler(ErlProjectLoader):

	def __init__(self, view):
		# init super
		ErlProjectLoader.__init__(self, view)
		# init
		self.panel_name = 'erl_autocompiler'
		self.panel_buffer = ''
		# setup panel
		self.setup_panel()

	def setup_panel(self):
		self.panel = self.window.get_output_panel(self.panel_name)

	def update_panel(self):
		if len(self.panel_buffer):
			self.panel.run_command("update", {"buffer": self.panel_buffer})
			self.panel.show(self.panel.size())
			self.panel_buffer = ''
			self.window.run_command("show_panel", {"panel": "output.%s" % self.panel_name})
			regions = []
			for line in self.last_text.splitlines():
				m = re.search("(.+):(\d+):", line)
				if m != None and self.view.file_name().endswith(m.group(1)):
					r = self.view.line(self.view.text_point(long(m.group(2)) - 1, 0))
					regions.append(r)
			self.view.add_regions("erl_errors", regions, "comment")

	def hide_panel(self):
		self.window.run_command("hide_panel")
		self.view.erase_regions("erl_errors")

	def log(self, text):
		if type(text) == bytes:
			text = text.decode('utf-8')
		self.last_text = text
		self.panel_buffer += text
		sublime.set_timeout(self.update_panel, 0)

	def compile(self):
		retcode, data = self.compile_source(skip_deps=True)
		if retcode != 0:
			ignore_subdirs_warnings = GLOBALS.ERL.settings.get('ignore_subdirs_warnings', False)
			ignore_warnings = GLOBALS.ERL.settings.get('ignore_warnings', False)
			if type(data) == bytes:
				data = data.decode('utf-8')

			filtered_text = ""
			for line in data.splitlines():
				if ignore_warnings and "WARN" in line:
					pass
				elif ignore_subdirs_warnings and "Ignoring sub_dirs for" in line:
					pass
				elif "(compile)" in line:
					pass
				else:
					filtered_text += line

			if filtered_text:
				self.log(data)
				return

		sublime.set_timeout(self.hide_panel, 0)

# listener
class ErlAutocompilerListener(sublime_plugin.EventListener):

	# CALLBACK ON VIEW SAVE
	def on_post_save(self, view):
		# check init successful
		if GLOBALS.ERL.initialized == False: return
		# ensure context matches
		caret = view.sel()[0].a
		if not ('source.erlang' in view.scope_name(caret)): return
		# init
		autocompiler = ErlAutocompiler(view)
		# compile saved file & reload completions
		class ErlThread(threading.Thread):
			def run(self):
				# compile
				autocompiler.compile()
		ErlThread().start()
