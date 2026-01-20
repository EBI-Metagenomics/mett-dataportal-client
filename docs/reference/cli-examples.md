# METT CLI Examples

Each entry shows a friendly `mett` command followed by the fully generic `mett api request` equivalent. Environment variables such as `METT_BASE_URL` and `METT_JWT` apply to both forms.

#### ME TT - API Integration Tests/Core APIs/Health/App-Health-Check

Friendly CLI:
```bash
mett system health --format json
```

Generic CLI:
```bash
mett api request GET /api/health \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/Health/Features-Check

Friendly CLI:
```bash
mett system features --format json
```

Generic CLI:
```bash
mett api request GET /api/features \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/species/Species-List-Positive

Friendly CLI:
```bash
mett species list --format json
```

Generic CLI:
```bash
mett api request GET /api/species/ \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Autocomplete-genomes

Friendly CLI:
```bash
mett genomes autocomplete --query cc --limit 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/autocomplete \
  --format json \
  --query query=cc \
  --query limit=5 \
  --header accept:application/json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Autocomplete-with-Filter-species

Friendly CLI:
```bash
mett genomes autocomplete --query cc --species bu --limit 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/autocomplete \
  --format json \
  --query query=cc \
  --query species_acronym=bu \
  --query limit=5
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genome-by-genome-Name-positive

Friendly CLI:
```bash
mett genomes by-isolates --isolate BU_909,BU_61 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/by-isolate-names \
  --format json \
  --query isolates=BU_909,BU_61
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genome-multple-by-isolate-names-positive

Friendly CLI:
```bash
mett genomes by-isolates --isolate BU_ATCC8492 --isolate PV_ATCC8482 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/by-isolate-names \
  --format json \
  --query isolates=BU_ATCC8492,PV_ATCC8482
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genome-multple-by-isolate-names-single-positive

Friendly CLI:
```bash
mett genomes by-isolates --isolate BU_ATCC8492 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/by-isolate-names \
  --format json \
  --query isolates=BU_ATCC8492
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-All-positive

Friendly CLI:
```bash
mett genomes list --page 1 --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/ \
  --format json \
  --query page=1 \
  --query per_page=5
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-All-TypeStrains

Friendly CLI:
```bash
mett genomes type-strains --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/type-strains \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-by-GenomeString-positive

Friendly CLI:
```bash
mett genomes search --query PV_H4 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/search \
  --format json \
  --query query=PV_H4
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-by-iso-species-query

Friendly CLI:
```bash
mett genomes search --query 909 --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/search \
  --format json \
  --query query=909 \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-by-GenomeString-all-blank

Friendly CLI:
```bash
mett genomes search --sort-field species --sort-order asc --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/search \
  --format json \
  --query query= \
  --query sortField=species \
  --query sortOrder=asc
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-by-SpeciesAcronym-positive

Friendly CLI:
```bash
mett species genomes bu --format json
```

Generic CLI:
```bash
mett api request GET /api/species/bu/genomes \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genomes-by-SpeciesAcronym-GenomeString-positive

Friendly CLI:
```bash
mett species genomes bu --query BU_ATCC --page 1 --format json
```

Generic CLI:
```bash
mett api request GET /api/species/bu/genomes/search \
  --format json \
  --query query=BU_ATCC \
  --query page=1
```

#### ME TT - API Integration Tests/Core APIs/genomes/Essentiality-By-TypeStrain_BU-Positive

Friendly CLI:
```bash
mett genomes essentiality BU_ATCC8492 contig_1 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/BU_ATCC8492/essentiality/contig_1 \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Essentiality-By-TypeStrain_PV-Positive

Friendly CLI:
```bash
mett genomes essentiality PV_ATCC8482 contig_1 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/PV_ATCC8482/essentiality/contig_1 \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genomes/Genome-Download

Friendly CLI:
```bash
mett genomes download
```

Generic CLI:
```bash
mett api request GET /api/genomes/download/tsv
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Faceted-Search-pfam

Friendly CLI:
```bash
mett genes faceted-search --species BU --limit 10 --pfam PF07660,PF07715 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/faceted-search \
  --format json \
  --query species_acronym=BU \
  --query limit=10 \
  --query pfam=pf13715
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Faceted-Search-Interpro-pfam

Friendly CLI:
```bash
mett genes faceted-search --species BU --limit 5 --interpro ipr011611 --pfam pf00294 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/faceted-search \
  --format json \
  --query species_acronym=BU \
  --query limit=5 \
  --query interpro=ipr011611 \
  --query pfam=pf00294
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Faceted-Search-SpeciesFiltered

Friendly CLI:
```bash
mett genes faceted-search --species BU --limit 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/faceted-search \
  --format json \
  --query species_acronym=BU \
  --query limit=5
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Faceted-Search-test

Friendly CLI:
```bash
mett genes faceted-search --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/faceted-search \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Faceted-Search-test Copy

Friendly CLI:
```bash
mett genes faceted-search --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/faceted-search \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-01

Friendly CLI:
```bash
mett genes autocomplete --species BU --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-LocusTag

Friendly CLI:
```bash
mett genes autocomplete --species PV --query PV_ATCC8482_03700 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=PV \
  --query query=PV_ATCC8482_03700
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-UniprotId

Friendly CLI:
```bash
mett genes autocomplete --query A7V2E8 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query query=A7V2E8
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-LocusTag-02

Friendly CLI:
```bash
mett genes autocomplete --species PV --query PV_TC-KB-P90_00653 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=PV \
  --query query=PV_TC-KB-P90_00653
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-Alias

Friendly CLI:
```bash
mett genes autocomplete --query BVU --page 1 --per-page 10 --isolate PV_ATCC8482 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query query=BVU \
  --query page=1 \
  --query per_page=10 \
  --query isolates=PV_ATCC8482
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-02

Friendly CLI:
```bash
mett genes autocomplete --isolate BU_2243B --isolate BU_3537 --isolate BU_61 --query dnaA --format json

mett genes autocomplete --isolate BU_2243B,BU_3537,BU_61 --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query isolates=BU_2243B,BU_3537,BU_61 \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-03

Friendly CLI:
```bash
mett genes autocomplete --species BU --isolate BU_3537 --isolate BU_AN67 --isolate BU_C7-17 --isolate BU_CCUG49527 --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query isolates=BU_3537,BU_AN67,BU_C7-17,BU_CCUG49527 \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-Essentiality-TypeStrain

Friendly CLI:
```bash
mett genes autocomplete --species BU --isolate BU_ATCC8492 --query pr --filter essentiality:essential --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query isolates=BU_ATCC8492 \
  --query query=pr \
  --query filter=essentiality:essential
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-Essentiality-TypeStrain-Ess_Liquid

Friendly CLI:
```bash
mett genes autocomplete --species BU --isolate BU_ATCC8492 --query pr --filter essentiality:essential_liquid --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query isolates=BU_ATCC8492 \
  --query query=pr \
  --query filter=essentiality:essential_liquid
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-Essentiality-TypeStrain-Ess_Liquid,Unclear

Friendly CLI:
```bash
mett genes autocomplete --species BU --isolate BU_ATCC8492 --query pr --filter essentiality:essential_liquid,unclear --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query isolates=BU_ATCC8492 \
  --query query=pr \
  --query filter=essentiality:essential_liquid,unclear
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-Autocomplete-Essentiality-TypeStrain-Ess,Interpro

Friendly CLI:
```bash
mett genes autocomplete --species BU --isolate BU_ATCC8492 --query pr --filter essentiality:essential_liquid;interpro:IPR035952 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/autocomplete \
  --format json \
  --query species_acronym=BU \
  --query isolates=BU_ATCC8492 \
  --query query=pr \
  --query filter=essentiality:essential_liquid;interpro:IPR035952
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-by-LocusTag-positive

Friendly CLI:
```bash
mett genes search-advanced --locus-tag BU_ATCC8492_00001 --per-page 1 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00001 \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genes/Gene-All-positive

Friendly CLI:
```bash
mett genes list --page 1 --per-page 10 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/ \
  --format json \
  --query page=1 \
  --query per_page=10
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-GeneString-positive

Friendly CLI:
```bash
mett genes search --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search \
  --format json \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-GenomeID-Single-postive

Friendly CLI:
```bash
mett genomes genes BU_909 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/BU_909/genes \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/genes/GeneSort-by-SEQID-GeneString-positive

Friendly CLI:
```bash
mett genes search-advanced --per-page 10 --sort-field seq_id --sort-order asc --isolate BU_909 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query= \
  --query per_page=10 \
  --query sort_field=seq_id \
  --query sort_order=asc \
  --query isolates=BU_909
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-IsolateName-Multiple-GeneString-positive-01

Friendly CLI:
```bash
mett genes search-advanced --isolate BU_2243B --isolate BU_3537 --isolate BU_61 --isolate BU_909 --isolate BU_ATCC8492 --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492 \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-IsolateName-Multiple-GeneString-positive-02

Friendly CLI:
```bash
mett genes search-advanced --isolate BU_2243B --isolate BU_3537 --isolate BU_61 --isolate BU_909 --isolate BU_ATCC8492 --filter 'pfam:pf13715;essentiality:not_essential' --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492 \
  --query query= \
  --query filter=pfam:pf13715;essentiality:not_essential
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-Species-IsolateName-Multiple-GeneString-positive-01

Friendly CLI:
```bash
mett genes search-advanced --species bu --isolate BU_2243B --isolate BU_3537 --isolate BU_61 --isolate BU_909 --isolate BU_ATCC8492 --query dnaA --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query species_acronym=bu \
  --query isolates=BU_2243B,BU_3537,BU_61,BU_909,BU_ATCC8492 \
  --query query=dnaA
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-LocusTag-QueryString-Advanced-01

Friendly CLI:
```bash
mett genes search-advanced --query BU_2243B_00003 --page 1 --per-page 10 --sort-field locus_tag --sort-order asc --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query=BU_2243B_00003 \
  --query page=1 \
  --query per_page=10 \
  --query sort_field=locus_tag \
  --query sort_order=asc
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-LocusTag-QueryString-Advanced-01 Copy

Friendly CLI:
```bash
mett genes search-advanced --query BU_ATCC8492_00001 --page 1 --per-page 10 --sort-field locus_tag --sort-order asc --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query=BU_ATCC8492_00001 \
  --query page=1 \
  --query per_page=10 \
  --query sort_field=locus_tag \
  --query sort_order=asc
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-LocusTag-EXACT

Friendly CLI:
```bash
mett genes search-advanced --page 1 --per-page 10 --sort-field locus_tag --sort-order asc --locus-tag BU_H1-6_01257 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query page=1 \
  --query per_page=10 \
  --query sort_field=locus_tag \
  --query sort_order=asc \
  --query locus_tag=BU_H1-6_01257
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-LocusTag-EXACT Copy

Friendly CLI:
```bash
mett genes search-advanced --locus-tag BU_JCM13286_03494 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query locus_tag=BU_JCM13286_03494
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-GENOME_EXACT

Friendly CLI:
```bash
mett genes search-advanced --query bu_909 --page 1 --per-page 10 --sort-field locus_tag --sort-order asc --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query=bu_909 \
  --query page=1 \
  --query per_page=10 \
  --query sort_field=locus_tag \
  --query sort_order=asc
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-AMY_INFO_FILTER-QueryString-Advanced-02

Friendly CLI:
```bash
mett genes search-advanced --page 1 --per-page 10 --sort-field locus_tag --sort-order asc --isolate BU_ATCC8492 --filter has_amr_info:true --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query= \
  --query page=1 \
  --query per_page=10 \
  --query sort_field=locus_tag \
  --query sort_order=asc \
  --query isolates=BU_ATCC8492 \
  --query filter=has_amr_info:true
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-Species-TypeStrain-GeneString-Essentiality-Positive

Friendly CLI:
```bash
mett genes search-advanced --species bu --isolate BU_ATCC8492 --query dna --filter essentiality:essential --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query species_acronym=bu \
  --query isolates=BU_ATCC8492 \
  --query query=dna \
  --query filter=essentiality:essential
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-Species-GeneString-positive-01

Friendly CLI:
```bash
mett genes search-advanced --species BU --query dna --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query species_acronym=BU \
  --query query=dna
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-GeneString-filter-positive-01

Friendly CLI:
```bash
mett genes search-advanced --query dna --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/search/advanced \
  --format json \
  --query query=dna
```

#### ME TT - API Integration Tests/Core APIs/genes/Genes-by-ProteinSequence-01

Friendly CLI:
```bash
mett genes protein BU_2243B_00003 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/protein/BU_2243B_00003 \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/metadata/COGCategories

Friendly CLI:
```bash
mett system cog-categories --format json
```

Generic CLI:
```bash
mett api request GET /api/metadata/cog-categories \
  --format json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Meta-data/databases-list

Friendly CLI:
```bash
mett pyhmmer databases --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/search/databases \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/pyhmmer-search-req Copy

Friendly CLI:
```bash
mett pyhmmer search --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json
```


# [Continue from here...]

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/pyhmmer-search-req

Friendly CLI:
```bash
mett pyhmmer search --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json
```


#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/pyhmmer-search-varied-seq

Friendly CLI:
```bash
mett pyhmmer search --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/pyhmmer-search-long

Friendly CLI:
```bash
mett pyhmmer search --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/pyhmmer-search-dna

Friendly CLI:
```bash
mett pyhmmer search --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/Query-Search-Results

Friendly CLI:
```bash
mett pyhmmer result {{hmmer_job_id}} --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}} \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/download-fasta-debug

Friendly CLI:
```bash
mett pyhmmer debug-fasta dfef7a0e-38f0-4568-8e10-5f7333ed2c13 --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/dfef7a0e-38f0-4568-8e10-5f7333ed2c13/debug-fasta \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/debug-aligned-fasta

Friendly CLI:
```bash
mett pyhmmer debug-msa {{hmmer_job_id}} --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}}/debug-pyhmmer-msa \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/Query-Domain-Results

Friendly CLI:
```bash
mett pyhmmer result-domains {{hmmer_job_id}} --target BU_CLA-JM-H26-B_04207 --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}}/domains \
  --format json \
  --query target=BU_CLA-JM-H26-B_04207 \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/test-Query-Domain

Friendly CLI:
```bash
mett pyhmmer result-domains 851eb6cd-0852-4f63-967b-5130fe7129d6 --target BU_CLA-JM-H26-B_04207 --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/851eb6cd-0852-4f63-967b-5130fe7129d6/domains \
  --format json \
  --query target=BU_CLA-JM-H26-B_04207 \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/test-Search-Results

Friendly CLI:
```bash
mett pyhmmer result 94da93bb-624a-4a3e-a8cb-947ac92390b3 --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/94da93bb-624a-4a3e-a8cb-947ac92390b3 \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/test-task

Friendly CLI:
```bash
mett pyhmmer testtask --format json
```

Generic CLI:
```bash
mett api request POST /api/pyhmmer/testtask \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Search/debug-task

Friendly CLI:
```bash
mett pyhmmer debug-task 2a6f5b95-9c43-46a6-ab80-9762b00db8aa --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/debug/task/2a6f5b95-9c43-46a6-ab80-9762b00db8aa \
  --format json \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Downloads/Download-TSV

Friendly CLI:
```bash
mett pyhmmer result-download {{hmmer_job_id}} --format tab --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}}/download \
  --format json \
  --query format=tab \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Downloads/Download-Fasta

Friendly CLI:
```bash
mett pyhmmer result-download {{hmmer_job_id}} --format fasta --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}}/download \
  --format json \
  --query format=fasta \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Core APIs/Pyhmmer/Downloads/Download-Aligned-Fasta

Friendly CLI:
```bash
mett pyhmmer result-download {{hmmer_job_id}} --format aligned_fasta --format json
```

Generic CLI:
```bash
mett api request GET /api/pyhmmer/result/{{hmmer_job_id}}/download \
  --format json \
  --query format=aligned_fasta \
  --header content-type:application/json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Drug-Data/Drug-Data-BU-By-IsolateName

Friendly CLI:
```bash
mett genomes drug-data BU_ATCC8492 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/BU_ATCC8492/drug-data \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-isolate/Drug-MIC-BU-for-Isolate-token-valid

Friendly CLI:
```bash
mett genomes drug-mic BU_ATCC8492 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/BU_ATCC8492/drug-mic \
  --format json
```


#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-drug/Drug-MIC-By-Drug-Name

Friendly CLI:
```bash
mett drugs mic-by-drug azithromycin --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/by-drug/azithromycin \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-drug/Drug-MIC-By-Drug-Name&Species

Friendly CLI:
```bash
mett drugs mic-by-drug azithromycin --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/by-drug/azithromycin \
  --format json \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-drug/Drug-MIC-By-Drug-Name-Paginated

Friendly CLI:
```bash
mett drugs mic --drug-name amoxicillin --species BU --page 1 --per-page 10 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query drug_name=amoxicillin \
  --query species_acronym=BU \
  --query page=1 \
  --query per_page=10
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-drug/Drug-MIC-By-Filters-MIC_Values

Friendly CLI:
```bash
mett drugs mic --drug-name amoxicillin --species BU --min-mic-value 35.0 --max-mic-value 45.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query drug_name=amoxicillin \
  --query species_acronym=BU \
  --query min_mic_value=35.0 \
  --query max_mic_value=45.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-drug/Drug-MIC-By-Filters-Higher-MIC_Value

Friendly CLI:
```bash
mett drugs mic --drug-name amoxicillin --species BU --min-mic-value 150.0 --max-mic-value 160.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query drug_name=amoxicillin \
  --query species_acronym=BU \
  --query min_mic_value=150.0 \
  --query max_mic_value=160.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-class/Drug-MIC-By-Drug-Class

Friendly CLI:
```bash
mett drugs mic-by-class beta_lactam --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/by-class/beta_lactam \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-class/Drug-MIC-By-Drug-Class-Filterby-Species

Friendly CLI:
```bash
mett drugs mic-by-class beta_lactam --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/by-class/beta_lactam \
  --format json \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-class/Drug-MIC-By-Drug-Class-Paginated

Friendly CLI:
```bash
mett drugs mic-by-class beta_lactam --page 1 --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/by-class/beta_lactam \
  --format json \
  --query page=1 \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/by-class/Drug-MIC-Filter-Drug-Class&Species

Friendly CLI:
```bash
mett drugs mic --drug-class beta_lactam --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query drug_class=beta_lactam \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-MIC-All

Friendly CLI:
```bash
mett drugs mic --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-MIC-By-Query

Friendly CLI:
```bash
mett drugs mic --query azithromycin --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query query=azithromycin
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-MIC-By-Filters-MIC_Values

Friendly CLI:
```bash
mett drugs mic --species BU --min-mic-value 35.0 --max-mic-value 45.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query species_acronym=BU \
  --query min_mic_value=35.0 \
  --query max_mic_value=45.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-MIC-By-Filters-Higher-MIC_Values

Friendly CLI:
```bash
mett drugs mic --species BU --min-mic-value 150.0 --max-mic-value 160.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query species_acronym=BU \
  --query min_mic_value=150.0 \
  --query max_mic_value=160.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-MIC-Paginated

Friendly CLI:
```bash
mett drugs mic --page 1 --per-page 10 --sort-by mic_value --sort-order asc --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query page=1 \
  --query per_page=10 \
  --query sort_by=mic_value \
  --query sort_order=asc
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-high-MIC-values

Friendly CLI:
```bash
mett drugs mic --min-mic-value 10.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query min_mic_value=10.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/MIC/Drug-low-MIC-values

Friendly CLI:
```bash
mett drugs mic --max-mic-value 1.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/mic/search \
  --format json \
  --query max_mic_value=1.0
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-isolate/Drug-Metabolism-BU-By-IsolateName

Friendly CLI:
```bash
mett genomes drug-metabolism BU_ATCC8492 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/BU_ATCC8492/drug-metabolism \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-isolate/Drug-Metabolism-PV-By-IsolateName

Friendly CLI:
```bash
mett genomes drug-metabolism PV_ATCC8482 --format json
```

Generic CLI:
```bash
mett api request GET /api/genomes/PV_ATCC8482/drug-metabolism \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-class/Drug-Metabolism-Search-by-class

Friendly CLI:
```bash
mett drugs metabolism-search --drug-class beta_lactam --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/search \
  --format json \
  --query drug_class=beta_lactam
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-class/Drug-Metabolism-by-drugClass

Friendly CLI:
```bash
mett drugs metabolism-by-class beta_lactam --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-class/beta_lactam \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-class/Drug-Metabolism-by-drugClass&Species

Friendly CLI:
```bash
mett drugs metabolism-by-class beta_lactam --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-class/beta_lactam \
  --format json \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-class/Drug-Metabolism-by-drugClass-Paginated

Friendly CLI:
```bash
mett drugs metabolism-by-class beta_lactam --page 1 --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-class/beta_lactam \
  --format json \
  --query page=1 \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-drug/Drug-Metabolism-by-drugName

Friendly CLI:
```bash
mett drugs metabolism-by-drug amoxapine --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-drug/amoxapine \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-drug/Drug-Metabolism-by-drugName-Fuzzy

Friendly CLI:
```bash
mett drugs metabolism-by-drug huperzine --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-drug/huperzine \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/by-drug/Drug-Metabolism-by-drugName&Species

Friendly CLI:
```bash
mett drugs metabolism-by-drug amoxapine --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/by-drug/amoxapine \
  --format json \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/Drug-Metabolism-All

Friendly CLI:
```bash
mett drugs metabolism-search --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/search \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/Drug-Metabolism-Search-Name

Friendly CLI:
```bash
mett drugs metabolism-search --query amoxapine --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/search \
  --format json \
  --query query=amoxapine
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/Drug-Metabolism-Search-degradation-threshold

Friendly CLI:
```bash
mett drugs metabolism-search --min-degr-percent 50.0 --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/search \
  --format json \
  --query min_degr_percent=50.0 \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Drug/Metabolism/Drug-Metabolism-By-SignificantEvents

Friendly CLI:
```bash
mett drugs metabolism-search --is-significant true --min-degr-percent 75.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/drugs/metabolism/search \
  --format json \
  --query is_significant=true \
  --query min_degr_percent=75.0
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Available Score Types

Friendly CLI:
```bash
mett ppi scores-available --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/scores/available \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - PV Species - Paginated

Friendly CLI:
```bash
mett ppi interactions --species PV --page 1 --per-page 10 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=PV \
  --query page=1 \
  --query per_page=10
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions -  BU_ATCC8492_01788

Friendly CLI:
```bash
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query locus_tag=BU_ATCC8492_01788 \
  --query species_acronym=BU \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions with score Filters -  BU_ATCC8492_01788

Friendly CLI:
```bash
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --score-type ds_score --score-threshold 0.1 --per-page 3 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query locus_tag=BU_ATCC8492_01788 \
  --query species_acronym=BU \
  --query score_type=ds_score \
  --query score_threshold=0.1 \
  --query per_page=3
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - A6KXK8

Friendly CLI:
```bash
mett ppi interactions --protein-id A6KXK8 --species PV --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query protein_id=A6KXK8 \
  --query species_acronym=PV
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - BU_ATCC8492_01788

Friendly CLI:
```bash
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query locus_tag=BU_ATCC8492_01788 \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - BU_ATCC8492_02176

Friendly CLI:
```bash
mett ppi interactions --locus-tag BU_ATCC8492_02176 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query locus_tag=BU_ATCC8492_02176
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Neighbors - A6KXK8

Friendly CLI:
```bash
mett ppi neighbors --protein-id A6KXK8 --n 5 --species PV --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/neighbors \
  --format json \
  --query protein_id=A6KXK8 \
  --query n=5 \
  --query species_acronym=PV
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Neighbors - BU_ATCC8492_01788

Friendly CLI:
```bash
mett ppi neighbors --locus-tag BU_ATCC8492_01788 --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/neighbors \
  --format json \
  --query locus_tag=BU_ATCC8492_01788 \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Neighborhood - A6KXK8

Friendly CLI:
```bash
mett ppi neighborhood --protein-id A6KXK8 --species PV --n 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/neighborhood \
  --format json \
  --query protein_id=A6KXK8 \
  --query species_acronym=PV \
  --query n=5
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Neighborhood - BU_ATCC8492_01788

Friendly CLI:
```bash
mett ppi neighborhood --locus-tag BU_ATCC8492_01788 --species BU --n 3 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/neighborhood \
  --format json \
  --query locus_tag=BU_ATCC8492_01788 \
  --query species_acronym=BU \
  --query n=3
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Neighborhood - A6L7C0

Friendly CLI:
```bash
mett ppi interactions --protein-id A6L7C0 --species PV --per-page 10000 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query protein_id=A6L7C0 \
  --query species_acronym=PV \
  --query per_page=10000
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - DS score

Friendly CLI:
```bash
mett ppi interactions --species BU --score-type ds_score --score-threshold 0.8 --per-page 10 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=BU \
  --query score_type=ds_score \
  --query score_threshold=0.8 \
  --query per_page=10
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Melt Score

Friendly CLI:
```bash
mett ppi interactions --species PV --score-type melt_score --score-threshold 0.9 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=PV \
  --query score_type=melt_score \
  --query score_threshold=0.9
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Abundance Score

Friendly CLI:
```bash
mett ppi network-properties --score-type abundance_score --score-threshold 0.95 --species PV --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/network-properties \
  --format json \
  --query score_type=abundance_score \
  --query score_threshold=0.95 \
  --query species_acronym=PV
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - XLMS Peptides

Friendly CLI:
```bash
mett ppi network-properties --score-type xlms_peptides --score-threshold 1 --species PV --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/network-properties \
  --format json \
  --query score_type=xlms_peptides \
  --query score_threshold=1 \
  --query species_acronym=PV
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - String Score

Friendly CLI:
```bash
mett ppi interactions --species PV --score-type string_score --score-threshold 0.7 --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=PV \
  --query score_type=string_score \
  --query score_threshold=0.7 \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - XL-MS evidence

Friendly CLI:
```bash
mett ppi interactions --species PV --has-xlms true --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=PV \
  --query has_xlms=true \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - STRING evidence

Friendly CLI:
```bash
mett ppi interactions --species PV --has-string true --per-page 5 --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/interactions \
  --format json \
  --query species_acronym=PV \
  --query has_string=true \
  --query per_page=5
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Network properties

Friendly CLI:
```bash
mett ppi network-properties --score-type ds_score --score-threshold 0.8 --species PV --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/network-properties \
  --format json \
  --query score_type=ds_score \
  --query score_threshold=0.8 \
  --query species_acronym=PV
```

#### ME TT - API Integration Tests/Experimental APIs/PPI Interactions/PPI-Interactions - Network data

Friendly CLI:
```bash
mett ppi network ds_score --score-threshold 0.8 --species PV --include-properties true --format json
```

Generic CLI:
```bash
mett api request GET /api/ppi/network/ds_score \
  --format json \
  --query score_threshold=0.8 \
  --query species_acronym=PV \
  --query include_properties=true
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Metadata

Friendly CLI:
```bash
mett ttp metadata --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/metadata \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Search based on Strain

Friendly CLI:
```bash
mett ttp search --query BU_ATCC8492 --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/search \
  --format json \
  --query query=BU_ATCC8492
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Search based on Compound

Friendly CLI:
```bash
mett ttp search --query myo-inositol --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/search \
  --format json \
  --query query=myo-inositol
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - gene interactions

Friendly CLI:
```bash
mett ttp gene-interactions PV_ATCC8482_00051 --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/gene/PV_ATCC8482_00051/interactions \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - gene interactions with Hit Call True

Friendly CLI:
```bash
mett ttp gene-interactions PV_ATCC8482_00051 --hit-calling true --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/gene/PV_ATCC8482_00051/interactions \
  --format json \
  --query hit_calling=true
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Compound Interactions

Friendly CLI:
```bash
mett ttp compound-interactions myo-inositol --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/compound/myo-inositol/interactions \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Analyze specific pools

Friendly CLI:
```bash
mett ttp pools-analysis --pool-a pool1 --pool-b pool8 --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/pools/analysis \
  --format json \
  --query poolA=pool1 \
  --query poolB=pool8
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - Analyze specific pools 2

Friendly CLI:
```bash
mett ttp pools-analysis --pool-a pool3 --pool-b pool10 --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/pools/analysis \
  --format json \
  --query poolA=pool3 \
  --query poolB=pool10
```

#### ME TT - API Integration Tests/Experimental APIs/Pooled_TTP/TTP - significant interactions

Friendly CLI:
```bash
mett ttp hits --max-fdr 0.05 --min-ttp-score 1.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/ttp/hits \
  --format json \
  --query max_fdr=0.05 \
  --query min_ttp_score=1.0
```

#### ME TT - API Integration Tests/Experimental APIs/Proteomics/Proteomics - By Locus tag

Friendly CLI:
```bash
mett genes proteomics BU_ATCC8492_00002 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00002/proteomics \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Proteomics/Proteomics - Search

Friendly CLI:
```bash
mett proteomics search --locus-tag BU_ATCC8492_00002 --uniprot A7V2F0 --uniprot A6L272 --format json
```

Generic CLI:
```bash
mett api request GET /api/proteomics/search \
  --format json \
  --query locus_tags=BU_ATCC8492_00002 \
  --query uniprot_ids=A7V2F0,A6L272
```

#### ME TT - API Integration Tests/Experimental APIs/Proteomics/Proteomics - Search with Quality

Friendly CLI:
```bash
mett proteomics search --locus-tag BU_ATCC8492_00002 --uniprot A7V2F0 --uniprot A6L272 --min-coverage 50 --min-unique-peptides 10 --has-evidence true --format json
```

Generic CLI:
```bash
mett api request GET /api/proteomics/search \
  --format json \
  --query locus_tags=BU_ATCC8492_00002 \
  --query uniprot_ids=A7V2F0,A6L272 \
  --query min_coverage=50 \
  --query min_unique_peptides=10 \
  --query has_evidence=true
```

#### ME TT - API Integration Tests/Experimental APIs/Proteomics/Proteomics - Search with Quality Only

Friendly CLI:
```bash
mett proteomics search --min-coverage 75 --min-unique-peptides 15 --has-evidence true --format json
```

Generic CLI:
```bash
mett api request GET /api/proteomics/search \
  --format json \
  --query min_coverage=75 \
  --query min_unique_peptides=15 \
  --query has_evidence=true
```

#### ME TT - API Integration Tests/Experimental APIs/Essentiality/Essentiality - By Locus tag

Friendly CLI:
```bash
mett genes essentiality BU_ATCC8492_00002 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00002/essentiality \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Essentiality/Essentiality - Search by Call

Friendly CLI:
```bash
mett essentiality search --essentiality-call essential --format json
```

Generic CLI:
```bash
mett api request GET /api/essentiality/search \
  --format json \
  --query essentiality_call=essential
```

#### ME TT - API Integration Tests/Experimental APIs/Essentiality/Essentiality - Search

Friendly CLI:
```bash
mett essentiality search --locus-tag BU_ATCC8492_00002 --uniprot A7V2F0 --uniprot A6L272 --format json
```

Generic CLI:
```bash
mett api request GET /api/essentiality/search \
  --format json \
  --query locus_tags=BU_ATCC8492_00002 \
  --query uniprot_ids=A7V2F0,A6L272
```

#### ME TT - API Integration Tests/Experimental APIs/Essentiality/Essentiality - Search for specific media

Friendly CLI:
```bash
mett essentiality search --essentiality-call essential --condition mGAM_undefined_rich_media --format json
```

Generic CLI:
```bash
mett api request GET /api/essentiality/search \
  --format json \
  --query essentiality_call=essential \
  --query experimental_condition=mGAM_undefined_rich_media
```

#### ME TT - API Integration Tests/Experimental APIs/Essentiality/Essentiality - Search with Quality Only

Friendly CLI:
```bash
mett essentiality search --min-tas-in-locus 25 --min-tas-hit 0.8 --format json
```

Generic CLI:
```bash
mett api request GET /api/essentiality/search \
  --format json \
  --query min_tas_in_locus=25 \
  --query min_tas_hit=0.8
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Data/FitnessData - By Locus tag

Friendly CLI:
```bash
mett genes fitness BU_ATCC8492_00002 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00002/fitness \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Data/FitnessData - in caecal media

Friendly CLI:
```bash
mett fitness search --contrast comm20_day7 --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness/search \
  --format json \
  --query contrast=comm20_day7
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Data/FitnessData - with significant fitness defects

Friendly CLI:
```bash
mett fitness search --max-fdr 0.05 --min-lfc 2.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness/search \
  --format json \
  --query max_fdr=0.05 \
  --query min_lfc=2.0
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Data/FitnessData - by Locus Tag

Friendly CLI:
```bash
mett fitness search --locus-tag BU_ATCC8492_00002 --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness/search \
  --format json \
  --query locus_tags=BU_ATCC8492_00002
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Data/FitnessData - high-confidence fitness data

Friendly CLI:
```bash
mett fitness search --min-barcodes 25 --max-fdr 0.01 --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness/search \
  --format json \
  --query min_barcodes=25 \
  --query max_fdr=0.01
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - By Locus tag

Friendly CLI:
```bash
mett genes reactions BU_ATCC8492_02615 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_02615/reactions \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search by Specific reaction

Friendly CLI:
```bash
mett reactions search --reaction-id ASPTA --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query reaction_id=ASPTA
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search for consuming specific metabolite

Friendly CLI:
```bash
mett reactions search --product glu__L_c --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query product=glu__L_c
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search by Locus Tags

Friendly CLI:
```bash
mett reactions search --locus-tag BU_ATCC8492_02615 --locus-tag BU_ATCC8492_02516 --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query locus_tags=BU_ATCC8492_02615,BU_ATCC8492_02516
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search by UniprotIds

Friendly CLI:
```bash
mett reactions search --uniprot A7UXT0 --uniprot A7V3S8 --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query uniprot_ids=A7UXT0,A7V3S8
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search by multiple filters

Friendly CLI:
```bash
mett reactions search --locus-tag BU_ATCC8492_02615 --substrate akg_c --product oaa_c --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query locus_tags=BU_ATCC8492_02615 \
  --query substrate=akg_c \
  --query product=oaa_c
```

#### ME TT - API Integration Tests/Experimental APIs/Reactions/Reactions - Search by multiple filters 2

Friendly CLI:
```bash
mett reactions search --substrate akg_c --product oaa_c --format json
```

Generic CLI:
```bash
mett api request GET /api/reactions/search \
  --format json \
  --query substrate=akg_c \
  --query product=oaa_c
```

#### ME TT - API Integration Tests/Experimental APIs/Mutant-Growth/MutantGrowth - By Locus tag

Friendly CLI:
```bash
mett genes mutant-growth PV_ATCC8482_01384 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/PV_ATCC8482_01384/mutant-growth \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Mutant-Growth/MutantGrowth - fast-growing mutants

Friendly CLI:
```bash
mett mutant-growth search --max-doubling-time 2.0 --format json
```

Generic CLI:
```bash
mett api request GET /api/mutant-growth/search \
  --format json \
  --query max_doubling_time=2.0
```

#### ME TT - API Integration Tests/Experimental APIs/Mutant-Growth/MutantGrowth - Search for high-quality growth data

Friendly CLI:
```bash
mett mutant-growth search --exclude-double-picked true --media caecal --format json
```

Generic CLI:
```bash
mett api request GET /api/mutant-growth/search \
  --format json \
  --query exclude_double_picked=true \
  --query media=caecal
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Correlation/Fitness-Correlation - By Locus tag

Friendly CLI:
```bash
mett genes correlations BU_ATCC8492_02530 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_02530/correlations \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Correlation/Fitness-Correlation - two locus tags

Friendly CLI:
```bash
mett fitness-correlations correlation --locus-tag-a BU_ATCC8492_02530 --locus-tag-b BU_ATCC8492_02762 --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness-correlations/correlation \
  --format json \
  --query locus_tag_a=BU_ATCC8492_02530 \
  --query locus_tag_b=BU_ATCC8492_02762
```

#### ME TT - API Integration Tests/Experimental APIs/Fitness-Correlation/Fitness-Correlation - search

Friendly CLI:
```bash
mett fitness-correlations search --query "Vitamin B12" --format json
```

Generic CLI:
```bash
mett api request GET /api/fitness-correlations/search \
  --format json \
  --query query=Vitamin B12
```

#### ME TT - API Integration Tests/Experimental APIs/Orthologs/Orthologs- one-to-one for a gene

Friendly CLI:
```bash
mett genes orthologs BU_ATCC8492_00001 --one-to-one-only true --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00001/orthologs \
  --format json \
  --query one_to_one_only=true
```

#### ME TT - API Integration Tests/Experimental APIs/Orthologs/Orthologs- all for the gene

Friendly CLI:
```bash
mett genes orthologs BU_WH4_00023 --one-to-one-only false --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_WH4_00023/orthologs \
  --format json \
  --query one_to_one_only=false
```

#### ME TT - API Integration Tests/Experimental APIs/Orthologs/Orthologs - if two genes are orthologs

Friendly CLI:
```bash
mett orthologs pair --locus-tag-a BU_ATCC8492_00001 --locus-tag-b PV_ATCC8482_00001 --format json
```

Generic CLI:
```bash
mett api request GET /api/orthologs/pair \
  --format json \
  --query locus_tag_a=BU_ATCC8492_00001 \
  --query locus_tag_b=PV_ATCC8482_00001
```

#### ME TT - API Integration Tests/Experimental APIs/Operons/Operons- with at least 5 genes and regulatory elements

Friendly CLI:
```bash
mett operons search --min-gene-count 2 --has-tss true --has-terminator true --format json
```

Generic CLI:
```bash
mett api request GET /api/operons/search \
  --format json \
  --query min_gene_count=2 \
  --query has_tss=true \
  --query has_terminator=true
```

#### ME TT - API Integration Tests/Experimental APIs/Operons/Operons- statistics for a species

Friendly CLI:
```bash
mett operons get statistics --species BU --format json
```

Generic CLI:
```bash
mett api request GET /api/operons/statistics \
  --format json \
  --query species_acronym=BU
```

#### ME TT - API Integration Tests/Experimental APIs/Operons/Operons- by Operon Id

Friendly CLI:
```bash
mett operons get BU_ATCC8492_00003__BU_ATCC8492_00004 --format json
```

Generic CLI:
```bash
mett api request GET /api/operons/BU_ATCC8492_00003__BU_ATCC8492_00004 \
  --format json
```

#### ME TT - API Integration Tests/Experimental APIs/Operons/Operons- get operons for a gene

Friendly CLI:
```bash
mett genes operons BU_ATCC8492_00077 --format json
```

Generic CLI:
```bash
mett api request GET /api/genes/BU_ATCC8492_00077/operons \
  --format json
```
