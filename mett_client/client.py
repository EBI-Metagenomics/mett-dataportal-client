"""High-level METT Data Portal API client built on top of the generated SDK."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import requests  # type: ignore[import]
from mett_dataportal_sdk import (
    ApiClient as SDKApiClient,
    Configuration as SDKConfiguration,
)
from mett_dataportal_sdk.api.drugs_api import DrugsApi
from mett_dataportal_sdk.api.essentiality_api import EssentialityApi
from mett_dataportal_sdk.api.fitness_api import FitnessApi
from mett_dataportal_sdk.api.genes_api import GenesApi
from mett_dataportal_sdk.api.genomes_api import GenomesApi
from mett_dataportal_sdk.api.mutant_growth_api import MutantGrowthApi
from mett_dataportal_sdk.api.orthologs_api import OrthologsApi
from mett_dataportal_sdk.api.pooled_ttp_interactions_api import PooledTTPInteractionsApi
from mett_dataportal_sdk.api.protein_protein_interactions_api import (
    ProteinProteinInteractionsApi,
)
from mett_dataportal_sdk.api.proteomics_api import ProteomicsApi
from mett_dataportal_sdk.api.reactions_api import ReactionsApi
from mett_dataportal_sdk.api.releases_api import ReleasesApi
from mett_dataportal_sdk.api.species_api import SpeciesApi
from mett_dataportal_sdk.exceptions import ApiException

from .config import Config, get_config
from .exceptions import APIError, AuthenticationError
from .request_utils import parse_tsv_response, request_json
from .models import (
    DrugMIC,
    DrugMetabolism,
    Gene,
    Genome,
    Pagination,
    Species,
)
from .utils import normalize_params, normalize_species_entry

T = TypeVar("T")
ApiType = TypeVar("ApiType")


@dataclass
class PaginatedResult(Generic[T]):
    items: List[T]
    pagination: Pagination | None
    raw: Dict[str, Any]


class DataPortalClient:
    """Thin wrapper that provides ergonomic helpers on top of the generated SDK."""

    def __init__(
        self,
        *,
        config: Config | None = None,
        base_url: str | None = None,
        jwt_token: str | None = None,
        release: str | None = None,
        timeout: int | None = None,
        verify_ssl: bool | None = None,
        user_agent: str | None = None,
        sdk_client: SDKApiClient | None = None,
    ) -> None:
        self.config = config or get_config()
        if base_url:
            self.config.base_url = base_url.rstrip("/")
        if jwt_token:
            self.config.jwt_token = jwt_token
        if release is not None:
            self.config.release = release
        if timeout is not None:
            self.config.timeout = timeout
        if verify_ssl is not None:
            self.config.verify_ssl = verify_ssl
        if user_agent:
            self.config.user_agent = user_agent

        configuration = self._build_sdk_configuration()
        self._sdk_client = sdk_client or SDKApiClient(configuration=configuration)
        # align UA with the rest of the project
        self._sdk_client.user_agent = self.config.user_agent
        if self.config.release:
            self._sdk_client.set_default_header("X-METT-Release", self.config.release)
        self._apis: Dict[Type[Any], Any] = {}
        self._http = self._build_http_session()

    # ------------------------------------------------------------------
    # Core API Methods
    # ------------------------------------------------------------------
    def list_releases(self) -> Dict[str, Any]:
        """List scientist-visible METT data releases (``/api/releases``)."""
        response = self._call_api(
            self._api(ReleasesApi).dataportal_api_core_release_endpoints_list_releases,
        )
        return response.model_dump()

    def list_species(self, *, format: str = "json") -> List[Species]:
        """List all species. Supports format='json' (default) or format='tsv'."""
        payload = request_json(
            self._http, self.config, "/api/species/", params={"format": format}
        )
        if isinstance(payload, dict):
            raw_items = payload.get("data") or []
        elif isinstance(payload, list):
            raw_items = payload
        else:
            raise APIError("Unexpected response for /api/species/")

        return [normalize_species_entry(item) for item in raw_items]

    def list_genomes(
        self, *, format: str = "json", **params: Any
    ) -> PaginatedResult[Genome]:
        """List all genomes. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated(
                "/api/genomes/", params=params, model=Genome
            )
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_core_genome_endpoints_get_all_genomes,
            params=params,
        )
        return self._to_paginated(response)

    def species_genomes(
        self, species_acronym: str, **params: Any
    ) -> PaginatedResult[Genome]:
        response = self._call_api(
            self._api(
                SpeciesApi
            ).dataportal_api_core_species_endpoints_get_genomes_by_species,
            params=params,
            species_acronym=species_acronym,
        )
        return self._to_paginated(response)

    def search_genomes(
        self, *, format: str = "json", **params: Any
    ) -> PaginatedResult[Genome]:
        """Search genomes. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated(
                "/api/genomes/search", params=params, model=Genome
            )
        # Use direct HTTP request to ensure format=json is included in query string
        json_params = (params or {}).copy()
        json_params["format"] = "json"
        payload = request_json(
            self._http, self.config, "/api/genomes/search", params=json_params
        )
        # Parse paginated response
        if isinstance(payload, dict):
            data = payload.get("data", [])
            pagination_dict = payload.get("pagination")
            pagination = Pagination(**pagination_dict) if pagination_dict else None
            raw = payload
        else:
            data = payload if isinstance(payload, list) else []
            pagination = None
            raw = {"data": data}
        items = [Genome(**item) if isinstance(item, dict) else item for item in data]
        return PaginatedResult(items=items, pagination=pagination, raw=raw)

    def get_genome_genes(
        self, isolate_name: str, **params: Any
    ) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(
                GenomesApi
            ).dataportal_api_core_genome_endpoints_get_genes_by_genome,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def search_genes(self, **params: Any) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(
                GenesApi
            ).dataportal_api_core_gene_endpoints_search_genes_by_string,
            params=params,
        )
        return self._to_paginated(response)

    def search_genes_advanced(self, **params: Any) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(
                GenesApi
            ).dataportal_api_core_gene_endpoints_search_genes_by_multiple_genomes_and_species_and_string,
            params=params,
        )
        return self._to_paginated(response)

    def get_gene(self, locus_tag: str) -> Gene:
        response = self._call_api(
            self._api(
                GenesApi
            ).dataportal_api_core_gene_endpoints_get_gene_by_locus_tag,
            locus_tag=locus_tag,
        )
        data = getattr(response, "data", response)
        if isinstance(data, Gene):
            return data
        if isinstance(data, dict):
            return Gene.model_validate(data)
        raise APIError(f"Unexpected gene response for locus tag {locus_tag}")

    def get_gene_release_history(self, locus_tag: str) -> Dict[str, Any]:
        """Releases that contain this locus tag (``/api/genes/{locus_tag}/release-history``)."""
        response = self._call_api(
            self._api(
                GenesApi
            ).dataportal_api_core_gene_endpoints_get_gene_release_history,
            locus_tag=locus_tag,
        )
        return response.model_dump()

    def get_genome_release_history(self, isolate_name: str) -> Dict[str, Any]:
        """Releases that contain this genome (``/api/genomes/{isolate_name}/release-history``)."""
        response = self._call_api(
            self._api(
                GenomesApi
            ).dataportal_api_core_genome_endpoints_get_genome_release_history,
            isolate_name=isolate_name,
        )
        return response.model_dump()

    # ------------------------------------------------------------------
    # Experimental API Methods
    # ------------------------------------------------------------------
    def search_drug_mic(
        self, *, format: str = "json", **params: Any
    ) -> PaginatedResult[DrugMIC]:
        """Search drug MIC data. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated(
                "/api/drugs/mic/search", params=params, model=DrugMIC
            )
        response = self._call_api(
            self._api(
                DrugsApi
            ).dataportal_api_experimental_drug_endpoints_search_drug_mic,
            params=params,
        )
        return self._to_paginated(response)

    def search_drug_metabolism(self, **params: Any) -> PaginatedResult[DrugMetabolism]:
        response = self._call_api(
            self._api(
                DrugsApi
            ).dataportal_api_experimental_drug_endpoints_search_drug_metabolism,
            params=params,
        )
        return self._to_paginated(response)

    def get_strain_drug_mic(
        self, isolate_name: str, **params: Any
    ) -> PaginatedResult[DrugMIC]:
        response = self._call_api(
            self._api(
                GenomesApi
            ).dataportal_api_experimental_drug_endpoints_get_strain_drug_mic,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def get_strain_drug_metabolism(
        self, isolate_name: str, **params: Any
    ) -> PaginatedResult[DrugMetabolism]:
        response = self._call_api(
            self._api(
                GenomesApi
            ).dataportal_api_experimental_drug_endpoints_get_strain_drug_metabolism,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def get_strain_drug_data(self, isolate_name: str) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                GenomesApi
            ).dataportal_api_experimental_drug_endpoints_get_strain_drug_data,
            isolate_name=isolate_name,
        )
        return response.model_dump()

    def search_proteomics(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                ProteomicsApi
            ).dataportal_api_experimental_proteomics_endpoints_search_proteomics,
            params=params,
        )
        return response.model_dump()

    def search_essentiality(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                EssentialityApi
            ).dataportal_api_experimental_essentiality_endpoints_search_essentiality,
            params=params,
        )
        return response.model_dump()

    def search_fitness(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                FitnessApi
            ).dataportal_api_experimental_fitness_endpoints_search_fitness,
            params=params,
        )
        return response.model_dump()

    def search_mutant_growth(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                MutantGrowthApi
            ).dataportal_api_experimental_mutant_growth_endpoints_search_mutant_growth,
            params=params,
        )
        return response.model_dump()

    def search_reactions(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                ReactionsApi
            ).dataportal_api_experimental_reactions_endpoints_search_reactions,
            params=params,
        )
        return response.model_dump()

    # ------------------------------------------------------------------
    # Interactions API Methods
    # ------------------------------------------------------------------
    def search_ttp(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                PooledTTPInteractionsApi
            ).dataportal_api_interactions_ttp_endpoints_search_interactions,
            params=params,
        )
        return response.model_dump()

    def get_ttp_gene_interactions(
        self, locus_tag: str, **params: Any
    ) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                PooledTTPInteractionsApi
            ).dataportal_api_interactions_ttp_endpoints_get_gene_interactions,
            params=params,
            locus_tag=locus_tag,
        )
        return response.model_dump()

    def get_ttp_compound_interactions(
        self, compound: str, **params: Any
    ) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                PooledTTPInteractionsApi
            ).dataportal_api_interactions_ttp_endpoints_get_compound_interactions,
            params=params,
            compound=compound,
        )
        return response.model_dump()

    def search_ppi(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_search_ppi_interactions,
            params=params,
        )
        return response.model_dump()

    def get_ppi_interaction(self, pair_id: str) -> Dict[str, Any]:
        """Get a single PPI interaction by pair ID (``/api/ppi/interactions/{pair_id}``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_ppi_interaction_by_pair_id,
            pair_id=pair_id,
        )
        return response.model_dump()

    def get_ppi_neighbors(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_all_protein_neighbors,
            params=params,
        )
        return response.model_dump()

    def get_ppi_string_network(self, **params: Any) -> Dict[str, Any]:
        """Fetch STRING interaction network (``/api/ppi/string-network``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_external_string_network_endpoints_get_string_network,
            params=params,
        )
        return response.model_dump()

    def get_ppi_data_sources(self) -> Dict[str, Any]:
        """List PPI data sources (``/api/ppi/data-sources``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_ppi_data_sources,
        )
        return response.model_dump()

    def get_ppi_available_score_types(self) -> Dict[str, Any]:
        """List PPI score types (``/api/ppi/scores/available``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_available_score_types,
        )
        return response.model_dump()

    def get_ppi_network(self, score_type: str, **params: Any) -> Dict[str, Any]:
        """PPI network for a score type (``/api/ppi/network/{score_type}``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_ppi_network,
            params=params,
            score_type=score_type,
        )
        return response.model_dump()

    def get_ppi_network_properties(
        self, score_type: str, **params: Any
    ) -> Dict[str, Any]:
        """PPI network summary statistics (``/api/ppi/network-properties``)."""
        response = self._call_api(
            self._api(
                ProteinProteinInteractionsApi
            ).dataportal_api_interactions_ppi_endpoints_get_ppi_network_properties,
            params=params,
            score_type=score_type,
        )
        return response.model_dump()

    def search_orthologs(self, **params: Any) -> PaginatedResult[Any]:
        """Search ortholog pairs with filters and pagination."""
        response = self._call_api(
            self._api(
                OrthologsApi
            ).dataportal_api_interactions_ortholog_endpoints_search_orthologs,
            params=params,
        )
        return self._to_paginated(response)

    def get_ortholog_pair(self, locus_tag_a: str, locus_tag_b: str) -> Dict[str, Any]:
        """Ortholog relationship between two locus tags."""
        response = self._call_api(
            self._api(
                OrthologsApi
            ).dataportal_api_interactions_ortholog_endpoints_get_ortholog_pair,
            locus_tag_a=locus_tag_a,
            locus_tag_b=locus_tag_b,
        )
        return response.model_dump()

    def get_orthologs_batch(self, **params: Any) -> Dict[str, Any]:
        """Batch ortholog lookup for multiple locus tags (``/api/orthologs/batch``)."""
        response = self._call_api(
            self._api(
                OrthologsApi
            ).dataportal_api_interactions_ortholog_endpoints_get_orthologs_batch,
            params=params,
        )
        return response.model_dump()

    # ------------------------------------------------------------------
    # Raw API Access
    # ------------------------------------------------------------------
    def raw_request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Union[Dict[str, Any], Sequence[Tuple[str, Any]]]] = None,
        headers: Optional[Mapping[str, str]] = None,
        data: Optional[Union[str, bytes]] = None,
        json_body: Optional[Any] = None,
        format: Optional[str] = None,
    ) -> requests.Response:
        """Low-level helper for issuing arbitrary API requests.

        Used by the CLI `mett api request` command to provide coverage for endpoints
        that do not have first-class helpers yet.
        """

        if json_body is not None and data is not None:
            raise ValueError("Provide only one of json_body or data")

        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            normalized = path if path.startswith("/") else f"/{path}"
            url = f"{self.config.base_url.rstrip('/')}{normalized}"

        request_headers = dict(headers or {})
        if format == "tsv":
            request_headers.setdefault("Accept", "text/tab-separated-values")
        elif format == "json" or format is None:
            request_headers.setdefault("Accept", "application/json")

        try:
            response = self._http.request(
                method=method.upper(),
                url=url,
                params=params,
                data=None if json_body is not None else data,
                json=json_body,
                headers=request_headers or None,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
        except requests.RequestException as exc:
            raise APIError(str(exc)) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            message = response.text or str(exc)
            status = response.status_code if response is not None else None
            raise APIError(message, status_code=status) from exc

        return response

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _api(self, api_cls: Type[ApiType]) -> ApiType:
        if api_cls not in self._apis:
            self._apis[api_cls] = api_cls(self._sdk_client)
        return self._apis[api_cls]

    def _build_sdk_configuration(self) -> SDKConfiguration:
        configuration = SDKConfiguration(host=self.config.base_url.rstrip("/"))
        configuration.verify_ssl = self.config.verify_ssl
        token = self.config.jwt_token
        if token:
            configuration.access_token = token
        return configuration

    def _build_http_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": self.config.user_agent,
            }
        )
        token = self.config.jwt_token
        if token:
            session.headers["Authorization"] = f"Bearer {token}"
        if self.config.release:
            session.headers["X-METT-Release"] = self.config.release
        return session

    @property
    def _request_timeout(self) -> float:
        return float(self.config.timeout)

    def _call_api(
        self,
        func: Callable[..., T],
        *,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> T:
        normalized_params = normalize_params(params or {})
        normalized_params.update(kwargs)
        normalized_params["_request_timeout"] = self._request_timeout
        return self._call(func, **normalized_params)

    def _call(self, func: Callable[..., T], **kwargs: Any) -> T:
        try:
            return func(**kwargs)
        except ApiException as exc:
            if exc.status in {401, 403}:
                raise AuthenticationError(
                    exc.body or "Authentication failed", status_code=exc.status
                ) from exc
            message = exc.body or exc.reason or "API request failed"
            raise APIError(message, status_code=exc.status) from exc

    def _request_tsv_paginated(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T] | None = None,
    ) -> PaginatedResult[Any]:
        """Make TSV request and parse into paginated result.

        TSV is a flat tabular export: cells are strings (nested objects often
        appear as JSON text). Rows are returned as coerced dicts — not as
        strict SDK pydantic models — because required nested fields like
        ``contigs`` may be omitted or shaped differently than JSON.

        ``model`` is accepted for call-site compatibility but ignored.
        """
        del model  # TSV rows are dicts; see docstring.
        tsv_params = (params or {}).copy()
        tsv_params["format"] = "tsv"

        # Make direct HTTP request for TSV
        url = f"{self.config.base_url.rstrip('/')}{endpoint}"
        headers = {"Accept": "text/tab-separated-values"}
        token = self.config.jwt_token
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            resp = self._http.get(
                url,
                params=tsv_params,
                headers=headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
            resp.raise_for_status()

            items = parse_tsv_response(resp.text)

            # Keep the original TSV body for CLI passthrough (avoids re-encoding
            # nested JSON cells). Parsed dicts remain available as ``items``.
            pagination = None
            raw = {"data": items, "tsv_text": resp.text}

            return PaginatedResult(items=items, pagination=pagination, raw=raw)
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in {401, 403}:
                raise AuthenticationError(
                    "Authentication failed", status_code=exc.response.status_code
                ) from exc
            status = exc.response.status_code if exc.response is not None else None
            raise APIError(f"Request failed: {exc}", status_code=status) from exc
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Request failed: {exc}") from exc
        except (ValueError, csv.Error) as exc:
            raise APIError(f"Failed to parse TSV response: {exc}") from exc

    @staticmethod
    def _to_paginated(schema: Any) -> PaginatedResult[Any]:
        data = list(schema.data or [])
        pagination = schema.pagination if hasattr(schema, "pagination") else None
        raw = schema.model_dump()
        return PaginatedResult(items=data, pagination=pagination, raw=raw)


__all__ = ["DataPortalClient", "PaginatedResult"]
