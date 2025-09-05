include .env
.PHONY: run create-bucket

export AWS_PAGER :=

run:
	cd terraform && terraform apply --auto-approve

create-bucket:
	@aws s3api create-bucket \
		--bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" \
		--region "${AWS_REGION}" \
		--create-bucket-configuration LocationConstraint="${AWS_REGION}" 2>/dev/null || \
		(aws s3api head-bucket --bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" 2>/dev/null && echo "Bucket already exists") || \
		(echo "❌ Failed to create bucket" && exit 1)

	@aws s3api put-bucket-versioning \
		--bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" \
		--versioning-configuration Status=Enabled

	@aws s3api put-bucket-encryption \
		--bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" \
		--server-side-encryption-configuration "{\"Rules\":[{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\":\"AES256\"}}]}"

	@aws s3api put-public-access-block \
		--bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" \
		--public-access-block-configuration "{\"BlockPublicAcls\":true,\"IgnorePublicAcls\":true,\"BlockPublicPolicy\":true,\"RestrictPublicBuckets\":true}"

	@echo "✅ Bucket "${TERRAFORM_STATE_S3_BUCKET_NAME}" configured successfully"