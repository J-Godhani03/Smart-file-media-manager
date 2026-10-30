# Task 13 — Git workflow

This package includes a Git repo with commits and example feature branches merged during packaging. The history records package assembly, **not an invented semester-long student workflow**. Continue developing with authentic commits.

Useful commands (from the project root):

```
git status
git log --oneline --graph --all --decorate
git switch -c feature/improve-preview
# change app/view.py, run tests
git add app/view.py
git commit -m "Improve image preview layout"
git switch main
git merge feature/improve-preview
```

## Show conflict resolution (controlled exercise, only if needed)

1. Create two branches from the same commit.
2. Edit the **same line** of a harmless test/demo text file differently on each branch, commit both changes.
3. Merge one branch into the other; Git should report a conflict.
4. Edit the file to the correct content, remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), then `git add` and `git commit`.
5. Record the commands, terminal output and a screenshot of the conflict/resolution in your technical report.

## Remote activity, where permitted

- Create a private GitHub/GitLab repository according to lecturer rules.
- `git remote add origin <https://github.com/J-Godhani03/Smart-file-media-manager.git>`
- `git push -u origin main` (or your chosen default branch); use `git pull` after remote changes.
- Open and merge a genuine pull request from a feature branch, then capture evidence.




Terminal Out that Git sucusefully connected 


PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> git add docs/GIT_WORKFLOW.md docs/Technical_Report.pdf docs/Test_Plan.pdf presentation/Project_Presentation.pptx
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> git commit -m "Update final documentation and presentation"
On branch main
nothing to commit, working tree clean
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> git status
On branch main
nothing to commit, working tree clean
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> git ls-remote --heads origin
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> git push -u origin main
Enumerating objects: 81, done.
Counting objects: 100% (81/81), done.
Delta compression using up to 16 threads
Compressing objects: 100% (72/72), done.
Writing objects: 100% (81/81), 634.41 KiB | 10.23 MiB/s, done.
Total 81 (delta 21), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (21/21), done.
To https://github.com/J-Godhani03/Smart-file-media-manager.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> ^C
PS C:\Users\HP\Downloads\Jaimin_M20_T2\Smart_File_Media_Manager> 






!