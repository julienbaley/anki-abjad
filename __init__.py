# -*- coding: utf-8 -*-
# Copyright: Julien Baley <julien.baley@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# USER MANUAL:
# This plug-in helps user removing diacritics from Arabic, Hebrew and Syriac.
# This can for instance be used to display the sentence without diacritics
# in the question, and display them in the answer.

# For Arabic, if your current template is {{Front}}, replace it
# with {{plain_arabic_except(hamza, shadda):Front}} #to display Arabic
# stripped of all diacritics except hamza and shadda. For completely
# plain Arabic, use {{plain_arabic_except():Field}}.

# Supported exceptions can be found in the dictionary just below. If the
# diacritic you want to retain is not there, find its Unicode point, add it in
# the relevant section and restart Anki.

CHARACTERS = {'arabic': {'hamza': [0x0621, 0x654, 0x655],
                         'shadda': [0x0651]},
              'hebrew': {},
              'syriac': {}}

# THE CODE THEREAFTER SHOULDN'T BE MODIFIED UNLESS YOU KNOW WHAT YOU DO #

import re
import unicodedata
from itertools import chain

import anki

UNICODE_RANGES = {'arabic': set(chain(range(0x0600, 0x06FF),
                                      range(0x0750, 0x077F),
                                      range(0x08A0, 0x08FF),
                                      range(0xFB50, 0xFDFF),
                                      range(0xFE70, 0xFEFF),
                                      range(0x10E60, 0x10E7F))),
                  'hebrew': set(range(0x0590, 0x05FF)),
                  'syriac': set(range(0x0700, 0x074F))}
SUPPORTED_SCRIPTS = set(UNICODE_RANGES)
PATTERN = r'plain_(?P<lang>{langs})_except\((?P<excs>.*?)\)'

FILTER_MATCHER = re.compile(PATTERN.format(langs='|'.join(SUPPORTED_SCRIPTS)))


def remove_diacritics_filter(field_text, field_name, filter_name, _):
    match = FILTER_MATCHER.match(filter_name)
    if match:
        lang = match.group('lang')
        incl = UNICODE_RANGES[lang]
        try:
            excl = {chr(c)
                    for k in match.group('excs').split(',')
                    for c in CHARACTERS[lang][k]}
        except (AttributeError, KeyError) as e:
            excl = set()

        nkfd_form = unicodedata.normalize('NFKD', field_text)
        keep = ''.join(c
                       for c in nkfd_form
                       if ord(c) not in incl  # not a char from desired script
                       or c in excl  # explicitly excluded from removal
                       or not unicodedata.combining(c)  # not a diacritic
                       )
        field_text = unicodedata.normalize('NFKC', keep)

    return field_text

anki.hooks.field_filter.append(remove_diacritics_filter)
