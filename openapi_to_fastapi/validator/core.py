import abc
import json
from pathlib import Path
from typing import Any, Optional, Union


class OpenApiValidationError(Exception):
    pass


class InvalidJSON(OpenApiValidationError):
    pass


class UnsupportedVersion(OpenApiValidationError):
    pass


class MissingParameter(OpenApiValidationError):
    pass


class BaseValidator:
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

    def validate(self):
        try:
            spec = json.loads(self.path.read_text())
        except json.JSONDecodeError:
            raise InvalidJSON(f"Incorrect JSON: {self.path}")
        self.validate_spec(spec)

    @abc.abstractmethod
    def validate_spec(self, spec: dict):
        raise NotImplementedError

    def collect_artifacts(self):
        """
        Runs by CLI tool after validation is completed
        :return: Object need in post validation step
        """
        pass

    @classmethod
    def run_post_validation(cls, artifacts) -> Optional[Any]:
        """
        Runs by CLI tool after entire test session is completed
        :param artifacts: List of elements returned by `collect_artifacts` method
        :return: Error message to be logged if post validation fails
        """
        return None


class DefaultValidator(BaseValidator):
    def validate_spec(self, spec: dict):
        if not spec.get("openapi", "").startswith("3"):
            raise UnsupportedVersion
