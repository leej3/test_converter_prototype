# /usr/bin/env python3
from pathlib import Path
import tempfile
import os
import yaml
from jsonschema import validate


class ExecutionObject:
    def __init__(self, input_file):
        self._is_valid = False
        input_file = Path(input_file)
        self.input_file = input_file
        self.tests = self.ingest_tests(input_file)

    def ingest_tests(self, input_file):
        if not self.test:
            if input_file.suffix == ".yaml":
                self.test = self.from_yaml(self.input_file)
            else:
                raise ValueError("File suffix must be yaml")

    def from_yaml(self, input_file):
        input_file = Path(input_file)

        test_obj = yaml.load(input_file.read_text())

        self.is_valid(test_obj)

    def to_yaml(self, fname):
        fname = Path(fname)
        fname.write_text(yaml.dump(self.test))

    def is_valid(self, test_dict):
        validate(test_dict, self.schema)
        return True

    @property
    def schema(self):
        self._schema = {
            "$schema": "defined_inplace",
            "type": "object",
            "properties": {
                "env_vars": {"type": "array"},
                "env": {"type": "array"},
                "inputs": {"type": "array"},
                "execute": {"type": "object"},
                "keywords": {"type": "array"},
                "label": {"type": "string"},
            },
            "required": ["inputs", "execute"],
        }
        return self._schema

    def __eq__(self, other):
        return self.test == other.test

    def __repr__(self):
        return f"{self.__class__.__name__}({self.input_file.name}) ({hex(id(self))})"

    def __str__(self):
        return {
            "input_file": self.input_file,
            "is_valid": self.is_valid(self.test),
            "test": self.test,
        }


class AFNITest(ExecutionObject):
    def __init__(self, input_file):
        super().__init__(input_file)

    def ingest_tests(self, input_file):
        if input_file.suffix == ".tcsh":
            self.test = self.from_tcsh(input_file)
        elif input_file.suffix == ".yaml":
            self.test = self.from_yaml(self.input_file)
        else:
            raise ValueError("File suffix must be tcsh or yaml")

    @property
    def section_mapping(self):
        self._section_mapping = {
            "ENV": "env",
            "LAB": "label",
            "CMD": "script",
            "KW": "keywords",
            "INP": "inputs",
        }
        return self._section_mapping

    def to_tcsh(self, fname):
        raise NotImplementedError
        fname = Path(fname)
        # TODO: format test
        # tcsh = "\n".join([])
        # fname.write_text(repr(self.test))

    def from_tcsh(self, input_file):
        input_file = Path(input_file)
        test_str = input_file.read_text()
        # do much parsing
        output = test_str
        return output


CWD = Path(os.path.abspath(__file__)).parent
TMP = Path(tempfile.gettempdir())


def test_AFNITEST():

    for yaml_file in CWD.glob("*.yaml"):

        yaml_obj = AFNITest(yaml_file)
        tcsh_obj = AFNITest(yaml_file.with_suffix(".tcsh"))
        assert yaml_obj.test == tcsh_obj.test

        tcsh_out = TMP / (yaml_file.stem + ".tcsh")
        yaml_out = TMP / (yaml_file.stem + ".yaml")
        yaml_obj.to_tcsh(tcsh_out)
        tcsh_obj.to_yaml(yaml_out)

        assert yaml_obj == AFNITest(tcsh_out)
        assert tcsh_obj == AFNITest(yaml_out)
