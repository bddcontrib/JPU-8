from src.parsing.tokens import *
from abc import ABC, abstractmethod


class AbstractLexer(ABC):
    @staticmethod
    @abstractmethod
    def get_config() -> tuple[dict[str, tuple], list[str], list[str], list[str]]:
        pass

    def __init__(self):
        self.token_map, self.delimiters, self.pseudo_delimiters, self.string_delimiters = self.get_config()

    def attempt_tokenization(self, string: str, line: int, column: int, force=False) -> Token | None:
        if string in self.token_map:
            return Token(*self.token_map[string], line=line, column=(column - len(string)))

        if string[0] in self.string_delimiters and string[-1] in self.string_delimiters and len(string) >= 2:
            return Token(TokenType.LITERAL, LiteralType.STRING, value=string[1:-1], line=line, column=(column - len(string)))

        if force:
            try:
                return Token(TokenType.LITERAL, LiteralType.NUMBER, value=int(string, 0), line=line, column=(column - len(string)))
            except ValueError:
                return Token(TokenType.IDENTIFIER, value=string, line=line, column=(column - len(string)))

        return None


    def tokenize(self, to_parse: str):
        tokens: list[Token] = []
        line = 1
        column = 0
        char = -1
        total_length = len(to_parse)
        accumulator = ""

        inside_string = False
        inside_comment = False

        while char < total_length - 1:
            char += 1
            column += 1
            current_char = to_parse[char]

            if inside_comment and not current_char == "\n":
                continue

            if inside_string and not (current_char in self.string_delimiters):
                accumulator += current_char
                continue

            if current_char in self.delimiters or current_char in self.pseudo_delimiters:
                if accumulator == "/" and current_char == "/":
                    inside_comment = True
                    accumulator = ""
                    continue

                if accumulator and not inside_string:
                    token = self.attempt_tokenization(accumulator, line, column, force=True)
                    assert token is not None
                    tokens.append(token)
                    accumulator = ""
                
                if current_char == "\n":
                    line += 1
                    column = 0
                    inside_comment = False

            if not (current_char in self.delimiters):
                if current_char in self.string_delimiters:
                    inside_string = not inside_string

                accumulator += current_char
                if len(accumulator) == 1:
                    # Försök ej tokeniza längre namn, som inte kan vara inline
                    # Annars kommer `function_test();` tokeniza `func`
                    result = self.attempt_tokenization(accumulator, line, column)
                    if result is not None:
                        tokens.append(result)
                        accumulator = ""

        return tokens


class JScriptLexer(AbstractLexer):
    @staticmethod
    def get_config() -> tuple[dict[str, tuple], list[str], list[str], list[str]]:
        token_map = {
            "(": (TokenType.OPENING_PARENTHESIS,),
            ")": (TokenType.CLOSING_PARENTHESIS,),
            "[": (TokenType.OPENING_SQUARE_BRACKET,),
            "]": (TokenType.CLOSING_SQUARE_BRACKET,),
            "{": (TokenType.OPENING_CURLY_BRACKET,),
            "}": (TokenType.CLOSING_CURLY_BRACKET,),
            ";": (TokenType.SEMICOLON,),
            "#": (TokenType.HASHTAG,),
            ",": (TokenType.COMMA,),
            ".": (TokenType.DOT,),

            "+": (TokenType.OPERAND, OperandType.PLUS),
            "-": (TokenType.OPERAND, OperandType.MINUS),
            "*": (TokenType.OPERAND, OperandType.STAR),
            "&": (TokenType.OPERAND, OperandType.AMPERSAND),
            "|": (TokenType.OPERAND, OperandType.PIPE),
            "^": (TokenType.OPERAND, OperandType.UP_ARROW),
            "~": (TokenType.OPERAND, OperandType.TILDE),

            "=": (TokenType.OPERAND, OperandType.EQUALITY),
            ">": (TokenType.OPERAND, OperandType.GREATER_THAN),
            "<": (TokenType.OPERAND, OperandType.LESS_THAN),
            "!": (TokenType.OPERAND, OperandType.EXCLAMATION),

            "if": (TokenType.KEYWORD, KeywordType.IF),
            "else": (TokenType.KEYWORD, KeywordType.ELSE),
            "func": (TokenType.KEYWORD, KeywordType.FUNCTION),
            "return": (TokenType.KEYWORD, KeywordType.RETURN),
            "while": (TokenType.KEYWORD, KeywordType.WHILE),
            "type": (TokenType.KEYWORD, KeywordType.TYPE),

            "define": (TokenType.KEYWORD, KeywordType.CN_DEFINE),
            "macro": (TokenType.KEYWORD, KeywordType.CN_MACRO),
            "entrypoint": (TokenType.KEYWORD, KeywordType.CN_ENTRYPOINT),
        }

        delimiters = [" ", "\n", "\t"]
        pseudo_delimiters = ["(", ")", "[", "]", "{", "}", ";", "+", "-", "*", "&", "|", "^", "~",
                             "=", ">", "<", "!", "/", ",", "."]
        string_delimiters = ["\"", "\'"]

        return token_map, delimiters, pseudo_delimiters, string_delimiters

class JSMLexer(AbstractLexer):
    @staticmethod
    def get_config() -> tuple[dict[str, tuple], list[str], list[str], list[str]]:
        token_map = {
            "[": (TokenType.OPENING_SQUARE_BRACKET,),
            "]": (TokenType.CLOSING_SQUARE_BRACKET,),
            "#": (TokenType.HASHTAG,),
            ".": (TokenType.DOT,),

            "|": (TokenType.OPERAND, OperandType.PIPE),
            "\n": (TokenType.EOL,),

            "include": (TokenType.KEYWORD, KeywordType.CN_INCLUDE),
            "define": (TokenType.KEYWORD, KeywordType.CN_DEFINE),
            "macro": (TokenType.KEYWORD, KeywordType.CN_MACRO),
            "entrypoint": (TokenType.KEYWORD, KeywordType.CN_ENTRYPOINT),
        }

        delimiters = [" ", "\t"]
        pseudo_delimiters = ["\n", "[", "]", "|", "."]
        string_delimiters = ["\"", "\'", "<", ">"]

        return token_map, delimiters, pseudo_delimiters, string_delimiters
