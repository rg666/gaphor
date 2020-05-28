"""
Base code for presentation elements
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Generic, List, Optional, TypeVar

from gaphor.core.modeling import Element
from gaphor.core.modeling.properties import association, attribute, relation_one

if TYPE_CHECKING:
    from gaphas.canvas import Canvas  # noqa
    from gaphas.connector import Handle  # noqa
    from gaphas.matrix import Matrix  # noqa

S = TypeVar("S", bound=Element)


class Stylesheet(Element):
    stylesheet: attribute[str] = attribute("stylesheet", str)

    def item_style(self, item):
        return {
            "color": (0.05, 0.05, 0.3, 1),
            "text-color": (0, 0, 0, 1),
            "background-color": (0.01, 0.01, 0.95, 0.2),
            "font-size": 28,
        }


class Presentation(Element, Generic[S]):
    """
    This presentation is used to link the behaviors of `gaphor.core.modeling` and `gaphas.Item`.
    """

    def __init__(self, id=None, model=None):
        super().__init__(id, model)

        def update(event):
            self.request_update()

        self._watcher = self.watcher(default_handler=update)

        self.watch("subject")

    subject: relation_one[S] = association(
        "subject", Element, upper=1, opposite="presentation"
    )

    @property
    def stylesheet(self) -> Optional[Stylesheet]:
        return next(self.model.select(Stylesheet), None,)  # type: ignore[arg-type]

    @property
    def style(self):
        sheet = self.stylesheet
        return sheet and sheet.item_style(self) or {}

    handles: Callable[[Presentation], List[Handle]]
    request_update: Callable[[Presentation], None]

    canvas: Optional[Canvas]

    matrix: Matrix

    def watch(self, path, handler=None):
        """
        Watch a certain path of elements starting with the DiagramItem.
        The handler is optional and will default to a simple
        self.request_update().

        Watches should be set in the constructor, so they can be registered
        and unregistered in one shot.

        This interface is fluent(returns self).
        """
        self._watcher.watch(path, handler)
        return self

    def subscribe_all(self):
        """
        Subscribe all watched paths, as defined through `watch()`.
        """
        self._watcher.subscribe_all()

    def unsubscribe_all(self):
        """
        Subscribe all watched paths, as defined through `watch()`.
        """
        self._watcher.unsubscribe_all()

    def unlink(self):
        """
        Remove the item from the canvas and set subject to None.
        """
        if self.canvas:
            self.canvas.remove(self)
        super().unlink()


Element.presentation = association(
    "presentation", Presentation, composite=True, opposite="subject"
)
