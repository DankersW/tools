# Git hooks

Running your own custom hooks is done by pointing the ```.git/hooks``` to your own ```hooks``` dir

```sh
mkdir hooks
git config core.hooksPath hooks
chmod 775 hooks/*
```

The ```.git/hooks``` contains some examples on hooks. They are ran by removing the ```.sample``` from the file name.

## Example pre-push hook

```sh
touch hooks/pre-push
```

Example python script that runs some go tooling

```python
#!/usr/bin/env python3

import subprocess

print("\nRunning pre-push git hook, doing a quick of your work before making it visualble to your colleages")
print(f"Note: If you dont want to run the hook add the option --no-verify \n")

# Running test-suite
cmd_test = "go test -race ./..."
test_result = subprocess.getoutput(cmd_test)
if "--- FAIL: " in test_result:
    print(f"FAILED: test suite ({cmd_test!r}). Results: \n {test_result}")
    exit(1)
else:
    print(f"PASSED: test suite ({cmd_test!r})")

# Linting
cmd_linting = "staticcheck ./..."
linting_result = subprocess.getoutput(cmd_linting)
if linting_result != "":
    print(f"FAILED: linting ({cmd_linting!r}). Results: \n {linting_result}")
    exit(1)
else:
    print(f"PASSED: linting ({cmd_linting!r})")

# Tidying dependancies
cmd_mod_tidy = "go mod tidy -v"
mod_tidy_result = subprocess.getoutput(cmd_mod_tidy)
if mod_tidy_result != "":
    print(f"FAILED: un-tidy dependency file ({cmd_mod_tidy!r}). Commiting new dependancies")
    subprocess.run('git add go.mod go.sum && git commit -m "ci: tidying dependancies"')
else:
    print(f"PASSED: tidy dependency file ({cmd_mod_tidy!r})")

print("\nAll passed, continuing with the push.\n")
```
