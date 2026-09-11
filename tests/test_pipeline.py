from pathlib import Path
import unittest

from src.salud_rag.guardrails import classify_query, sanitize_text
from src.salud_rag.pipeline import RagPipeline


ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def test_retrieves_pharmacy_information(self) -> None:
        pipeline = RagPipeline(ROOT / "data" / "source_documents")
        result = pipeline.ask("¿Cómo se informa el retiro de medicamentos crónicos?")
        self.assertEqual(result.route, "administrativa")
        self.assertTrue(any("FARMACIA" in source for source in result.sources))

    def test_emergency_is_blocked_before_retrieval(self) -> None:
        decision = classify_query("Tengo dolor de pecho y falta de aire")
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.route, "emergencia")

    def test_personal_data_is_redacted(self) -> None:
        text = sanitize_text("Mi rut es 12.345.678-9 y mi correo es persona@example.com")
        self.assertIn("[RUT]", text)
        self.assertIn("[EMAIL]", text)


if __name__ == "__main__":
    unittest.main()

