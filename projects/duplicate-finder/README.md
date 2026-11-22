# Duplicate Finder

**Problem:** Finding redundant files manually is slow, and automated deletion is risky.

**Solution:** Scan by file size, calculate SHA-256 only for same-size candidates and output groups of equal-content files.

```bash
python main.py /path/to/a/test/folder
```

**Safety:** This program only reads files. It does **not** delete anything, does not follow symlinks and skips unreadable files. File content can change while scanning; use on stable folders.
