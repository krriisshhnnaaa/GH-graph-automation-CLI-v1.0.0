# CLI Ideas & Roadmap

A collection of planned improvements and future features for the GitHub Graph Automation CLI.

---

## 1. Easier Installation with `uv`

**Goal:** Make installation and distribution of the CLI as simple and fast as possible.

### Ideas

* [ ] Package the CLI using `uv`
* [ ] Simplify dependency installation
* [ ] Provide a straightforward installation command
* [ ] Make the CLI easier to install on a fresh machine
* [ ] Improve first-time setup experience

### Future Considerations

* Cross-platform installation
* Version management
* Simple upgrade/update workflow

---

## 2. Secure GitHub Authentication

**Goal:** Provide a secure and user-friendly way to authenticate with GitHub.

### Ideas

* [ ] Implement secure GitHub authentication
* [ ] Avoid requiring users to manually expose tokens
* [ ] Store credentials securely
* [ ] Validate authentication before starting an operation
* [ ] Provide clear authentication error messages

### Future Considerations

* OAuth-based authentication
* GitHub CLI integration
* Token/keychain management
* Authentication profiles for multiple accounts

---

## 3. Enhanced Display & Status Features

**Goal:** Improve the CLI's terminal interface and make automation progress easier to understand.

### Ideas

* [ ] Expand push status information
* [ ] Add more detailed progress indicators
* [ ] Display current operation
* [ ] Display push queue/progress
* [ ] Improve formatting and readability
* [ ] Add useful summary information after completion

### Future Considerations

* Interactive terminal UI
* Live progress updates
* Configurable display verbosity
* Quiet mode for scripting
* Debug mode

---

## 4. Dynamic File Handling

**Goal:** Allow new files to be added while existing files are still being processed, without requiring the user to create a new repository.

### Current Problem

If files are added while the CLI is already pushing existing files, the current workflow may require creating or starting another repository/workflow.

### Desired Behavior

The CLI should be able to detect newly added files during an active operation and incorporate them into the existing workflow.

```text
Initial files
     │
     ▼
   Push Queue
     │
     ├── File A ──► Push
     ├── File B ──► Push
     └── File C ──► Push
                │
                │ New file detected
                ▼
             File D
                │
                ▼
          Add to queue
                │
                ▼
             Push
```

### Ideas

* [ ] Detect newly added files during an active run
* [ ] Add newly detected files to the existing queue
* [ ] Avoid creating a new repository
* [ ] Preserve existing push state
* [ ] Handle files added multiple times during a run
* [ ] Prevent duplicate processing

### Future Considerations

* Real-time directory monitoring
* Configurable scan intervals
* Dynamic queue management
* Pause/resume support
* Persistent job state

---

## Priority

| Feature                      | Priority | Status  |
| ---------------------------- | -------- | ------- |
| `uv` installation            | High     | Planned |
| Secure GitHub authentication | High     | Planned |
| Enhanced display features    | Medium   | Planned |
| Dynamic file handling        | High     | Planned |

---

## Notes

This document is intentionally kept as a living roadmap. New ideas, improvements, and potential architectural changes can be added as the CLI evolves.
