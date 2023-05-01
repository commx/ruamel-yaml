
import ruamel.yaml
from ruamel.yaml.composer import Composer
from ruamel.yaml.constructor import Constructor
from ruamel.yaml.resolver import Resolver


class CanonicalError(ruamel.yaml.YAMLError):
    pass


class CanonicalScanner:
    def __init__(self, data):
        try:
            if isinstance(data, bytes):
                data = data.decode('utf-8')
        except UnicodeDecodeError:
            raise CanonicalError('utf-8 stream is expected')
        self.data = data + '\0'
        self.index = 0
        self.tokens = []
        self.scanned = False

    def check_token(self, *choices):
        if not self.scanned:
            self.scan()
        if self.tokens:
            if not choices:
                return True
            for choice in choices:
                if isinstance(self.tokens[0], choice):
                    return True
        return False

    def peek_token(self):
        if not self.scanned:
            self.scan()
        if self.tokens:
            return self.tokens[0]

    def get_token(self, choice=None):
        if not self.scanned:
            self.scan()
        token = self.tokens.pop(0)
        if choice and not isinstance(token, choice):
            raise CanonicalError('unexpected token ' + repr(token))
        return token

    def get_token_value(self):
        token = self.get_token()
        return token.value

    def scan(self):
        self.tokens.append(ruamel.yaml.StreamStartToken(None, None))
        while True:
            self.find_token()
            ch = self.data[self.index]
            if ch == '\0':
                self.tokens.append(ruamel.yaml.StreamEndToken(None, None))
                break
            elif ch == '%':
                self.tokens.append(self.scan_directive())
            elif ch == '-' and self.data[self.index : self.index + 3] == '---':
                self.index += 3
                self.tokens.append(ruamel.yaml.DocumentStartToken(None, None))
            elif ch == '[':
                self.index += 1
                self.tokens.append(ruamel.yaml.FlowSequenceStartToken(None, None))
            elif ch == '{':
                self.index += 1
                self.tokens.append(ruamel.yaml.FlowMappingStartToken(None, None))
            elif ch == ']':
                self.index += 1
                self.tokens.append(ruamel.yaml.FlowSequenceEndToken(None, None))
            elif ch == '}':
                self.index += 1
                self.tokens.append(ruamel.yaml.FlowMappingEndToken(None, None))
            elif ch == '?':
                self.index += 1
                self.tokens.append(ruamel.yaml.KeyToken(None, None))
            elif ch == ':':
                self.index += 1
                self.tokens.append(ruamel.yaml.ValueToken(None, None))
            elif ch == ',':
                self.index += 1
                self.tokens.append(ruamel.yaml.FlowEntryToken(None, None))
            elif ch == '*' or ch == '&':
                self.tokens.append(self.scan_alias())
            elif ch == '!':
                self.tokens.append(self.scan_tag())
            elif ch == '"':
                self.tokens.append(self.scan_scalar())
            else:
                raise CanonicalError('invalid token')
        self.scanned = True

    DIRECTIVE = '%YAML 1.1'

    def scan_directive(self):
        if (
            self.data[self.index : self.index + len(self.DIRECTIVE)] == self.DIRECTIVE
            and self.data[self.index + len(self.DIRECTIVE)] in ' \n\0'
        ):
            self.index += len(self.DIRECTIVE)
            return ruamel.yaml.DirectiveToken('YAML', (1, 1), None, None)
        else:
            raise CanonicalError('invalid directive')

    def scan_alias(self):
        if self.data[self.index] == '*':
            TokenClass = ruamel.yaml.AliasToken
        else:
            TokenClass = ruamel.yaml.AnchorToken
        self.index += 1
        start = self.index
        while self.data[self.index] not in ', \n\0':
            self.index += 1
        value = self.data[start : self.index]
        return TokenClass(value, None, None)

    def scan_tag(self):
        self.index += 1
        start = self.index
        while self.data[self.index] not in ' \n\0':
            self.index += 1
        value = self.data[start : self.index]
        if not value:
            value = '!'
        elif value[0] == '!':
            value = 'tag:yaml.org,2002:' + value[1:]
        elif value[0] == '<' and value[-1] == '>':
            value = value[1:-1]
        else:
            value = '!' + value
        return ruamel.yaml.TagToken(value, None, None)

    QUOTE_CODES = {'x': 2, 'u': 4, 'U': 8}

    QUOTE_REPLACES = {
        '\\': '\\',
        '"': '"',
        ' ': ' ',
        'a': '\x07',
        'b': '\x08',
        'e': '\x1B',
        'f': '\x0C',
        'n': '\x0A',
        'r': '\x0D',
        't': '\x09',
        'v': '\x0B',
        'N': '\u0085',
        'L': '\u2028',
        'P': '\u2029',
        '_': '_',
        '0': '\x00',
    }

    def scan_scalar(self):
        self.index += 1
        chunks = []
        start = self.index
        ignore_spaces = False
        while self.data[self.index] != '"':
            if self.data[self.index] == '\\':
                ignore_spaces = False
                chunks.append(self.data[start : self.index])
                self.index += 1
                ch = self.data[self.index]
                self.index += 1
                if ch == '\n':
                    ignore_spaces = True
                elif ch in self.QUOTE_CODES:
                    length = self.QUOTE_CODES[ch]
                    code = int(self.data[self.index : self.index + length], 16)
                    chunks.append(chr(code))
                    self.index += length
                else:
                    if ch not in self.QUOTE_REPLACES:
                        raise CanonicalError('invalid escape code')
                    chunks.append(self.QUOTE_REPLACES[ch])
                start = self.index
            elif self.data[self.index] == '\n':
                chunks.append(self.data[start : self.index])
                chunks.append(' ')
                self.index += 1
                start = self.index
                ignore_spaces = True
            elif ignore_spaces and self.data[self.index] == ' ':
                self.index += 1
                start = self.index
            else:
                ignore_spaces = False
                self.index += 1
        chunks.append(self.data[start : self.index])
        self.index += 1
        return ruamel.yaml.ScalarToken("".join(chunks), False, None, None)

    def find_token(self):
        found = False
        while not found:
            while self.data[self.index] in ' \t':
                self.index += 1
            if self.data[self.index] == '#':
                while self.data[self.index] != '\n':
                    self.index += 1
            if self.data[self.index] == '\n':
                self.index += 1
            else:
                found = True


class CanonicalParser:
    def __init__(self):
        self.events = []
        self.parsed = False

    def dispose(self):
        pass

    # stream: STREAM-START document* STREAM-END
    def parse_stream(self):
        self.get_token(ruamel.yaml.StreamStartToken)
        self.events.append(ruamel.yaml.StreamStartEvent(None, None))
        while not self.check_token(ruamel.yaml.StreamEndToken):
            if self.check_token(ruamel.yaml.DirectiveToken, ruamel.yaml.DocumentStartToken):
                self.parse_document()
            else:
                raise CanonicalError('document is expected, got ' + repr(self.tokens[0]))
        self.get_token(ruamel.yaml.StreamEndToken)
        self.events.append(ruamel.yaml.StreamEndEvent(None, None))

    # document: DIRECTIVE? DOCUMENT-START node
    def parse_document(self):
        # node = None
        if self.check_token(ruamel.yaml.DirectiveToken):
            self.get_token(ruamel.yaml.DirectiveToken)
        self.get_token(ruamel.yaml.DocumentStartToken)
        self.events.append(ruamel.yaml.DocumentStartEvent(None, None))
        self.parse_node()
        self.events.append(ruamel.yaml.DocumentEndEvent(None, None))

    # node: ALIAS | ANCHOR? TAG? (SCALAR|sequence|mapping)
    def parse_node(self):
        if self.check_token(ruamel.yaml.AliasToken):
            self.events.append(ruamel.yaml.AliasEvent(self.get_token_value(), None, None))
        else:
            anchor = None
            if self.check_token(ruamel.yaml.AnchorToken):
                anchor = self.get_token_value()
            tag = None
            if self.check_token(ruamel.yaml.TagToken):
                tag = self.get_token_value()
            if self.check_token(ruamel.yaml.ScalarToken):
                self.events.append(
                    ruamel.yaml.ScalarEvent(
                        anchor, tag, (False, False), self.get_token_value(), None, None
                    )
                )
            elif self.check_token(ruamel.yaml.FlowSequenceStartToken):
                self.events.append(ruamel.yaml.SequenceStartEvent(anchor, tag, None, None))
                self.parse_sequence()
            elif self.check_token(ruamel.yaml.FlowMappingStartToken):
                self.events.append(ruamel.yaml.MappingStartEvent(anchor, tag, None, None))
                self.parse_mapping()
            else:
                raise CanonicalError(
                    "SCALAR, '[', or '{' is expected, got " + repr(self.tokens[0])
                )

    # sequence: SEQUENCE-START (node (ENTRY node)*)? ENTRY? SEQUENCE-END
    def parse_sequence(self):
        self.get_token(ruamel.yaml.FlowSequenceStartToken)
        if not self.check_token(ruamel.yaml.FlowSequenceEndToken):
            self.parse_node()
            while not self.check_token(ruamel.yaml.FlowSequenceEndToken):
                self.get_token(ruamel.yaml.FlowEntryToken)
                if not self.check_token(ruamel.yaml.FlowSequenceEndToken):
                    self.parse_node()
        self.get_token(ruamel.yaml.FlowSequenceEndToken)
        self.events.append(ruamel.yaml.SequenceEndEvent(None, None))

    # mapping: MAPPING-START (map_entry (ENTRY map_entry)*)? ENTRY? MAPPING-END
    def parse_mapping(self):
        self.get_token(ruamel.yaml.FlowMappingStartToken)
        if not self.check_token(ruamel.yaml.FlowMappingEndToken):
            self.parse_map_entry()
            while not self.check_token(ruamel.yaml.FlowMappingEndToken):
                self.get_token(ruamel.yaml.FlowEntryToken)
                if not self.check_token(ruamel.yaml.FlowMappingEndToken):
                    self.parse_map_entry()
        self.get_token(ruamel.yaml.FlowMappingEndToken)
        self.events.append(ruamel.yaml.MappingEndEvent(None, None))

    # map_entry: KEY node VALUE node
    def parse_map_entry(self):
        self.get_token(ruamel.yaml.KeyToken)
        self.parse_node()
        self.get_token(ruamel.yaml.ValueToken)
        self.parse_node()

    def parse(self):
        self.parse_stream()
        self.parsed = True

    def get_event(self):
        if not self.parsed:
            self.parse()
        return self.events.pop(0)

    def check_event(self, *choices):
        if not self.parsed:
            self.parse()
        if self.events:
            if not choices:
                return True
            for choice in choices:
                if isinstance(self.events[0], choice):
                    return True
        return False

    def peek_event(self):
        if not self.parsed:
            self.parse()
        return self.events[0]


class CanonicalLoader(CanonicalScanner, CanonicalParser, Composer, Constructor, Resolver):
    def __init__(self, stream):
        if hasattr(stream, 'read'):
            stream = stream.read()
        CanonicalScanner.__init__(self, stream)
        CanonicalParser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)


ruamel.yaml.CanonicalLoader = CanonicalLoader


def canonical_scan(stream):
    yaml = ruamel.yaml.YAML()
    yaml.scanner = CanonicalScanner
    return yaml.scan(stream)


ruamel.yaml.canonical_scan = canonical_scan


def canonical_parse(stream):
    yaml = ruamel.yaml.YAML()
    return yaml.parse(stream, Loader=CanonicalLoader)


ruamel.yaml.canonical_parse = canonical_parse


def canonical_compose(stream):
    yaml = ruamel.yaml.YAML()
    return yaml.compose(stream, Loader=CanonicalLoader)


ruamel.yaml.canonical_compose = canonical_compose


def canonical_compose_all(stream):
    yaml = ruamel.yaml.YAML()
    return yaml.compose_all(stream, Loader=CanonicalLoader)


ruamel.yaml.canonical_compose_all = canonical_compose_all


def canonical_load(stream):
    yaml = ruamel.yaml.YAML()
    return yaml.load(stream, Loader=CanonicalLoader)


ruamel.yaml.canonical_load = canonical_load


def canonical_load_all(stream):
    yaml = ruamel.yaml.YAML(typ='safe', pure=True)
    yaml.Loader = CanonicalLoader
    return yaml.load_all(stream)


ruamel.yaml.canonical_load_all = canonical_load_all
