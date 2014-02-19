# -*- coding: utf-8 -*-
# Copyright: Julien Baley <julien.baley@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

#TO CUSTOMIZE THIS PLUGIN, SEE COMMENT AT THE BOTTOM OF THE FILE!

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
    self.incl = unicode_ranges[script]
    self.excl = [unichr(c) for c in exceptions]
    addHook('fmod_'+name, self.remove_diacritics)
  
  def remove_diacritics(self, txt, extra, *args): #extra/args are passed by Anki, not used
    nkfd_form = unicodedata.normalize('NFKD', txt)
    keep = "".join([c for c in nkfd_form if \
                    not (ord(c) in self.incl and unicodedata.combining(c)) \
                    or c in self.excl])
    return unicodedata.normalize('NFKC',keep)


#ADD YOUR HOOKS HERE
Hook(name='plain_arabic',script='arabic')
Hook(name='keep_shadda', script='arabic',exceptions=[0x0651,])
Hook(name='plain_hebrew',script='hebrew')
Hook(name='plain_syriac',script='syriac')
