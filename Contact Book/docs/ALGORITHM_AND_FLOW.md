# Algorithms and Workflow

## Student Result Management System
Start → Load JSON → Main Menu → Add/View/Search/Update/Delete/Statistics → Save JSON → Exit.

### Result Calculation
1. Add all subject marks.
2. Calculate percentage as total divided by number of subjects.
3. If any subject is below 35, result is FAIL.
4. Otherwise assign a grade based on percentage.

## Contact Book
Start → Load JSON → Main Menu → Create/Read/Search/Update/Delete/CSV Export → Save JSON → Exit.

### CRUD Mapping
- Create → `add_contact()`
- Read → `view_contacts()` / `view_contact_details()`
- Update → `update_contact()`
- Delete → `delete_contact()`
- Search → `search_contacts()`
- File storage → JSON
- Export → CSV
