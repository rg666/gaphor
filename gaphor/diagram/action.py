"""
Action diagram item.
"""

from math import pi

from gaphor import UML
from gaphor.diagram.nameditem import NamedItem
from gaphor.diagram.style import ALIGN_CENTER, ALIGN_MIDDLE
from gaphas.util import text_align, text_extents

class ActionItem(NamedItem):
    __uml__   = UML.Action
    __style__ = {
        'min-size':   (50, 30),
        'name-align': (ALIGN_CENTER, ALIGN_MIDDLE),
    }

    def pre_update(self, context):
        self.update_name_size(context)
        self.min_width, self.min_height = self.get_name_size()
        super(ActionItem, self).pre_update(context)

    def draw(self, context):
        """
        Draw action symbol.
        """
        c = context.cairo

        d = 15

        c.move_to(0, d)
        c.arc(d, d, d, pi, 1.5 * pi)
        c.line_to(self.width - d, 0)
        c.arc(self.width - d, d, d, 1.5 * pi, 0)
        c.line_to(self.width, self.height - d)
        c.arc(self.width - d, self.height - d, d, 0, 0.5 * pi)
        c.line_to(d, self.height)
        c.arc(d, self.height - d, d, 0.5 * pi, pi)
        c.close_path()

        c.stroke()

        super(ActionItem, self).draw(context)


# vim:sw=4:et
