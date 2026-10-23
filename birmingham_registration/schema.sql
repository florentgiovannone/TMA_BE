CREATE TABLE IF NOT EXISTS artworks (
  slug text PRIMARY KEY,
  title text NOT NULL,
  stock integer NOT NULL CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS registrations (
  id uuid PRIMARY KEY,
  name varchar(100) NOT NULL,
  surname varchar(100) NOT NULL,
  email varchar(254) NOT NULL,
  company varchar(200) NOT NULL,
  position varchar(200) NOT NULL,
  town varchar(100) NOT NULL,
  country varchar(100) NOT NULL,
  artwork_slug text NOT NULL REFERENCES artworks (slug),
  status text NOT NULL CHECK (status IN ('unconfirmed', 'confirmed')),
  consent_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL,
  confirmed_at timestamptz,
  expires_at timestamptz NOT NULL,
  token_hash text CHECK (token_hash IS NULL OR token_hash ~ '^[0-9a-f]{64}$')
);

ALTER TABLE registrations ADD COLUMN IF NOT EXISTS phone_dial_code varchar(8);
ALTER TABLE registrations ADD COLUMN IF NOT EXISTS phone_number varchar(20);
ALTER TABLE registrations ADD COLUMN IF NOT EXISTS phone_extension varchar(10);

CREATE UNIQUE INDEX IF NOT EXISTS registrations_one_confirmed
  ON registrations (email)
  WHERE status = 'confirmed';

CREATE UNIQUE INDEX IF NOT EXISTS registrations_one_unconfirmed
  ON registrations (email)
  WHERE status = 'unconfirmed';

CREATE UNIQUE INDEX IF NOT EXISTS registrations_token_hash
  ON registrations (token_hash)
  WHERE token_hash IS NOT NULL;

INSERT INTO artworks (slug, title, stock) VALUES
  ('the-star-of-bethlehem', 'The Star of Bethlehem', 0),
  ('the-golden-boys', 'The Golden Boys', 0)
ON CONFLICT (slug) DO NOTHING;
