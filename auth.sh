
aws iam list-policies --scope Local --query 'Policies[].[Arn]' --output text | while read -r policy_arn; do aws iam get-policy --policy-arn "$policy_arn" --query 'Policy.DefaultVersionId' --output text | while read -r version_id; do aws iam get-policy-version --policy-arn "$policy_arn" --version-id "$version_id" --query 'PolicyVersion.Document' --output json | jq -e '.Statement[] | select(.Action == "sts:AssumeRole" and .Principal.AWS == "*")' && echo "Policy ARN matching criteria: $policy_arn"; done; done
#!/bin/bash; OUTPUT_DIR="./lambda_env_vars"; mkdir -p "${OUTPUT_DIR}"; FUNCTION_NAMES=$(aws lambda list-functions --query 'Functions[].FunctionName' --output text); for FUNCTION_NAME in $FUNCTION_NAMES; do echo "Fetching environment variables for ${FUNCTION_NAME}..."; aws lambda get-function-configuration --function-name "${FUNCTION_NAME}" --query 'Environment.Variables' --output json > "${OUTPUT_DIR}/${FUNCTION_NAME}_env_vars.json"; if [ $? -eq 0 ]; then echo "Saved environment variables for ${FUNCTION_NAME}"; else echo "Failed to fetch environment variables for ${FUNCTION_NAME}"; fi; done; echo "All done."

#!/bin/bash
users=$(aws iam list-users --query 'Users[*].UserName' --output text); for user in $users; do echo "User: $user"; echo "Directly Attached Policies:"; aws iam list-attached-user-policies --user-name "$user" --query 'AttachedPolicies[*].PolicyName' --output table; echo "Group Policies:"; groups=$(aws iam list-groups-for-user --user-name "$user" --query 'Groups[*].GroupName' --output text); for group in $groups; do echo " Group: $group"; aws iam list-attached-group-policies --group-name "$group" --query 'AttachedPolicies[*].PolicyName' --output table; done; echo "--------------------------------"; done

#!/bin/bash

# List all IAM roles and get their names
for role_name in $(aws iam list-roles | jq -r '.Roles[].RoleName'); do
    echo "Checking role: $role_name"
    # For each role, list the attached policies
    for policy_arn in $(aws iam list-attached-role-policies --role-name "$role_name" | jq -r '.AttachedPolicies[].PolicyArn'); do
        # Get the default version of the policy
        policy_version=$(aws iam get-policy --policy-arn "$policy_arn" | jq -r '.Policy.DefaultVersionId')
        # Get the policy document
        policy_document=$(aws iam get-policy-version --policy-arn "$policy_arn" --version-id "$policy_version" | jq -r '.PolicyVersion.Document')
        # Check if the policy document contains "s3:GetObject" or "s3:Get*"
        if echo "$policy_document" | jq -r 'to_string' | grep -E "s3:GetObject|s3:Get\*" > /dev/null; then
            echo "Role: $role_name has a policy with 's3:GetObject' or 's3:Get*': $policy_arn"
        fi
    done
done

aws iam list-roles | jq -r '.Roles[].RoleName' | while read -r role; do aws iam list-attached-role-policies --role-name "$role" | jq -r '.AttachedPolicies[].PolicyArn' | while read -r policy_arn; do aws iam get-policy-version --policy-arn "$policy_arn" --version-id $(aws iam get-policy --policy-arn "$policy_arn" | jq -r '.Policy.DefaultVersionId') | jq -r '.PolicyVersion.Document.Statement[] | select(.Effect == "Allow" and .Action | (type == "string" and . == "s3:GetObject" or startswith("s3:Get")) or (type == "array" and .[] | . == "s3:GetObject" or startswith("s3:Get"))) | .Resource' | while read -r resource; do echo "Role: $role, Policy ARN: $policy_arn, Resource: $resource"; done; done; done



for bucket in $(aws s3api list-buckets --query 'Buckets[].Name' --output text); do acl=$(aws s3api get-bucket-acl --bucket "$bucket" --output json); readPermissions=$(echo $acl | jq -e '.Grants[] | select(.Grantee.URI=="http://acs.amazonaws.com/groups/global/AuthenticatedUsers" and (.Permission=="READ" or .Permission=="FULL_CONTROL"))' 2>/dev/null); if [ $? -eq 0 ]; then echo "Bucket with AuthenticatedUsers READ permission found: $bucket"; fi; done