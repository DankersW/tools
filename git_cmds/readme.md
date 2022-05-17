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

Squash all commits into one with MAIN as base branch

```shell
git checkout [branch-name]
git reset $(git merge-base main $(git branch --show-current))
git add -A
git commit -m "one commit on yourBranch"
git push --force origin upstream-branch
```

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

## Alterning commit author

```shell
# Switch user to the new author
git log
git checkout <commit-you-want-to-change>
git commit --amend --author "New Author Name <New Author Email>" # --> gives a new hash
git checkout <orgininal-branch>
git rebase -i <new-hash>
```
