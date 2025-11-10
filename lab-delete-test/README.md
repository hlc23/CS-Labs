# lab-delete-test

A minimal Flask lab used to test the `package-labs.yml` workflow behavior when a lab directory is deleted.

How to run locally:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000

To test the workflow behavior:
1. Commit and push this directory so the workflow creates `build/lab-delete-test.zip`.
2. Delete this directory, commit and push — the updated workflow should remove `build/lab-delete-test.zip` and commit that removal back to the repo.
