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
- `git remote add origin <YOUR_OWN_PRIVATE_REMOTE_URL>`
- `git push -u origin main` (or your chosen default branch); use `git pull` after remote changes.
- Open and merge a genuine pull request from a feature branch, then capture evidence.

**Do not submit this guide as proof that a conflict or remote PR occurred.** Include logs/screenshots of your real actions.
