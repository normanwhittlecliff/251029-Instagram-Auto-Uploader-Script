# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog
and this project follows Semantic Versioning.

---

## 2026-02-03 - v1.6.0

### Fixed
- Fixed Instagram login failure caused by repeated password authentication.
- Added session-based login (`session.json`) to avoid 400 Bad Request errors.

### Changed
- Login flow now prefers saved sessions instead of raw credentials. A `session.json` is created if it`s the first time logging in. 
- The login_instagram() function was changed to:

```
def login_instagram():
    cl = Client()
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        cl.login(USERNAME, PASSWORD)
    else:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")
    return cl
```

---

...

---

## 2025-12-10 - v1.0.0

### Added
- Initial release.
- Image posts and video reels support.


