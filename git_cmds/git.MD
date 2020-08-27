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
