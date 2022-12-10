import logging
import requests

from django.core.management import BaseCommand
from requests.adapters import HTTPAdapter, Retry

from head.candidates.constants import BRAZILIAN_STATES
from head.candidates.models import Candidate

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "This command get 2014 candidates information using TSE API."

    def handle(self, *args, **options):
        for state in BRAZILIAN_STATES:
            logger.info(f"Fetching candidates information for {state}")

            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            session.mount("https://", HTTPAdapter(max_retries=retries))

            response = session.get(
                f"https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/listar/2014/{state}/680/6/candidatos"
            )

            data = response.json()
            electoral_unit = data["unidadeEleitoral"]["sigla"]

            for candidate in data["candidatos"]:
                Candidate.objects.get_or_create(
                    tse_id=candidate["id"],
                    defaults={
                        "name": candidate["nomeCompleto"],
                        "number": candidate["numero"],
                        "party": candidate["partido"]["sigla"],
                        "electoral_unit": electoral_unit,
                    },
                )
