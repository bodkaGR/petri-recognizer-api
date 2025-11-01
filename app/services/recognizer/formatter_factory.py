from app.domain.interfaces.i_formatter import IFormatter
from app.formatters.java_formatter import JavaFormatter
from app.formatters.json_formatter import JSONFormatter
from app.formatters.pnml_formatter import PNMLFormatter


class FormatterFactory:

    def create(self, file_type: str) -> IFormatter:
        match file_type.lower():
            case "pnml":
                return PNMLFormatter()
            case "json":
                return JSONFormatter()
            case "petriobj":
                return JavaFormatter()
            case _:
                raise ValueError(f"Unsupported file type: {file_type}")