-- Preserve legacy profile names while exposing the column used by the backend.
BEGIN;
ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name varchar(100);
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'users' AND column_name = 'fullname'
    ) THEN
        UPDATE users SET full_name = fullname WHERE full_name IS NULL;
    END IF;
END $$;
UPDATE users SET full_name = username WHERE full_name IS NULL;
COMMIT;
