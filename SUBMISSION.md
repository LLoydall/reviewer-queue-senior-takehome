# Submission
## Summary of changes
- Enforced strict state transitions for all reviewer actions on the backend to comply with business rules.
- Fixed the active queue sorting logic to correctly prioritize urgency by risk level, customer tier, and then submission date.
- Implemented a tabbed interface in the frontend to separate the active queue from terminated items.

## Bugs fixed
- Items in terminal states (approved, rejected, escalated) can no longer be modified or claimed.
- Unassigned items can no longer be approved, rejected, or escalated without first being claimed.
- The active queue now correctly excludes all terminal items, rather than just filtering out approved ones.

## Product/UX decisions
- **Separate Terminal Tray:** Instead of merely hiding closed items, I introduced a "Closed" tab. This keeps the active queue clean while allowing reviewers to reference their completed work, and sets the foundation for future pagination.
- **Helpful Error Messages:** Added user-friendly error messages for invalid actions, improving the reviewer experience by clearly indicating why an action failed.
- **Auto-Advance:** When an item is moved to a terminal state from the Active tab, it is immediately removed from the list, and the UI automatically selects the next available item to maintain reviewer momentum.

## Tests added
- Validated that the active queue properly filters out terminal states and correctly applies the multi-level urgency sorting (risk > tier > date).
- Validated that terminal items are strictly locked and return a 409 Conflict if modified.
- Validated that invalid state transitions (e.g., claiming an in_review item) are cleanly rejected.  

## Known gaps
- **Frontend Unit Testing:** There are currently no automated tests for the Vue frontend. Adding component tests (e.g., via Vitest and Vue Test Utils) would help verify UI-specific logic, such as the tab switching and dynamic button disabled states.

## Files changed and why
- `backend/app/main.py:` Extracted an is_terminal helper function to centralize business logic, updated `list_review_items` to support sorting and `list_type` filtering, and enforced strict status transition rules in apply_action.

- `backend/tests/test_workflow.py:` Created this file to introduce targeted tests for the queue sorting, filtering, and strict state transition locks.

- `frontend/src/api.ts:` Updated `fetchReviewItems` to accept a `listType` parameter to support the new UI tabs.

- `frontend/src/App.vue:` Introduced tab state logic, updated `performAction` to remove terminal items from the active view upon completion, and bound action buttons to disabled states based on the workflow rules.

- `frontend/src/styles.css:` Added styling for the new queue tabs and empty state indicators.


## AI assistance used

I utilized an AI assistant to quickly draft the multi-level Python sorting logic for the queue urgency, brainstorm the UX for handling terminal items (leading to the tabbed approach), and generate the boilerplate for the Pytest validation tests. I reviewed all generated code to ensure it met the exact workflow requirements before committing.
