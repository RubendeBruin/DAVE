:mod:`DAVE.gui.helpers.highlighter`
===================================

.. py:module:: DAVE.gui.helpers.highlighter


Module Contents
---------------

.. function:: format(color, style='')

   Return a QTextCharFormat with the given attributes.


.. data:: STYLES
   

   

.. py:class:: PythonHighlighter(document)

   Bases: :class:`PySide2.QtGui.QSyntaxHighlighter`

   Syntax highlighter for the Python language.

   .. attribute:: keywords
      :annotation: = ['and', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 'try', 'while', 'yield', 'None', 'True', 'False']

      

   .. attribute:: operators
      :annotation: = ['=', '==', '!=', '<', '<=', '>', '>=', '\\+', '-', '\\*', '/', '//', '\\%', '\\*\\*', '\\+=', '-=', '\\*=', '/=', '\\%=', '\\^', '\\|', '\\&', '\\~', '>>', '<<']

      

   .. attribute:: braces
      :annotation: = ['\\{', '\\}', '\\(', '\\)', '\\[', '\\]']

      

   .. method:: highlightBlock(self, text)


      Apply syntax highlighting to the given block of text.


   .. method:: match_multiline(self, text, delimiter, in_state, style)


      Do highlighting of multi-line strings. ``delimiter`` should be a
      ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
      ``in_state`` should be a unique integer to represent the corresponding
      state changes when inside those strings. Returns True if we're still
      inside a multi-line string when this function is finished.



.. data:: app
   

   

