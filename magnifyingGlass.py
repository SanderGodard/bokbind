#!/bin/python3
import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import bokbind


# https://dbus.freedesktop.org/doc/dbus-python/dbus.lowlevel.html#dbus.lowlevel.MethodCallMessage


class Args():
	def __init__(self, parameters, title, text, silent):
		self.parameters = parameters
		self.title = title
		self.text = text
		self.silent = silent


def notifications(bus, message):
	# print(message)
	if message.get_args_list(byte_arrays=True)[0][0] == ":":
		return False
	title = message.get_args_list(byte_arrays=True)[3]
	if title in ["Notification history", "Notifications"]:
		return False
	app = message.get_args_list(byte_arrays=True)[0]
	msg = message.get_args_list(byte_arrays=True)[4]

	# print(message.get_args_list()[1])
	# print(message.get_args_list()[2])
	# print(message.get_args_list()[5])
	# print(message.get_args_list(byte_arrays=True)[6])
	# print(message.get_args_list()[7])

	if app == "notify-send":
		silent = True
		return False
	else:
		silent = False
		# pass
		#message.terminate()

	args = Args("", str(title + " - " + app), msg, silent)
	print(app + " - " + title + " - " + msg)
	# args.parameters, args.title, args.text, args.silent
	if not bokbind.main("store", args):
		print("	Failed to store")

	# print(message.get_destination())
	# print(message.get_interface())
	# print(message.get_member())
	# print(message.get_sender())
	# print(bus)
#	for i in message:
#		print(i)
	return True
    # do your magic


DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
