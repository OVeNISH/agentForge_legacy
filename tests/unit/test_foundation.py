import io
import json
import logging
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from modernize.config import Config, load_config
from modernize.llm import LLMClient, MockLLMClient
from modernize.logging import JSONFormatter, configure_logging


class ConfigurationTests(unittest.TestCase):
    def load_document(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(document, encoding="utf-8")
            return load_config(path)

    def test_defaults(self):
        self.assertEqual(load_config(), Config())
        self.assertEqual(load_config().to_dict(), {
            "legacy_image": "modernize-legacy:cp0",
            "modern_image": "modernize-modern:cp0",
            "log_level": "INFO",
        })

    def test_overrides_preserve_other_defaults(self):
        config = self.load_document('{"legacy_image":"local/legacy:v1","log_level":"DEBUG"}')
        self.assertEqual(config.legacy_image, "local/legacy:v1")
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.modern_image, Config().modern_image)

    def test_invalid_documents_are_rejected(self):
        for document in ('{', '[]', 'null', '{"typo":1}',
                         '{"legacy_image":null}', '{"modern_image":12}',
                         '{"legacy_image":""}', '{"modern_image":"bad image"}',
                         '{"log_level":"trace"}', '{"log_level":[]}'):
            with self.subTest(document=document), self.assertRaises((ValueError, TypeError)):
                self.load_document(document)

    def test_missing_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                load_config(Path(directory) / "missing.json")


class MockClientTests(unittest.TestCase):
    def test_interface_returns_deterministic_response(self):
        client: LLMClient = MockLLMClient()
        first = client.complete("propose inputs")
        self.assertEqual(first, client.complete("propose inputs"))
        self.assertEqual(first.text, '{"inputs": []}')
        self.assertEqual(first.model, "deterministic-mock")

    def test_custom_response(self):
        self.assertEqual(MockLLMClient(response="fixture").complete("prompt").text, "fixture")


class LoggingTests(unittest.TestCase):
    def test_formatter_preserves_message_as_json(self):
        record = logging.LogRecord("modernize", logging.WARNING, "", 0,
                                   'message %s', ('"unicode: \u2603"\n',), None)
        record.created = 0
        self.assertEqual(json.loads(JSONFormatter().format(record)), {
            "timestamp": "1970-01-01T00:00:00+00:00",
            "level": "WARNING", "logger": "modernize",
            "message": 'message "unicode: \u2603"\n',
        })

    def test_configuration_filters_level_and_does_not_duplicate_events(self):
        logger = logging.getLogger("modernize")
        previous = (logger.handlers[:], logger.level, logger.propagate)
        stream = io.StringIO()
        try:
            with redirect_stderr(stream):
                configure_logging("INFO")
                configured = configure_logging("WARNING")
                configured.info("hidden")
                configured.warning("visible")
            self.assertEqual(len(stream.getvalue().splitlines()), 1)
            self.assertEqual(json.loads(stream.getvalue())["message"], "visible")
            self.assertFalse(configured.propagate)
        finally:
            logger.handlers, logger.level, logger.propagate = previous
