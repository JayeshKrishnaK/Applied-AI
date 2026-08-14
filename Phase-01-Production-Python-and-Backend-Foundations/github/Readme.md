# Starting with git from scratch

1. Install git in windows/Linux. use `git --version` to verify it.
2. Create a folder
3. To make the contents of the folder to be tracked by git - Go into the folder and run `git init`. This will create *.git* folder inside the folder we created and tracks the history of the folder.
3. Create a remote repository and get the URL. Name of the repo and the folder we create need not necessarlily be same.
4. Once we initialize the local git using `git init`, it automcatically creates a local branch called `main`. We can use `git branch -M master` to force rename the local branch or also can create a new branch using `git checkout -b master` or `git switch -c main`
5. Now to map the local repo to remote repo we created, run `git remote add origin <URL>`. Origin is the name given by us to repo and it's the common name used generally. It can be named anything.
6. To make our first commit, git wants to know who is the author of the commit. So we use `git config --global user.email <mail id>` and `git config --global user.name <any name>`. This tells git a user is trying to commit to origin with this mail id and user name. Git then validates their permissions to push to repo.
7. ***Git doesn't track empty folders*** So inorder to make our first push, create a file and then run:
        - `git add <file name>` - to stage the changes
        - `git commit -m "message"` - to create a local snapshot of the changes made.
        - `git push --set-upstream origin master` or `git push -u origin master` - pushes the changes to repo we named as origin with a branch master.
8. Now after this every time we push, we can just use `git push` as git now maps the local branch with remote branch.
9. `git remote -v` - to view the URL we connected to.
10. `git config user.name` - to view on what name I going to commit. Similar for mail as well.