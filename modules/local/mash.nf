process MASH {
    tag "$meta.id"
    label 'process_medium'

    container "staphb/mash:2.3"

    input:
    tuple val(meta), path(contigs)

    output:
    path("*.mash.tsv")     , emit: mash_files
    path "versions.yml"    , emit: versions

    when:
    task.ext.when == null || task.ext.when

    script:
    def args = task.ext.args ?: ''
    def prefix = task.ext.prefix ?: "${meta.id}"
    def memory = task.memory.toGiga()
    """
    mash sketch ${prefix}.contigs.fa
    mash dist /db/RefSeqSketchesDefaults.msh ${prefix}.contigs.fa.msh > ${prefix}.distances.tab
    sort -gk3 ${prefix}.distances.tab > ${prefix}.mash.tsv

    cat <<-END_VERSIONS > versions.yml
    "${task.process}":
        mash: \$(echo \$(mash --version 2>&1) | sed 's/^.*mash //')
    END_VERSIONS
    """
}
