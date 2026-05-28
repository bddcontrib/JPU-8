from logging import Logger

from src.parsing.tokens import *
from src.parsing.stream_utils import TokenStream
from src.parsing.lexer import JSMLexer



class WTFError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Instruction:
    def __init__(self, data: int, intermediate: int | None = None):
        self.data: int = data
        self.intermediate: int = intermediate if intermediate is not None else 0

class InstructionPair:
    def __init__(self, flg_set_instruction: Instruction, flg_unset_instruction: Instruction):
        self.flg_set: Instruction = flg_set_instruction
        self.flg_unset: Instruction = flg_unset_instruction

class Assembler:
    # TODO: don't hardcode
    BASE_LIB_PATH = "./src/assembler/lib/"

    def __init__(self, logger: Logger):
        self.logger = logger
        self.dependencies = []
        self.entrypoint = None

    def assemble(self, code: str):
        lexer = JSMLexer()
        tokens = lexer.tokenize(code)
        token_stream = TokenStream(tokens)
        print(tokens)

        while not token_stream.is_empty():
            r = token_stream.match_one(token_type=TokenType.HASHTAG)
            if r is not None:
                token, option = token_stream.expect(
                    {"token_type": TokenType.KEYWORD, "subtype": KeywordType.CN_INCLUDE},
                    {"token_type": TokenType.KEYWORD, "subtype": KeywordType.CN_ENTRYPOINT},
                    {"token_type": TokenType.KEYWORD, "subtype": KeywordType.CN_MACRO},
                    {"token_type": TokenType.KEYWORD, "subtype": KeywordType.CN_DEFINE},
                )

                match option:
                    case 0: # include
                        lib = token_stream.expect_one(token_type=TokenType.IDENTIFIER)
                        with open(self.BASE_LIB_PATH + lib.value, "r" ) as f:
                            new_code = f.read()
                            new_tokens = lexer.tokenize(new_code)
                            token_stream.extend_head(new_tokens)
                        token_stream.expect_one(token_type=TokenType.EOL)
                    case 1: # entrypoint
                        tok = token_stream.expect(
                            {"token_type": TokenType.IDENTIFIER},
                            {"token_type": TokenType.LITERAL, "subtype": LiteralType.NUMBER}
                        )
                    case 2: # macro
                        pass
                    case 3: # define
                        pass
