from enum import Enum

from .has_node_reference import HasNodeReference
from .. import Node
from ..settings import NodePropertyInfo


class ProduceTextAlgorithm(Enum):
    """ProduceTextAlgorithm class.
    Enum class with the different algorithms to produce the text of an annotation.
    """

    NOTHING = 0            # just the raw text
    PROPERTY = 1           # the text is a property of the node, nicely formatted using docs
    PROPERTY_RAW = 2       # the text is a property of the node, but not formatted
    EVAL = 3               # the text is evaluated as python code, the result is used a label. The node is available as 'node'


class TextProducer(HasNodeReference):
    """TextProducer class.

    TextProducer objects are used to provide the text of an annotation.

    The text of an annotation is provided by the get_text() method.

    Optionally, the text can be formatted using a format string (ff).
    Optionally the text can be hidden using the hide property, which can either be a bool or something to be evaluated.

    """

    def __init__(self,
                 node : Node,
                 text : str ,
                 how  : ProduceTextAlgorithm = ProduceTextAlgorithm.NOTHING,
                 ff : str or None = None):
        self._node : Node or None = node
        self._text : str = text
        self._how = how
        self.ff : str or None = ff  # format string, eg "{:.3f}"

        self._hide: bool or str = False

        self._property_documentation : NodePropertyInfo or None = None

        self._changed()

    @property
    def hide(self):
        return self._hide

    @hide.setter
    def hide(self, value):
        assert isinstance(value, (bool, str)), f'hide must be a boolean or a string, got {type(value)}'
        self._hide = value

    @property
    def hidden(self):
        if self._hide == False:
            return False
        if self._hide == True:
            return True

        assert isinstance(self._hide, str), f'if _hide is not a boolean then it must be a string, got {type(self._hide)}'

        r =  eval(self._hide, {"node": self._node})
        assert isinstance(r, bool), f'evaluated hide must be a boolean, got {type(r)} when evaluating {self._hide}'

        return r

    def as_dict(self):

        assert self.is_valid

        return {
            "node": self._node.name,
            "text": self._text,
            "how": self._how.value,
            "ff": self.ff if self.ff is not None else ""
        }

    @staticmethod
    def from_dict(d, scene):
        node = scene[d["node"]]
        tp =  TextProducer(node, d["text"], ProduceTextAlgorithm(d["how"]))
        if d["ff"]:
            tp.ff = d["ff"]
        return tp

    def _changed(self):
        if not self.is_valid:
            raise ValueError('Node is not valid')

        if self._how == ProduceTextAlgorithm.PROPERTY:
            documentation = self._node._scene.give_documentation(self._node, self._text)
            if documentation is None:
                raise ValueError('Could not find documentation for property "{}" of node "{}"'.format(self._text, self._node))

            self._property_documentation = documentation

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value : str):
        self._text = value
        self._changed()

    @property
    def how(self) -> ProduceTextAlgorithm:
        return self._how

    @how.setter
    def how(self, value : ProduceTextAlgorithm):
        self._how = value
        self._changed()

    @property
    def node(self) -> Node:
        return self._node

    @node.setter
    def node(self, value : Node):
        self._node = value
        self._changed()


    def get_text(self) -> str:

        if self.hidden:
            return ""

        if self._how == ProduceTextAlgorithm.PROPERTY or self._how == ProduceTextAlgorithm.PROPERTY_RAW:

            value = getattr(self._node, self._text, None)
            if value is None:
                return ""


            if self.ff is not None:
                value = self.ff.format(value)
            else:
                if isinstance(value, float):
                    value = "{:.3f}".format(value)
                else:
                    value = str(value)

            if self._how == ProduceTextAlgorithm.PROPERTY_RAW:
                return str(value)

            if self._property_documentation is None:
                raise ValueError('No property documentation - call _changed() first')

            # format the value
            doc = self._property_documentation # alias

            if doc.units:
                value += " " + doc.units

            value = self._text + " = " + value

            return value

        elif self._how == ProduceTextAlgorithm.EVAL:
            try:
                value = eval(self._text, {"node": self._node})
            except Exception as e:
                value = 'ERROR:\n' + str(e)

            return value

        elif self._how == ProduceTextAlgorithm.NOTHING:
            return self._text

        else:
            raise ValueError('Unknown ProduceTextAlgorithm')


    def update(self):
        pass

    @property
    def is_valid(self):
        if self._node is None:
            return True

        return self._node.is_valid
