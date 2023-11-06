class ModelInvalidException(Exception):
    """Exception raised when a model is invalid and should no longer be used.

    This can be raised for example when errors occur during the construction of a node and the node
    has to be left in an invalid state.

    In the GUI this will cause the model to be thrown away and restored to the last valid undo state.
    """

    pass
