import gi

gi.require_version("GLib", "2.0")

from gi.repository import GLib

class DateUtils():
    def __init__(self):
        pass

    def currentDate(self):
        time_zone = GLib.TimeZone()
        date = GLib.DateTime.new_now(time_zone)
        format_date = GLib.DateTime.format(date, "%Y-%m-%d %H:%M:%S")
        return format_date

    def formatedCurrentDate(self):
        time_zone = GLib.TimeZone()
        date = GLib.DateTime.new_now(time_zone)
        format_current_date = GLib.DateTime.format(date, "%d/%m/%Y %H:%M:%S")
        return format_current_date
    