# -*- coding: utf-8 -*-
# Copyright: Julien Baley <julien.baley@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

#USER MANUAL:
#This plug-in helps user removing diacritics from Arabic, Hebrew and Syriac.
#This can for instance be used to display the sentence without diacritics
#in the question, and display them in the answer. 

#For Arabic, if your current template is {{Front}}, replace it 
#with {{plain_arabic_except(hamza, shadda):Front}} #to display Arabic
#stripped of all diacritics except hamza and shadda. For completely 
#plain Arabic, have either {{plain_arabic_except:Field}}
#or {{plain_arabic_except():Field}}.

#Supported exceptions can be found in the dictionary just below. If the diacritic
#you want to retain is not there, find its Unicode point, add it in the relevant
#section and restart Anki.

characters = {'arabic':{'hamza': [0x0621,0x654,0x655],
                        'shadda':[0x0651,]},
              'hebrew':{},
              'syriac':{}}

##THE CODE THEREAFTER SHOULDN'T BE MODIFIED UNLESS YOU KNOW WHAT YOU DO#

from anki.hooks import addHook
from itertools import chain
import unicodedata

supported_scripts = ['arabic','hebrew','syriac']

unicode_ranges = {'arabic':set(chain(range(0x0600, 0x06FF),
                                     range(0x0750, 0x077F),
                                     range(0x08A0, 0x08FF),
                                     range(0xFB50, 0xFDFF),
                                     range(0xFE70, 0xFEFF),
                                     range(0x10E60, 0x10E7F))),
                  'hebrew':set(range(0x0590, 0x05FF)),
                  'syriac':set(range(0x0700, 0x074F))}

class Hook():
  def __init__(self, name, script, exceptions=[]):
    assert script in supported_scripts
    self.script = script
    self.incl = unicode_ranges[script]
    addHook('fmod_'+name, self.remove_diacritics)
  
  def remove_diacritics(self, txt, exc, *_):
    nkfd_form = unicodedata.normalize('NFKD', txt)
    try:
      excl = [unichr(c) for k in exc.split(',') for c in characters[self.script][k]]
    except (AttributeError, KeyError):
      excl = set()
    keep = "".join([c for c in nkfd_form if \
                    not (ord(c) in self.incl and unicodedata.combining(c)) \
                    or c in excl])
    return unicodedata.normalize('NFKC',keep)


#ADD YOUR HOOKS HERE
Hook(name='plain_arabic_except',script='arabic')
Hook(name='plain_hebrew_except',script='hebrew')
Hook(name='plain_syriac_except',script='syriac')
