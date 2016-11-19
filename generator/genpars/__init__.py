import re


class Container(object):
    """
    Abstract container class which makes everything that inherits from it behave like a list.
    """

    def __init__(self, items=None):
        """
        Create new container, optionally preset with given items.

        :param items:       Items to preset the container with
        """

        if items is None:
            self.items = []
        else:
            self.items = items

    def append(self, item):
        """
        Add a new item to the container data.

        :param item:        Item to add
        """
        self.items.append(item)

    def __getitem__(self, idx):
        """
        Allow support of the [] operator.

        :param idx:     Index which should be accessed.
        :return:        Item from container on given index
        """
        return self.items[idx]

    def __iter__(self):
        """
        Support iteration.

        :return:        Yields one item from items
        """

        for d in self.items:
            yield d

    def __len__(self):
        """
        Number of items in this container.

        :return:        Number of items in this container
        """
        return len(self.items)


class Tok(object):
    """
    Class to represent a token defined by a token kind and the token value. This class is used for the input tokens,
    as well as for the rules in the grammar defining the expected tokens.
    """

    def __init__(self, kind, value=None, neg_kind=False, neg_value=False):
        """
        Create a new Token representation.

        :param kind:        The token kind (the token kinds need to be defined from the outside).
                            For tokens from the input stream, this needs to be a defined value.
                            For matching tokens in a rule (by using == or __eq__), this could be:
                                - None (default): this matches every kind of the input token
                                - Kind: the kind of the input token must match the output token
                                - List of kinds: the input token kind must be in this list
        :param value:       For tokens from the input stream, this is the value found.
                            For matching tokens in a rule (by using == or __eq__), this could be:
                                - None (default): this matches every value of the input token
                                - Value: the value of the input token must match the output token
                                - List of values: the input token value must be in this list
        :param neg_kind:    If this is True, matching for the kind is negated
        :param neg_value:   If this is True, matching for the value is negated
        """

        self._kind = kind
        self._value = value
        self.neg_kind = neg_kind
        self.neg_value = neg_value

    @property
    def kind(self):
        """
        Get the kind of this token.

        :return:        The kind of this token
        """
        return self._kind

    @property
    def value(self):
        """
        Get the value of this token.

        :return:        The value of this token
        """
        return self._value

    def __eq__(self, other):
        """
        Compare two tokens (used for matching).

        :param other:       Other token to compare this one with
        :return:            True if tokens equal, False otherwise
        """

        if not isinstance(other.kind, list):
            k0 = [other.kind]
        else:
            k0 = other.kind

        if not isinstance(other.value, list):
            v0 = [other.value]
        else:
            v0 = other.value

        if not isinstance(self.kind, list):
            k1 = [self.kind]
        else:
            k1 = self.kind

        if not isinstance(self.value, list):
            v1 = [self.value]
        else:
            v1 = self.value

        neg_kind = self.neg_kind or other.neg_kind
        neg_value = self.neg_value or other.neg_value

        if v0 == [None] or v1 == [None]:
            result = (len(list(set(k0) & set(k1))) and not neg_kind)
        else:
            k = len(list(set(k0) & set(k1)))
            v = len(list(set(v0) & set(v1)))

            if neg_kind:
                k = not k

            if neg_value:
                v = not v

            result = k and v

        return bool(result)

    def __repr__(self):
        """
        Represent this token.

        :return:        String to represent this token
        """

        if isinstance(self.kind, str):
            k = "'%s'" % self.kind
        else:
            k = str(self.kind)

        if isinstance(self.value, str):
            v = "'%s'" % self.value
        else:
            v = str(self.value)

        return "Token(%s, %s, neg_kind=%s, neg_value=%s)" % (k, v, self.neg_kind, self.neg_value)


class Consumer(Container):
    """
    Abstract class all consumers inherit from.
    """

    def __init__(self, *args, **kwargs):
        """
        Construct a consumer.

        :param args:        List of tokens (Tok) and consumers (ConsAND, ConsOR, ConsMULT)
        :param kwargs:      Additional arguments:
                            - action: callback function called when the consumer consumed successfully
                                (takes tokens as an argument)
        """

        Container.__init__(self, list(args))

        if "action" in kwargs:
            self.action = kwargs["action"]
        else:
            self.action = None

    def __repr__(self):
        """
        Represent a consumer as a string.

        :return:        Consumer string representation
        """

        param = ""
        action = None

        if isinstance(self.items, list):
            for i in self.items:
                if len(param) > 0:
                    param += ", "
                param += i.__repr__()

        if self.action is not None:
            action = self.action.__name__

        return "%s(%s, action=%s)" % (self.__class__.__name__, param, action)

    def match(self, inp):
        """
        Try to match expected tokens against input, and if they match , consume them from the input.

        :param inp:     List of input tokens
        :return:        Number of tokens consumed from the input
        """
        return 0


class AND(Consumer):
    """
    AND consumer: every token or other operation inside an AND operation need to match and consume from
    the input token list.
    """

    def match(self, inp):
        """
        Try to match expected tokens against input, and if they match , consume them from the input.
        This consumer only consumes when all sub-consumers consumed (AND).

        :param inp:     List of input tokens
        :return:        Number of tokens consumed from the input
        """

        and_complete = len(self.items)
        matches = 0
        work = inp

        for t in self.items:
            if isinstance(t, Consumer) and len(work):
                r = t.match(work)
                if r:
                    and_complete -= 1

                matches += r
                work = work[matches:]
            elif len(work):
                if work[0] == t:
                    matches += 1
                    work = work[1:]
                    and_complete -= 1
                else:
                    return 0

        if and_complete > 0:
            matches = 0
        elif self.action is not None:
            self.action(inp[:matches])

        return matches


class OR(Consumer):
    """
    OR consumer: might or might not consume form the input token list.
    """

    def match(self, inp):
        """
        Try to match expected tokens against input, and if they match , consume them from the input.
        This consumer only consumes when one of the sub-consumers consumed (OR).

        :param inp:     List of input tokens
        :return:        Number of tokens consumed from the input
        """
        matches = 0
        work = inp

        for i in self.items:
            if isinstance(i, Consumer) and len(work):
                matches += i.match(work)
                if matches:
                    return matches
            elif len(work):
                if work[0] == i:
                    matches += 1
                    break

        if matches and self.action is not None:
            self.action(inp[:matches])

        return matches


class MULT(Consumer):
    """
    Take a consumer and repeats it until no more tokens could be consumed from the input tokens.
    """

    def match(self, inp):
        """
        This consumer executes the containing root consumer as long as that consumer consumed.

        :param inp:     List of input tokens
        :return:        Number of tokens that could be consumed from the input
        """

        matches = 0

        while True:
            m = self.items[0].match(inp)
            inp = inp[m:]

            if m > 0:
                matches += m
            else:
                break

        if matches and self.action is not None:
            self.action(inp[:matches])

        return matches


class Rule(object):
    """
    A single rule of the grammar.
    """

    def __init__(self, root_cons):
        """
        Create a rule with a given root consumer.

        :param root_cons:       The root consumer of this rule
        """

        assert isinstance(root_cons, Consumer)

        self.root_cons = root_cons

    def match(self, inp):
        """
        Try to match this rule to the input tokens.

        :param inp:     Input tokens
        :return:        Number of tokens that could be consumed from the input
        """

        matched = self.root_cons.match(inp)

        return matched

    def __repr__(self):
        """
        Represent a rule as a string.

        :return:        Rule string representation
        """
        return "%s(%s)" % (self.__class__.__name__, self.root_cons.__repr__())


class Grammar(Container):
    """
    The whole grammar (made up of rules)
    """

    def __init__(self, rules=None):
        """
        Create a grammar.

        :param rules:       List of rules that make up the grammar
        """
        Container.__init__(self, rules)


class Scanner:
    """
    Scanner used by the tokenizer
    """

    def __init__(self, lexicon, flags=0):
        """
        Create a parser from a given lexicon.

        :param lexicon:     Lexicon in the form of list, each entry with:
                            (<regex>, lambda scanner, token: Tok(<kind>, <value>)))
        :param flags:       Extra flags for parsing.
        """

        import sre_parse
        import sre_compile
        from sre_constants import BRANCH, SUBPATTERN

        self.lexicon = lexicon

        # combine phrases into a compound pattern
        p = []
        s = sre_parse.Pattern()
        s.flags = flags
        for phrase, action in lexicon:
            p.append(sre_parse.SubPattern(s, [
                (SUBPATTERN, (len(p)+1, sre_parse.parse(phrase, flags))),
                ]))

        s.groups = len(p)+1
        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile.compile(p, re.MULTILINE)

    def scan(self, string):
        """
        Scan the input string, return a list of tokens.

        :param string:      Input string to scan
        :return:            List of tokens (Tok)
        """

        result = []
        append = result.append
        match = self.scanner.scanner(string).match
        i = 0

        while 1:
            m = match()
            if not m:
                break
            j = m.end()
            if i == j:
                break
            action = self.lexicon[m.lastindex-1][1]
            if hasattr(action, '__call__'):
                self.match = m
                action = action(self, m.group())
            if action is not None:
                append(action)
            i = j

        return result, string[i:]


class Tokenizer(Container):
    """
    A tokenizer.
    """

    def __init__(self, patterns=None):
        """
        Create a tokenizer from a list of patterns.

        :param patterns:    Patterns in the form of list, each entry with:
                            (<regex>, lambda scanner, token: Tok(<kind>, <value>)))
        """
        Container.__init__(self, patterns)

    def tokenize(self, inp):
        """
        Tokenize the input string.

        :param inp:         Input string
        :return:            List of tokens (Tok)
        """
        scanner = Scanner(self.items)

        return scanner.scan(inp)[0]

    def __repr__(self):
        """
        String representation of this Tokenizer.

        :return:            String representation.
        """
        return "%s()" % self.__class__.__name__


class Parser(object):
    """
    Complete parser using a tokenizer and a grammar to do it's work
    """

    def __init__(self, tokenizer, grammar):
        """
        Create a parser.

        :param tokenizer:       The tokenizer to use (Tokenizer)
        :param grammar:         The grammar to use (Grammar)
        """

        assert isinstance(tokenizer, Tokenizer)
        assert isinstance(grammar, Grammar)

        self.tokenizer = tokenizer
        self.grammar = grammar

    def parse(self, inp):
        """
        Parse the input by first tokenizing it, and than applying the grammar.

        :param inp:             Input string
        :return:                Tuple: True/False on success/failure, Tokens not parsed
        """

        tokens = self.tokenizer.tokenize(inp)
        tokens_left = len(tokens)

        # print(tokens)

        while tokens_left:

            for rule in self.grammar:
                tokens = tokens[rule.match(tokens):]

            if len(tokens) < tokens_left:
                tokens_left = len(tokens)
            else:
                # nothing is matching any more - stop
                break

        return len(tokens) == 0, tokens

    def __repr__(self):
        """
        String representation of this Parser.

        :return:            String representation.
        """

        if self.tokenizer is not None:
            tok = self.tokenizer.__repr__()
        else:
            tok = None

        if self.grammar is not None:
            gr = self.grammar.__repr__()
        else:
            gr = None

        return "%s(%s, %s)" % (self.__class__.__name__, tok, gr)
