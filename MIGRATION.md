# Dribdat vNext: Migration Strategy

Moving from the legacy Flask stack to the modern FastAPI stack requires a robust data migration path. We utilize the **Frictionless Data Package** format as our intermediate "bridge."

## 1. Phase 1: Export from Legacy Dribdat
The legacy application already includes some support for data exports. We recommend enhancing the existing `dribdat/apipackage.py` to produce a full Data Package:

- **Resource: Users:** Export all active users (excluding passwords, which will need to be reset or migrated via a secure hash if compatible).
- **Resource: Events:** All hackathon event metadata.
- **Resource: Projects:** All project data including team memberships.
- **Resource: Activities:** The full "Dribs" history for each project.

## 2. Phase 2: Data Package Validation
Before importing into vNext, the exported package can be validated using the `frictionless` CLI:
```bash
frictionless validate datapackage.json
```
This ensures that the data conforms to the expected schema and that there are no broken relationships (e.g., a project pointing to a non-existent event).

## 3. Phase 3: Import into Dribdat vNext
The vNext application will include a migration CLI:
```bash
dribdat-cli migrate --source datapackage.json
```

### Key Import Steps:
1. **Dependency Sorting:** Import Events first, then Categories, then Users, then Projects, then Activities.
2. **Password Handling:** Since FastAPI (via Passlib/Bcrypt) might use different salt/rounds than Flask-Bcrypt, we recommend:
    - Carrying over the hashes and attempting compatibility.
    - OR flagging users to "Reset Password on First Login."
3. **ID Mapping:** Maintain a mapping of old IDs to new IDs if the primary keys change during the import process.

## 4. Phase 4: S3 Media Migration
If S3 was used in the legacy app, the `image_url` fields in the database will likely remain valid if the same S3 bucket is used. If moving buckets:
1. Use a script to iterate through all `image_url` and `logo_url` fields.
2. Download from the old bucket and upload to the new bucket.
3. Update the database record in vNext.

## 5. Why this strategy?
- **Agent Friendly:** Migration logic is decoupled from both the old and new database schemas.
- **Standardized:** Uses the [Data Package](https://specs.frictionlessdata.io/data-package/) standard.
- **Resilient:** You can edit the intermediate JSON/CSV files manually if data cleanup is required during the transition.
