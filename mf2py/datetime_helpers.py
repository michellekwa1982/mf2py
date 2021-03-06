'''helper functions to deal wit datetime strings'''
from __future__ import unicode_literals, print_function

import re

# REGEX!

DATE_RE = r'\d{4}-\d{2}-\d{2}'
SEC_RE = r'(:(?P<second>\d{2})(\.\d+)?)'
RAWTIME_RE = r'(?P<hour>\d{1,2})(:(?P<minute>\d{2})%s?)?' % (SEC_RE)
AMPM_RE = 'am|pm|a\.m\.|p\.m\.'
TIMEZONE_RE = r'Z|[+-]\d{2}:?\d{2}?'
TIME_RE = (r'(?P<rawtime>%s)( ?(?P<ampm>%s))?( ?(?P<tz>%s))?' %
           (RAWTIME_RE, AMPM_RE, TIMEZONE_RE))
DATETIME_RE = (r'(?P<date>%s)(?P<separator>[T ])(?P<time>%s)'
               % (DATE_RE, TIME_RE))

def normalize_datetime(dtstr, match=None):
        """Try to normalize a datetime string.
        1. Convert 12-hour time to 24-hour time

        pass match in if we have already calculated it to avoid rework
        """
        match = match or (dtstr and re.match(DATETIME_RE + '$', dtstr))
        if match:
            datestr = match.group('date')
            hourstr = match.group('hour')
            minutestr = match.group('minute') or '00'
            secondstr = match.group('second')
            ampmstr = match.group('ampm')
            separator = match.group('separator')
            if ampmstr:
                hourstr = match.group('hour')
                if ampmstr.startswith('p'):
                    hourstr = str(int(hourstr) + 12)
            dtstr = '%s%s%s:%s' % (
                datestr, separator, hourstr, minutestr)

            if secondstr:
                dtstr += ':'+secondstr

            tzstr = match.group('tz')
            if tzstr:
                dtstr += tzstr
        return dtstr

