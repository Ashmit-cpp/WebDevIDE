# importing required libraries
from PyQt5.QtWidgets import QWidget
from Modules import *


class Highlighter(QSyntaxHighlighter):
    # Python keywords
    keywords = [
        'and', 'DOCTYPE', 'break', 'class', 'continue', 'script',
        'del', 'elif', 'else', 'except', 'p', 'let',
            'for', 'from', 'global', 'if', 'href', 'in',
        'h2', 'lambda', 'not', 'or', 'pass', 'const',
        'raise', 'return', 'try', 'while', 'yield',
        'div', 'True', 'False', 'input', 'label', 'body',
        'html', 'style', 'head', 'title', 'form', 'hr', 'h1', 'var','link'

    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def format(color, style=''):
        """Return a QTextCharFormat with the given attributes.
        """
        _color = QColor()
        _color.setNamedColor(color)
        _format = QTextCharFormat()
        _format.setForeground(_color)
        if 'bold' in style:
            _format.setFontWeight(QFont.Bold)
        if 'italic' in style:
            _format.setFontItalic(True)

        return _format

    # Syntax styles that can be shared by all languages #C792EA
    STYLES = {
        'keyword': format('#FA1E70'),
        'operator': format('#58D1EB'),
        'brace': format('#58D1EB'),
        'def': format('#FA8419', 'bold'),
        'string': format('#D5B11E'),
        'string2': format('darkMagenta'),
        'comment': format('darkGrey', 'italic'),
        'self': format('#FF5360', 'italic'),
        'numbers': format('#9D65FF'),
    }

    def __init__(self, parent):
        super(Highlighter, self).__init__(parent)



        # Multi-line strings (expression, flag, style)
        self.tri_single = (QRegExp("'''"), 1, Highlighter.STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, Highlighter.STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, Highlighter.STYLES['keyword'])
                  for w in Highlighter.keywords]
        rules += [(r'%s' % o, 0, Highlighter.STYLES['operator'])
                  for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, Highlighter.STYLES['brace'])
                  for b in Highlighter.braces]

        # All other rules
        rules += [
            # From '//' until a newline
            (r'//[^\n]*', 0, Highlighter.STYLES['comment']),
            # 'self'
            (r'\bdocument\b', 0, Highlighter.STYLES['self']),
            (r'\bconsole\b', 0, Highlighter.STYLES['self']),
            (r'\bthis\b', 0, Highlighter.STYLES['self']),

            # 'def' followed by an identifier
            (r'\bconst\b\s*(\w+)', 1, Highlighter.STYLES['def']),
            (r'\blet\b\s*(\w+)', 1, Highlighter.STYLES['def']),
            (r'\bvar\b\s*(\w+)', 1, Highlighter.STYLES['def']),
            (r'\bclass\b\s*(\w+)', 1, Highlighter.STYLES['def']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, Highlighter.STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, Highlighter.STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, Highlighter.STYLES['numbers']),


            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, Highlighter.STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, Highlighter.STYLES['string']),


        ]

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QColor(152, 224, 36))

        self.highlightingRules = [((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                                    functionFormat))]
        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
            """

        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


        self.tripleQuoutesWithinStrings = []
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            if index >= 0:
                # if there is a string we check
                # if there are some triple quotes within the string
                # they will be ignored if they are matched again
                if expression.pattern() in [r'"[^"\\]*(\\.[^"\\]*)*"', r"'[^'\\]*(\\.[^'\\]*)*'"]:
                    innerIndex = self.tri_single[0].indexIn(text, index + 1)
                    if innerIndex == -1:
                        innerIndex = self.tri_double[0].indexIn(text, index + 1)

                    if innerIndex != -1:
                        tripleQuoteIndexes = range(innerIndex, innerIndex + 3)
                        self.tripleQuoutesWithinStrings.extend(tripleQuoteIndexes)

            while index >= 0:
                # skipping triple quotes within strings
                if index in self.tripleQuoutesWithinStrings:
                    index += 1
                    expression.indexIn(text, index)
                    continue

                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
            ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
            ``in_state`` should be a unique integer to represent the corresponding
            state changes when inside those strings. Returns True if we're still
            inside a multi-line string when this function is finished.
            """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # skipping triple quotes within strings
            if start in self.tripleQuoutesWithinStrings:
                return False
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
