# IAM Role with cross-account trust relationship
resource "aws_iam_role" "cross_account_role" {
  name        = "POCTranscribeCrossAccountAssumeRole"
  description = "Role that can be assumed by AWS account 211125594036"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::211125594036:root"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "s3_bucket_access_policy" {
  name        = "transcribe-s3-bucket-access-policy"
  description = "Policy to allow read access on source bucket and write access on target bucket"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::aws-transcribe-poc-src-001",
          "arn:aws:s3:::aws-transcribe-poc-src-001/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = [
          "arn:aws:s3:::aws-transcribe-poc-tgt-001/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_bucket_access_policy_attachment" {
  role       = aws_iam_role.cross_account_role.name
  policy_arn = aws_iam_policy.s3_bucket_access_policy.arn
}


resource "aws_iam_role_policy_attachment" "transcribe_full_access" {
  role       = aws_iam_role.cross_account_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonTranscribeFullAccess"
}
