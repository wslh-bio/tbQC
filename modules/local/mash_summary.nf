process MASH_SUMMARY {
    label 'process_single'

    container "quay.io/wslh-bioinformatics/spriggan-pandas:1.3.2"

    input:
    path("data/*")

    output:
    path("mash_results.tsv"), emit: mash_tsv

    script:
    """
    mash_summary.py
    """
}
