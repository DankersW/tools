# Gitlab

## generate personal access token and use it

```sh
# Generate Personal Access Token with read_registry:
# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html
echo "machine gitlab.com login YOUR_EMAIL_ADDRESS password YOUR_ACCESS_TOKEN" >> ~/.netrc
```

## CI

clone a repo:

```yml
scripts:
    - git clone https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.com/vinnter/pyro/firectrl-core.git
```

get latest artifact from a branch in a repo:

```yml
scripts:
    - 'curl --location --output core.zip --header "JOB-TOKEN: $CI_JOB_TOKEN" https://gitlab.com/vinnter/pyro/firectrl-core/-/jobs/artifacts/development/download?job=build_core_g2'
```
