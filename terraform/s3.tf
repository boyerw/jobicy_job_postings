resource "aws_s3_bucket" "data_lake" {
    # bucket_prefix = "${var.project}-${data.aws_called_identity.current.account_id}-scripts"
    bucket_prefix = "jobicy-data"
}

# s3 bucket with public access for storing scripts
resource "aws_s3_bucket" "scripts" {
    bucket_prefix = "jobicy-scripts"
}

resource "aws_s3_bucket_public_access_block" "scripts" {
    bucket = aws_s3_bucket.scripts.id

    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

# The Python scripts for the glue job
resource "aws_s3_object" "glue_job_extract_postings_script" {
  bucket = aws_s3_bucket.scripts.id
  key    = "extract_postings.py"
  source = "./assets/extract_postings.py"

  etag = filemd5("./assets/extract_postings.py")
}