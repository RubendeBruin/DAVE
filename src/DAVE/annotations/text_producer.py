from .has_node_reference import HasNodeReference
from .. import Node


class TextProducer(HasNodeReference):
    """TextProducer class.

    TextProducer objects are used to provide the text of an annotation.

    The text of an annotation is provided by the get_text() method.
    """

    def __init__(self):
        self.node : Node or None = None

    def get_text(self) -> str:
        return "Not implemented"

    def update(self):
        pass

    @property
    def is_valid(self):
        if self.node is None:
            return True

        return self.node.is_valid

class TextProducer_NodeProperty(TextProducer):
    """TextProducerProperty class.

    TextProducerProperty objects are used to provide the text of an annotation.

    The text of an annotation is provided by the get_text() method.
    """

    def __init__(self, node : Node, property : str, format : str = ""):
        """

        Args:
            node:
            property:
            format: example "{:.2f}"
        """
        super().__init__()

        self.node = node
        self.property = property
        self.format = format

    def get_text(self) -> str:
        value = getattr(self.node, self.property, None)
        if value is None:
            return ""

        if self.format:
            return self.format.format(value)

        return str(value)

class TextProducer_Eval(TextProducer):
    """TextProducer_Eval class.

    Evaluates a string as python code to get the text of an annotation.
    The string is evaluated with "node" as self.node.

    eg:     TextProducer_Eval(node, "Tension = {node.tension:.3f}")

    """

    def __init__(self, node: Node, code_to_eval: str):
        """
        Evaluates a string as python code to get the text of an annotation.
        The string is evaluated with "node" as self.node.

        eg:     TextProducer_Eval(node, 'f"Tension = {node.tension:.3f}"')

        """
        super().__init__()

        self.node = node
        self.code_to_eval = code_to_eval

    def get_text(self) -> str:
        try:
            value = eval(self.code_to_eval, {"node": self.node})
        except Exception as e:
            value = str(e)

        return value