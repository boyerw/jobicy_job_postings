resource "aws_glue_job" "extract_postings_job" {
    name         = "Jobicy-extract-postings-job"
    role_arn     = aws_iam_role.glue_role.arn
    # glue_version = "5.0"

    command {
        name            = "glue_extract"
        script_location = "s3://${aws_s3_bucket.scripts.id}/${aws_s3_object.glue_job_extract_postings_script.id}"
        python_version  = 3
    }

    default_arguments = {
        "--enable-job-insights" = "true"
        "--job-language"        = "python"
        "--conf"                = "spark.rpc.message.maxSize=2000"
        "--enable-metrics"      = "true"
        "--s3_bucket"           = aws_s3_bucket.data_lake.bucket
        # "--source_path"         = "staging/reviews_Toys_and_Games.json.gz"
        "--target_path"         = "data_science_postings/"
        # "--compression"         = "snappy"
        # "--partition_cols"      = jsonencode(["year", "month"])
    }

    timeout = 15

    number_of_workers = 2
    worker_type       = "G.1X"
}