# Good to remember GIT commands

## Rebase

```shell
git checkout master
git pull origin master
git checkout [branch-name]
git rebase master [branch-name]
git push -f origin [branch-name]
```

## Squash commits

```shell
git rebase -i HEAD~[number-of-commits]
```

in VM selected the first on to be ```e``` and the others write ```s```

## Clean-up outdated branch references

```shell
git remote prune origin
```

## Renaming local and remote

```shell
# Rename the local branch to the new name
git branch -m <old_name> <new_name>

# Delete the old branch on remote - where <remote> is, for example, origin
git push <remote> --delete <old_name>

# Push the new branch to remote
git push <remote> <new_name>

# Reset the upstream branch for the new_name local branch
git push <remote> -u <new_name>
```
