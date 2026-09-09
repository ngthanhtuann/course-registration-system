-- Add the admin profile table omitted by the original legacy schema.
-- Safe to re-run; existing users and profiles are preserved.
CREATE TABLE IF NOT EXISTS administrators (
    admin_id varchar(20) PRIMARY KEY,
    user_id varchar(20) NOT NULL UNIQUE REFERENCES users(user_id)
);
INSERT INTO administrators (admin_id, user_id)
SELECT user_id, user_id FROM users WHERE lower(role::text) = 'admin'
ON CONFLICT DO NOTHING;
