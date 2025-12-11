# Command-line Examples

All examples assume the following environment variables:

- `METT_BASE_URL` (defaults to `https://www.gut-microbes.org` if unset)
- `METT_JWT` for endpoints that require experimental access
- `HMMER_JOB_ID` or other placeholders when noted

## ME TT - API Integration Tests

### Core APIs/Health

#### App-Health-Check

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/health"
```

#### Features-Check

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/features"
```

### Core APIs/Pyhmmer/Downloads

#### Download-Aligned-Fasta

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}/download?format=aligned_fasta" \
    -H 'Content-Type: application/json'
```

#### Download-Fasta

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}/download?format=fasta" \
    -H 'Content-Type: application/json'
```

#### Download-TSV

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}/download?format=tab" \
    -H 'Content-Type: application/json'
```

### Core APIs/Pyhmmer/Meta-data

#### databases-list

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search/databases" \
    -H 'Content-Type: application/json'
```

#### mxchoices-list

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search/mx-choices" \
    -H 'Content-Type: application/json'
```

### Core APIs/Pyhmmer/Search

#### Query-Domain-Results

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}/domains?target=BU_CLA-JM-H26-B_04207" \
    -H 'Content-Type: application/json'
```

#### Query-Search-Results

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}" \
    -H 'Content-Type: application/json'
```

#### debug-aligned-fasta

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/${HMMER_JOB_ID}/debug-pyhmmer-msa" \
    -H 'Content-Type: application/json'
```

#### debug-task

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/debug/task/2a6f5b95-9c43-46a6-ab80-9762b00db8aa" \
    -H 'Content-Type: application/json'
```

#### download-fasta-debug

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/dfef7a0e-38f0-4568-8e10-5f7333ed2c13/debug-fasta" \
    -H 'Content-Type: application/json'
```

#### pyhmmer-search-dna

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search" \
    -H 'Content-Type: application/json' \
    -d '{
    "database": "bu_type_strains",
    "threshold": "evalue",
    "threshold_value": 0.01,
    "input": ">test_dna\nATGAGTGAAATAGATCATGTCGGGCTGTGGAACCGCTGTCTTGAAATCATCAG",
    "popen": 0.02,
    "pextend": 0.4
}'
```

#### pyhmmer-search-long

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search" \
    -H 'Content-Type: application/json' \
    -d '{
    "database": "bu_all",
    "threshold": "evalue",
    "threshold_value": 0.01,
    "input": ">test_long_sequence\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLVYQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKQPGKTLEYNVVVDWKSRKTTVDLESTGRTIIKER",
    "mx": "BLOSUM62",
    "E": 1,
    "domE": 1,
    "incE": 0.01,
    "incdomE": 0.03,
    "T": null,
    "domT": null,
    "incT": null,
    "incdomT": null,
    "popen": 0.02,
    "pextend": 0.4
}'
```

#### pyhmmer-search-req

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search" \
    -H 'Content-Type: application/json' \
    -d '{
    "database": "bu_pv_all",
    "threshold": "evalue",
    "threshold_value": 0.01,
    "input": ">Example protein sequence\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLV",
    "mx": "BLOSUM62",
    "E": 1,
    "domE": 1,
    "incE": 0.01,
    "incdomE": 0.03,
    "T": null,
    "domT": null,
    "incT": null,
    "incdomT": null,
    "popen": 0.02,
    "pextend": 0.4
}'
```

#### pyhmmer-search-req Copy

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search" \
    -H 'Content-Type: application/json' \
    -d '{
    "database": "bu_pv_all",
    "threshold": "evalue",
    "threshold_value": 0.01,
    "input": ">Example protein sequence\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLV",
    "mx": "BLOSUM62",
    "E": 1,
    "domE": 1,
    "incE": 0.01,
    "incdomE": 0.03,
    "T": null,
    "domT": null,
    "incT": null,
    "incdomT": null,
    "popen": 0.02,
    "pextend": 0.4
}'
```

#### pyhmmer-search-varied-seq

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/search" \
    -H 'Content-Type: application/json' \
    -d '{
    "database": "bu_pv_all",
    "threshold": "evalue",
    "threshold_value": 0.01,
    "input": ">Example protein sequence\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLVKQVP",
    "mx": "BLOSUM62",
    "E": 1,
    "domE": 1,
    "incE": 0.01,
    "incdomE": 0.03,
    "T": null,
    "domT": null,
    "incT": null,
    "incdomT": null,
    "popen": 0.02,
    "pextend": 0.4
}'
```

#### test-Query-Domain

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/851eb6cd-0852-4f63-967b-5130fe7129d6/domains?target=BU_CLA-JM-H26-B_04207" \
    -H 'Content-Type: application/json'
```

#### test-Search-Results

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/result/94da93bb-624a-4a3e-a8cb-947ac92390b3" \
    -H 'Content-Type: application/json'
```

#### test-task

```bash
curl -X POST "${METT_BASE_URL:-https://www.gut-microbes.org}/api/pyhmmer/testtask" \
    -H 'Content-Type: application/json' \
    -d '{
  "input": ">query1\nMSEQNNTEMTFQIQRIYTKDISFEAPNAPHVFQKDWRAKQ",
  "database": "bu_all",
  "threshold": "evalue",
  "threshold_value": 1e-5
}
'
```

### Core APIs/genes

#### Gene-All-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/?page=1&per_page=10"
```

#### Gene-Autocomplete-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&query=dnaA"
```

#### Gene-Autocomplete-02

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?isolates=BU_2243B,BU_3537,BU_61&query=dnaA"
```

#### Gene-Autocomplete-03

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&isolates=BU_3537,BU_AN67,BU_C7-17,BU_CCUG49527&query=dnaA"
```

#### Gene-Autocomplete-Alias

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?query=BVU&page=1&per_page=10&isolates=PV_ATCC8482"
```

#### Gene-Autocomplete-Essentiality-TypeStrain

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&isolates=BU_ATCC8492&query=pr&filter=essentiality:essential"
```

#### Gene-Autocomplete-Essentiality-TypeStrain-Ess,Interpro

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&isolates=BU_ATCC8492&query=pr&filter=essentiality:essential_liquid;interpro:IPR035952"
```

#### Gene-Autocomplete-Essentiality-TypeStrain-Ess_Liquid

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&isolates=BU_ATCC8492&query=pr&filter=essentiality:essential_liquid"
```

#### Gene-Autocomplete-Essentiality-TypeStrain-Ess_Liquid,Unclear

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=BU&isolates=BU_ATCC8492&query=pr&filter=essentiality:essential_liquid,unclear"
```

#### Gene-Autocomplete-LocusTag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=PV&query=PV_ATCC8482_03700"
```

#### Gene-Autocomplete-LocusTag-02

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?species_acronym=PV&query=PV_TC-KB-P90_00653"
```

#### Gene-Autocomplete-UniprotId

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/autocomplete?query=A7V2E8"
```

#### Gene-Faceted-Search-Interpro-pfam

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/faceted-search?species_acronym=BU&limit=5&interpro=ipr011611&pfam=pf00294"
```

#### Gene-Faceted-Search-SpeciesFiltered

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/faceted-search?species_acronym=BU&limit=5"
```

#### Gene-Faceted-Search-pfam

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/faceted-search?species_acronym=BU&limit=10&pfam=pf13715"
```

#### Gene-Faceted-Search-test

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/faceted-search"
```

#### Gene-Faceted-Search-test Copy

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/faceted-search"
```

#### Gene-by-LocusTag-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00001"
```

#### GeneSort-by-SEQID-GeneString-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=&per_page=10&sort_field=seq_id&sort_order=asc&isolates=BU_909"
```

#### Genes-Download

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/protein/BU_2243B_00003"
```

#### Genes-by-AMY_INFO_FILTER-QueryString-Advanced-02

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=&page=1&per_page=10&sort_field=locus_tag&sort_order=asc&isolates=BU_ATCC8492&filter=has_amr_info%3Atrue"
```

#### Genes-by-GENOME_EXACT

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=bu_909&page=1&per_page=10&sort_field=locus_tag&sort_order=asc"
```

#### Genes-by-GeneString-filter-positive-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=dna"
```

#### Genes-by-GeneString-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search?query=dnaA"
```

#### Genes-by-GenomeID-Single-postive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_909/genes"
```

#### Genes-by-IsolateName-Multiple-GeneString-positive-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492&query=dnaA"
```

#### Genes-by-IsolateName-Multiple-GeneString-positive-02

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492&query=&filter=pfam:pf13715;essentiality:not_essential"
```

#### Genes-by-LocusTag-EXACT

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?page=1&per_page=10&sort_field=locus_tag&sort_order=asc&locus_tag=BU_H1-6_01257"
```

#### Genes-by-LocusTag-EXACT Copy

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?locus_tag=BU_JCM13286_03494"
```

#### Genes-by-LocusTag-QueryString-Advanced-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=BU_2243B_00003&page=1&per_page=10&sort_field=locus_tag&sort_order=asc"
```

#### Genes-by-LocusTag-QueryString-Advanced-01 Copy

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?query=BU_ATCC8492_00001&page=1&per_page=10&sort_field=locus_tag&sort_order=asc"
```

#### Genes-by-ProteinSequence-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/protein/BU_2243B_00003"
```

#### Genes-by-Species-GeneString-positive-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?species_acronym=BU&query=dna"
```

#### Genes-by-Species-IsolateName-Multiple-GeneString-positive-01

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?species_acronym=bu&isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492&query=dnaA"
```

#### Genes-by-Species-TypeStrain-GeneString-Essentiality-Positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/search/advanced?species_acronym=bu&isolates=BU_ATCC8492&query=dna&filter=essentiality:essential"
```

### Core APIs/genomes

#### Autocomplete-genomes

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/autocomplete?query=bu&limit=5" \
    -H 'accept: application/json'
```

#### Autocomplete-with-Filter-species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/autocomplete?query=bu&species_acronym=bu&limit=5"
```

#### Essentiality-By-TypeStrain_BU-Positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_ATCC8492/essentiality/contig_1"
```

#### Essentiality-By-TypeStrain_PV-Positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/PV_ATCC8482/essentiality/contig_1"
```

#### Genome-Download

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/download/tsv"
```

#### Genome-by-genome-Name-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/by-isolate-names?isolates=BU_909"
```

#### Genome-multple-by-isolate-names-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/by-isolate-names?isolates=BU_ATCC8492,PV_ATCC8482"
```

#### Genome-multple-by-isolate-names-single-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/by-isolate-names?isolates=BU_ATCC8492"
```

#### Genomes-All-TypeStrains

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/type-strains"
```

#### Genomes-All-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/?page=1&per_page=5"
```

#### Genomes-by-GenomeString-all-blank

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/search?query=&sortField=species&sortOrder=asc"
```

#### Genomes-by-GenomeString-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/search?query=PV_H4"
```

#### Genomes-by-SpeciesAcronym-GenomeString-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/species/pv/genomes/search?query=pv&page=3"
```

#### Genomes-by-SpeciesAcronym-positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/species/bu/genomes"
```

#### Genomes-by-iso-species-query

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/search?query=90&isolates=BU_909&species_acronym=BU"
```

### Core APIs/metadata

#### COGCategories

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/metadata/cog-categories"
```

### Core APIs/species

#### Species-List-Positive

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/species/"
```

### Experimental APIs/Drug/Drug-Data

#### Drug-Data-BU-By-IsolateName

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_ATCC8492/drug-data"
```

#### Drug-Data-PV-By-IsolateName

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/PV_ATCC8482/drug-data"
```

### Experimental APIs/Drug/MIC

#### Drug-MIC-All

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search"
```

#### Drug-MIC-By-Filters-Higher-MIC_Values

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?species_acronym=BU&min_mic_value=150.0&max_mic_value=160.0"
```

#### Drug-MIC-By-Filters-MIC_Values

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?species_acronym=BU&min_mic_value=35.0&max_mic_value=45.0"
```

#### Drug-MIC-By-Query

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?query=azithromycin"
```

#### Drug-MIC-Paginated

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?page=1&per_page=10&sort_by=mic_value&sort_order=asc"
```

#### Drug-high-MIC-values

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?min_mic_value=10.0"
```

#### Drug-low-MIC-values

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?max_mic_value=1.0"
```

### Experimental APIs/Drug/MIC/by-class

#### Drug-MIC-By-Drug-Class

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-class/beta_lactam"
```

#### Drug-MIC-By-Drug-Class-Filterby-Species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-class/beta_lactam?species_acronym=BU"
```

#### Drug-MIC-By-Drug-Class-Paginated

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-class/beta_lactam?page=1&per_page=5"
```

#### Drug-MIC-Filter-Drug-Class&Species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?drug_class=beta_lactam&species_acronym=BU"
```

### Experimental APIs/Drug/MIC/by-drug

#### Drug-MIC-By-Drug-Name

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-drug/azithromycin"
```

#### Drug-MIC-By-Drug-Name&Species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-drug/azithromycin?species_acronym=BU"
```

#### Drug-MIC-By-Drug-Name-Fuzzy

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/by-drug/actinomycin"
```

#### Drug-MIC-By-Drug-Name-Paginated

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?drug_name=amoxicillin&species_acronym=BU&page=1&per_page=10"
```

#### Drug-MIC-By-Filters-Higher-MIC_Value

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?drug_name=amoxicillin&species_acronym=BU&min_mic_value=150.0&max_mic_value=160.0"
```

#### Drug-MIC-By-Filters-MIC_Values

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/mic/search?drug_name=amoxicillin&species_acronym=BU&min_mic_value=35.0&max_mic_value=45.0"
```

### Experimental APIs/Drug/MIC/by-isolate

#### Drug-MIC-BU-for-Isolate-token-missing

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_ATCC8492/drug-mic"
```

#### Drug-MIC-BU-for-Isolate-token-valid

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_ATCC8492/drug-mic"
```

#### Drug-MIC-PV-for-Isolate

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/PV_ATCC8482/drug-mic"
```

### Experimental APIs/Drug/Metabolism

#### Drug-Metabolism-All

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/search"
```

#### Drug-Metabolism-By-SignificantEvents

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/search?is_significant=true&min_degr_percent=75.0"
```

#### Drug-Metabolism-Search-Name

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/search?query=amoxapine"
```

#### Drug-Metabolism-Search-degradation-threshold

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/search?min_degr_percent=50.0&species_acronym=BU"
```

### Experimental APIs/Drug/Metabolism/by-class

#### Drug-Metabolism-Search-by-class

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/search?drug_class=beta_lactam"
```

#### Drug-Metabolism-by-drugClass

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-class/beta_lactam"
```

#### Drug-Metabolism-by-drugClass&Species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-class/beta_lactam?species_acronym=BU"
```

#### Drug-Metabolism-by-drugClass-Paginated

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-class/beta_lactam?page=1&per_page=5"
```

### Experimental APIs/Drug/Metabolism/by-drug

#### Drug-Metabolism-by-drugName

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-drug/amoxapine"
```

#### Drug-Metabolism-by-drugName&Species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-drug/amoxapine?species_acronym=BU"
```

#### Drug-Metabolism-by-drugName-Fuzzy

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/drugs/metabolism/by-drug/huperzine"
```

### Experimental APIs/Drug/Metabolism/by-isolate

#### Drug-Metabolism-BU-By-IsolateName

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/BU_ATCC8492/drug-metabolism"
```

#### Drug-Metabolism-PV-By-IsolateName

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genomes/PV_ATCC8482/drug-metabolism"
```

### Experimental APIs/Essentiality

#### Essentiality - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00002/essentiality"
```

#### Essentiality - Search

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/essentiality/search?locus_tags=BU_ATCC8492_00002&uniprot_ids=A7V2F0,A6L272"
```

#### Essentiality - Search by Call

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/essentiality/search?essentiality_call=essential"
```

#### Essentiality - Search for specific media

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/essentiality/search?essentiality_call=essential&experimental_condition=mGAM_undefined_rich_media"
```

#### Essentiality - Search with Quality Only

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/essentiality/search?min_tas_in_locus=25&min_tas_hit=0.8"
```

### Experimental APIs/Fitness-Correlation

#### Fitness-Correlation - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_02530/correlations"
```

#### Fitness-Correlation - search

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness-correlations/search?query=Vitamin B12"
```

#### Fitness-Correlation - two locus tags

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness-correlations/correlation?locus_tag_a=BU_ATCC8492_02530&locus_tag_b=BU_ATCC8492_02762"
```

### Experimental APIs/Fitness-Data

#### FitnessData - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00002/fitness"
```

#### FitnessData - by Locus Tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness/search?locus_tags=BU_ATCC8492_00002"
```

#### FitnessData - high-confidence fitness data

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness/search?min_barcodes=25&max_fdr=0.01"
```

#### FitnessData - in caecal media

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness/search?contrast=comm20_day7"
```

#### FitnessData - with significant fitness defects

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/fitness/search?max_fdr=0.05&min_lfc=2.0"
```

### Experimental APIs/Mutant-Growth

#### MutantGrowth - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/PV_ATCC8482_01384/mutant-growth"
```

#### MutantGrowth - Search for high-quality growth data

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/mutant-growth/search?exclude_double_picked=true&media=caecal"
```

#### MutantGrowth - fast-growing mutants

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/mutant-growth/search?max_doubling_time=2.0"
```

### Experimental APIs/Operons

#### Operons- by Operon Id

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/operons/BU_ATCC8492_00003__BU_ATCC8492_00004"
```

#### Operons- get operons for a gene

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00077/operons"
```

#### Operons- statistics for a species

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/operons/statistics?species_acronym=BU"
```

#### Operons- with at least 5 genes and regulatory elements

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/operons/search?min_gene_count=2&has_tss=true&has_terminator=true"
```

### Experimental APIs/Orthologs

#### Orthologs - if two genes are orthologs

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/orthologs/pair?locus_tag_a=BU_ATCC8492_00001&locus_tag_b=PV_ATCC8482_00001"
```

#### Orthologs- all for the gene

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_WH4_00023/orthologs?one_to_one_only=false"
```

#### Orthologs- one-to-one for a gene

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00001/orthologs?one_to_one_only=true"
```

### Experimental APIs/PPI Interactions

#### PPI-Available Score Types

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/scores/available"
```

#### PPI-Interactions -  BU_ATCC8492_01788

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?locus_tag=BU_ATCC8492_01788&species_acronym=BU&per_page=5"
```

#### PPI-Interactions - A6KXK8

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?protein_id=A6KXK8&species_acronym=PV"
```

#### PPI-Interactions - Abundance Score

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/network-properties?score_type=abundance_score&score_threshold=0.95&species_acronym=PV"
```

#### PPI-Interactions - BU_ATCC8492_01788

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?locus_tag=BU_ATCC8492_01788&species_acronym=BU"
```

#### PPI-Interactions - BU_ATCC8492_02176

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?locus_tag=BU_ATCC8492_02176"
```

#### PPI-Interactions - DS score

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=BU&score_type=ds_score&score_threshold=0.8&per_page=10"
```

#### PPI-Interactions - Melt Score

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=PV&score_type=melt_score&score_threshold=0.9"
```

#### PPI-Interactions - Neighborhood - A6KXK8

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/neighborhood?protein_id=A6KXK8&species_acronym=PV&n=5"
```

#### PPI-Interactions - Neighborhood - A6L7C0

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?protein_id=A6L7C0&species_acronym=PV&per_page=10000"
```

#### PPI-Interactions - Neighborhood - BU_ATCC8492_01788

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/neighborhood?locus_tag=BU_ATCC8492_01788&species_acronym=BU&n=3"
```

#### PPI-Interactions - Neighbors - A6KXK8

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/neighbors?protein_id=A6KXK8&n=5&species_acronym=PV"
```

#### PPI-Interactions - Neighbors - BU_ATCC8492_01788

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/neighbors?locus_tag=BU_ATCC8492_01788&species_acronym=BU"
```

#### PPI-Interactions - Network data

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/network/ds_score?score_threshold=0.8&species_acronym=PV&include_properties=true"
```

#### PPI-Interactions - Network properties

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/network-properties?score_type=ds_score&score_threshold=0.8&species_acronym=PV"
```

#### PPI-Interactions - PV Species - Paginated

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=PV&page=1&per_page=10"
```

#### PPI-Interactions - STRING evidence

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=PV&has_string=true&per_page=5"
```

#### PPI-Interactions - String Score

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=PV&score_type=string_score&score_threshold=0.7&per_page=5"
```

#### PPI-Interactions - XL-MS evidence

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?species_acronym=PV&has_xlms=true&per_page=5"
```

#### PPI-Interactions - XLMS Peptides

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/network-properties?score_type=xlms_peptides&score_threshold=1&species_acronym=PV"
```

#### PPI-Interactions with score Filters -  BU_ATCC8492_01788

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ppi/interactions?locus_tag=BU_ATCC8492_01788&species_acronym=BU&score_type=ds_score&score_threshold=0.1&per_page=3"
```

### Experimental APIs/Pooled_TTP

#### TTP - Analyze specific pools

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/pools/analysis?poolA=pool1&poolB=pool8"
```

#### TTP - Analyze specific pools 2

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/pools/analysis?poolA=pool3&poolB=pool10"
```

#### TTP - Compound Interactions

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/compound/myo-inositol/interactions"
```

#### TTP - Metadata

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/metadata"
```

#### TTP - Search based on Compound

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/search?query=myo-inositol"
```

#### TTP - Search based on Strain

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/search?query=BU_ATCC8492"
```

#### TTP - gene interactions

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/gene/PV_ATCC8482_00051/interactions"
```

#### TTP - gene interactions with Hit Call True

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/gene/PV_ATCC8482_00051/interactions?hit_calling=true"
```

#### TTP - significant interactions

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/ttp/hits?max_fdr=0.05&min_ttp_score=1.0"
```

### Experimental APIs/Proteomics

#### Proteomics - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_00002/proteomics"
```

#### Proteomics - Search

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/proteomics/search?locus_tags=BU_ATCC8492_00002&uniprot_ids=A7V2F0,A6L272"
```

#### Proteomics - Search with Quality

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/proteomics/search?locus_tags=BU_ATCC8492_00002&uniprot_ids=A7V2F0,A6L272&min_coverage=50&min_unique_peptides=10&has_evidence=true"
```

#### Proteomics - Search with Quality Only

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/proteomics/search?min_coverage=75&min_unique_peptides=15&has_evidence=true"
```

### Experimental APIs/Reactions

#### Reactions - By Locus tag

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/genes/BU_ATCC8492_02615/reactions"
```

#### Reactions - Search by Locus Tags

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?locus_tags=BU_ATCC8492_02615,BU_ATCC8492_02516"
```

#### Reactions - Search by Specific reaction

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?reaction_id=ASPTA"
```

#### Reactions - Search by UniprotIds

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?uniprot_ids=A7UXT0,A7V3S8"
```

#### Reactions - Search by multiple filters

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?locus_tags=BU_ATCC8492_02615&substrate=akg_c&product=oaa_c"
```

#### Reactions - Search by multiple filters 2

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?substrate=akg_c&product=oaa_c"
```

#### Reactions - Search for consuming specific metabolite

```bash
curl -X GET "${METT_BASE_URL:-https://www.gut-microbes.org}/api/reactions/search?product=glu__L_c"
```
