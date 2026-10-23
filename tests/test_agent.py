from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.salud_agent.agent import MunicipalHealthAgent
from src.salud_agent.guardrails import sanitize_text


ROOT = Path(__file__).resolve().parents[1]


class AgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.agent = MunicipalHealthAgent(
            ROOT / "data" / "source_documents",
            Path(self.temp.name),
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_consultation_uses_sources(self) -> None:
        result = self.agent.ask("¿Cómo retiro medicamentos crónicos?", "t1")
        self.assertEqual(result.action, "responder_con_fuentes")
        self.assertTrue(any("farmacia" in citation.lower() for citation in result.citations))

    def test_emergency_changes_plan_and_escalates(self) -> None:
        result = self.agent.ask("Tengo dolor de pecho y falta de aire", "t2")
        self.assertEqual(result.action, "escalar_urgencia")
        self.assertIn("urgencia", result.answer.lower())
        self.assertTrue(any(step.priority == "critica" for step in result.plan))

    def test_operational_outage_uses_contingency_route(self) -> None:
        result = self.agent.ask("El sistema está caído y no puedo agendar", "t3")
        self.assertEqual(result.route, "contingencia")
        self.assertEqual(result.action, "aplicar_contingencia")

    def test_personal_data_is_removed_before_persistence(self) -> None:
        self.assertNotIn("12.345.678-9", sanitize_text("RUT 12.345.678-9"))

    def test_short_term_memory_preserves_previous_turn(self) -> None:
        self.agent.ask("¿Cómo cambio una hora?", "t4")
        result = self.agent.ask("¿Qué debo registrar después?", "t4")
        self.assertTrue(any("cambio una hora" in item.lower() for item in result.memory_used))

    def test_long_term_memory_recovers_previous_case(self) -> None:
        self.agent.ask("¿Cómo retiro medicamentos crónicos?", "t5")
        result = self.agent.ask("Necesito recordar el retiro de medicamentos", "t6")
        self.assertTrue(any("medicamentos" in item.lower() for item in result.memory_used))


if __name__ == "__main__":
    unittest.main()

