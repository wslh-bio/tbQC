process RESULTS {
    label 'process_single'

    container "quay.io/wslh-bioinformatics/spriggan-pandas:1.3.2"

    input:
    path("bbduk_results.tsv")
    path("coverage_stats.tsv")
    path("quast_results.tsv")
    path("mlst_results.tsv")
    path("kraken_results.tsv")
    path(kraken_version, stageAs:"kraken_version.yml")
    path("mash_results.tsv")

    output:
    path('tbqc_report.csv')

    script:
    """
    compile_results.py ${kraken_version} ${workflow.manifest.version}
    """
}
