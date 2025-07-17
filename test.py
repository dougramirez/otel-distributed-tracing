import os
import unittest

README_PATH = os.path.join(os.path.dirname(__file__), "README.md")


class TestReadmeContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(README_PATH, "r", encoding="utf-8") as f:
            cls.content = f.read()

    def test_setup_commands_present(self):
        required_commands = [
            "python3 -m venv .venv",
            "source .venv/bin/activate",
            "pip install --upgrade pip",
            "pip3 install black",
            "pip3 install isort",
            "pip3 install fastapi",
            "pip3 install uvicorn",
            "pip3 install opentelemetry-sdk",
            "pip3 install opentelemetry-exporter-otlp-proto-grpc",
            "pip3 install httpx",
        ]
        for cmd in required_commands:
            self.assertIn(cmd, self.content, f"Missing setup command: {cmd}")

    def test_traceparent_header_format(self):
        pattern = r"traceparent: [0-9a-f]{2}-[0-9a-f]{32}-[0-9a-f]{16}-[0-9a-f]{2}"
        self.assertRegex(
            self.content, pattern, "traceparent header format is incorrect"
        )

    def test_tracestate_header_example(self):
        self.assertIn("tracestate: foo=bar", self.content)

    def test_uvicorn_commands(self):
        self.assertIn("uvicorn bands.main:app --reload --port 8000", self.content)
        self.assertIn("uvicorn reviews.main:app --reload --port 8080", self.content)

    def test_client_run_example(self):
        self.assertIn("python3 run.py", self.content)
        self.assertIn('"name": "Fugazi"', self.content)

    def test_signoz_links(self):
        self.assertIn("https://signoz.io/docs/install/docker/", self.content)
        self.assertIn("http://localhost:3301/trace/", self.content)

    def test_resource_links(self):
        resources = [
            "https://opentelemetry.io",
            "https://www.w3.org/TR/trace-context",
            "https://signoz.io",
        ]
        for url in resources:
            self.assertIn(url, self.content)

    def test_privacy_link(self):
        self.assertIn(
            "https://www.w3.org/TR/trace-context/#privacy-considerations", self.content
        )


if __name__ == "__main__":
    unittest.main()
