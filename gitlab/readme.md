# Gitlab

## generate personal access token and use it

```sh
# Generate Personal Access Token with read_registry:
# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
echo "machine gitlab.com login YOUR_EMAIL_ADDRESS password YOUR_ACCESS_TOKEN" >> ~/.netrc
```