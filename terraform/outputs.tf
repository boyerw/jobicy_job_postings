output "extract_glue_job" {
    value = aws_glue_job.extract_postings_job.name
}

output "glue_role" {
    value = aws_iam_role.glue_role.name
}