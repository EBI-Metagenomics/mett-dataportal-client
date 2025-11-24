"""High-level METT Data Portal API client built on top of the generated SDK."""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

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
from mett_dataportal_sdk.api.pooled_ttp_interactions_api import PooledTTPInteractionsApi
from mett_dataportal_sdk.api.protein_protein_interactions_api import ProteinProteinInteractionsApi
from mett_dataportal_sdk.api.proteomics_api import ProteomicsApi
from mett_dataportal_sdk.api.reactions_api import ReactionsApi
from mett_dataportal_sdk.api.species_api import SpeciesApi
from mett_dataportal_sdk.exceptions import ApiException

from .config import Config, get_config
from .exceptions import APIError, AuthenticationError
from .models import (
    DrugMIC,
    DrugMetabolism,
    Gene,
    Genome,
    Pagination,
    Species,
)

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
        api_key: str | None = None,
        jwt_token: str | None = None,
        timeout: int | None = None,
        verify_ssl: bool | None = None,
        user_agent: str | None = None,
        sdk_client: SDKApiClient | None = None,
    ) -> None:
        self.config = config or get_config()
        if base_url:
            self.config.base_url = base_url.rstrip("/")
        if api_key:
            self.config.api_key = api_key
        if jwt_token:
            self.config.jwt_token = jwt_token
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
        self._apis: Dict[Type[Any], Any] = {}
        self._http = self._build_http_session()

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------
    def list_species(self, *, format: str = "json") -> List[Species]:
        """List all species. Supports format='json' (default) or format='tsv'."""
        payload = self._request_json("/api/species/", params={"format": format})
        if isinstance(payload, dict):
            raw_items = payload.get("data") or []
        elif isinstance(payload, list):
            raw_items = payload
        else:
            raise APIError("Unexpected response for /api/species/")

        return [self._normalize_species_entry(item) for item in raw_items]

    def list_genomes(self, *, format: str = "json", **params: Any) -> PaginatedResult[Genome]:
        """List all genomes. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated("/api/genomes/", params=params, model=Genome)
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_core_genome_endpoints_get_all_genomes,
            params=params,
        )
        return self._to_paginated(response)

    def species_genomes(self, species_acronym: str, **params: Any) -> PaginatedResult[Genome]:
        response = self._call_api(
            self._api(SpeciesApi).dataportal_api_core_species_endpoints_get_genomes_by_species,
            params=params,
            species_acronym=species_acronym,
        )
        return self._to_paginated(response)

    def search_genomes(self, *, format: str = "json", **params: Any) -> PaginatedResult[Genome]:
        """Search genomes. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated("/api/genomes/search", params=params, model=Genome)
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_core_genome_endpoints_search_genomes_by_string,
            params=params,
        )
        return self._to_paginated(response)

    def get_genome_genes(self, isolate_name: str, **params: Any) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_core_genome_endpoints_get_genes_by_genome,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def search_genes(self, **params: Any) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(GenesApi).dataportal_api_core_gene_endpoints_search_genes_by_string,
            params=params,
        )
        return self._to_paginated(response)

    def search_genes_advanced(self, **params: Any) -> PaginatedResult[Gene]:
        response = self._call_api(
            self._api(GenesApi).dataportal_api_core_gene_endpoints_search_genes_by_multiple_genomes_and_species_and_string,
            params=params,
        )
        return self._to_paginated(response)

    def get_gene(self, locus_tag: str) -> Gene:
        response = self._call_api(
            self._api(GenesApi).dataportal_api_core_gene_endpoints_get_gene_by_locus_tag,
            locus_tag=locus_tag,
        )
        return response

    # --------------------------- Experimental ---------------------------
    def search_drug_mic(self, *, format: str = "json", **params: Any) -> PaginatedResult[DrugMIC]:
        """Search drug MIC data. Supports format='json' (default) or format='tsv'."""
        if format == "tsv":
            return self._request_tsv_paginated("/api/drugs/mic/search", params=params, model=DrugMIC)
        response = self._call_api(
            self._api(DrugsApi).dataportal_api_experimental_drug_endpoints_search_drug_mic,
            params=params,
        )
        return self._to_paginated(response)

    def search_drug_metabolism(self, **params: Any) -> PaginatedResult[DrugMetabolism]:
        response = self._call_api(
            self._api(DrugsApi).dataportal_api_experimental_drug_endpoints_search_drug_metabolism,
            params=params,
        )
        return self._to_paginated(response)

    def get_strain_drug_mic(self, isolate_name: str, **params: Any) -> PaginatedResult[DrugMIC]:
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_experimental_drug_endpoints_get_strain_drug_mic,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def get_strain_drug_metabolism(
        self, isolate_name: str, **params: Any
    ) -> PaginatedResult[DrugMetabolism]:
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_experimental_drug_endpoints_get_strain_drug_metabolism,
            params=params,
            isolate_name=isolate_name,
        )
        return self._to_paginated(response)

    def get_strain_drug_data(self, isolate_name: str) -> Dict[str, Any]:
        response = self._call_api(
            self._api(GenomesApi).dataportal_api_experimental_drug_endpoints_get_strain_drug_data,
            isolate_name=isolate_name,
        )
        return response.model_dump()

    def search_proteomics(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(ProteomicsApi).dataportal_api_experimental_proteomics_endpoints_search_proteomics,
            params=params,
        )
        return response.model_dump()

    def search_essentiality(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(EssentialityApi).dataportal_api_experimental_essentiality_endpoints_search_essentiality,
            params=params,
        )
        return response.model_dump()

    def search_fitness(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(FitnessApi).dataportal_api_experimental_fitness_endpoints_search_fitness,
            params=params,
        )
        return response.model_dump()

    def search_mutant_growth(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(MutantGrowthApi).dataportal_api_experimental_mutant_growth_endpoints_search_mutant_growth,
            params=params,
        )
        return response.model_dump()

    def search_reactions(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(ReactionsApi).dataportal_api_experimental_reactions_endpoints_search_reactions,
            params=params,
        )
        return response.model_dump()

    def search_ttp(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(PooledTTPInteractionsApi).dataportal_api_interactions_ttp_endpoints_search_interactions,
            params=params,
        )
        return response.model_dump()

    def get_ttp_gene_interactions(self, locus_tag: str, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(PooledTTPInteractionsApi).dataportal_api_interactions_ttp_endpoints_get_gene_interactions,
            params=params,
            locus_tag=locus_tag,
        )
        return response.model_dump()

    def get_ttp_compound_interactions(self, compound: str, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(PooledTTPInteractionsApi).dataportal_api_interactions_ttp_endpoints_get_compound_interactions,
            params=params,
            compound=compound,
        )
        return response.model_dump()

    def search_ppi(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(ProteinProteinInteractionsApi).dataportal_api_interactions_ppi_endpoints_search_ppi_interactions,
            params=params,
        )
        return response.model_dump()

    def get_ppi_neighbors(self, **params: Any) -> Dict[str, Any]:
        response = self._call_api(
            self._api(ProteinProteinInteractionsApi).dataportal_api_interactions_ppi_endpoints_get_all_protein_neighbors,
            params=params,
        )
        return response.model_dump()

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
        token = self.config.jwt_token or self.config.api_key
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
        token = self.config.jwt_token or self.config.api_key
        if token:
            session.headers["Authorization"] = f"Bearer {token}"
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
        normalized_params = self._normalize_params(params or {})
        normalized_params.update(kwargs)
        normalized_params["_request_timeout"] = self._request_timeout
        return self._call(func, **normalized_params)

    def _call(self, func: Callable[..., T], **kwargs: Any) -> T:
        try:
            return func(**kwargs)
        except ApiException as exc:
            if exc.status in {401, 403}:
                raise AuthenticationError(exc.body or "Authentication failed", status_code=exc.status) from exc
            message = exc.body or exc.reason or "API request failed"
            raise APIError(message, status_code=exc.status) from exc

    def _request_json(self, endpoint: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        """Direct HTTP GET for endpoints that don't match the published schema.
        
        Supports both JSON (default) and TSV (format=tsv) responses.
        """
        url = f"{self.config.base_url.rstrip('/')}{endpoint}"
        format_type = (params or {}).get("format", "json")
        
        # Prepare headers based on format
        headers = {}
        if format_type == "tsv":
            headers["Accept"] = "text/tab-separated-values"
        else:
            headers["Accept"] = "application/json"
        
        try:
            resp = self._http.get(
                url,
                params=params,
                headers=headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
            resp.raise_for_status()
            
            # Parse TSV if requested
            if format_type == "tsv":
                return self._parse_tsv_response(resp.text)
            
            # Default: parse JSON
            return resp.json()
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in {401, 403}:
                raise AuthenticationError("Authentication failed", status_code=exc.response.status_code) from exc
            status = exc.response.status_code if exc.response is not None else None
            raise APIError(f"Request failed: {exc}", status_code=status) from exc
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Request failed: {exc}") from exc
        except (ValueError, csv.Error) as exc:
            raise APIError(f"Failed to parse TSV response: {exc}") from exc

    @staticmethod
    def _parse_tsv_response(tsv_text: str) -> List[Dict[str, Any]]:
        """Parse TSV response into a list of dictionaries.
        
        Assumes first row contains headers. Returns list of dicts where keys are header names.
        """
        if not tsv_text.strip():
            return []
        
        reader = csv.DictReader(io.StringIO(tsv_text), delimiter="\t")
        return [dict(row) for row in reader]
    
    def _request_tsv_paginated(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        model: Type[T] | None = None,
    ) -> PaginatedResult[T]:
        """Make TSV request and parse into paginated result.
        
        Note: TSV responses may not include pagination metadata.
        If pagination info is missing, pagination will be None.
        """
        tsv_params = (params or {}).copy()
        tsv_params["format"] = "tsv"
        
        # Make direct HTTP request for TSV
        url = f"{self.config.base_url.rstrip('/')}{endpoint}"
        headers = {"Accept": "text/tab-separated-values"}
        token = self.config.jwt_token or self.config.api_key
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
            
            # Parse TSV
            rows = self._parse_tsv_response(resp.text)
            
            # Convert to model instances if model provided
            items: List[T]
            if model is None:
                items = rows  # type: ignore[assignment]
            else:
                items = [model(**row) for row in rows]
            
            # TSV responses typically don't include pagination metadata
            # Check response headers or assume no pagination info
            pagination = None
            raw = {"data": [dict(item) if hasattr(item, "model_dump") else item for item in items]}
            
            return PaginatedResult(items=items, pagination=pagination, raw=raw)
        except requests.exceptions.HTTPError as exc:
            if exc.response is not None and exc.response.status_code in {401, 403}:
                raise AuthenticationError("Authentication failed", status_code=exc.response.status_code) from exc
            status = exc.response.status_code if exc.response is not None else None
            raise APIError(f"Request failed: {exc}", status_code=status) from exc
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Request failed: {exc}") from exc
        except (ValueError, csv.Error) as exc:
            raise APIError(f"Failed to parse TSV response: {exc}") from exc
    
    @staticmethod
    def _normalize_params(params: Dict[str, Any]) -> Dict[str, Any]:
        normalized: Dict[str, Any] = {}
        for key, value in params.items():
            if value is None:
                continue
            if key.startswith("_"):
                normalized[key] = value
                continue
            if any(ch.isupper() for ch in key):
                snake = re.sub(r"(?<!^)(?=[A-Z])", "_", key).lower()
                normalized[snake] = value
            else:
                normalized[key] = value
        return normalized

    @staticmethod
    def _normalize_species_entry(entry: Any) -> Species:
        if hasattr(entry, "model_dump"):
            entry = entry.model_dump()
        if not isinstance(entry, dict):
            return {
                "species_scientific_name": str(entry),
                "species_acronym": None,
                "genome_count": None,
                "type_strain_count": None,
                "description": None,
                "taxonomy_id": None,
            }

        def _first(*keys: str) -> Optional[Any]:
            for key in keys:
                if key in entry and entry[key] not in (None, ""):
                    return entry[key]
            return None

        return {
            "species_acronym": _first("species_acronym", "acronym", "short_name"),
            "species_scientific_name": _first("species_scientific_name", "scientific_name", "name"),
            "genome_count": _first("genome_count", "genomes", "num_genomes"),
            "type_strain_count": _first("type_strain_count", "type_strains"),
            "description": _first("description", "common_name"),
            "taxonomy_id": _first("taxonomy_id", "tax_id"),
        }

    @staticmethod
    def _to_paginated(schema: Any) -> PaginatedResult[Any]:
        data = list(schema.data or [])
        pagination = schema.pagination if hasattr(schema, "pagination") else None
        raw = schema.model_dump()
        return PaginatedResult(items=data, pagination=pagination, raw=raw)


__all__ = ["DataPortalClient", "PaginatedResult"]
