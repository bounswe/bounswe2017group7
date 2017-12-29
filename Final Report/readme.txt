The branch projectreport will be the branch where everybody in the team will contribute to the project report.

There is a zip file, a tex file and a pdf of the project. Please fill your part of the report and upload to this branch.

To contribute to this branch follow these steps:

* First, get all the branches in the repo
git fetch
* You should now see the branch projectreport when you display branches
git branch
* Checkout to the remote branch by
git checkout -b projectreport origin/projectreport
* Make sure you are in the correct branch
git branch
* If you see a warning saying the head is detached
git checkout projectreport (if it fails: git checkout -b projectreport)
git branch --set-upstream projectreport origin/projectreport
* Now you are good to go. Make your changes. Add. Commit. And push to the branch
git push origin projectreport

* If you are now committing for the first time, please do a git pull before contributing again since everybody will update the same file, and it will happen very frequently.