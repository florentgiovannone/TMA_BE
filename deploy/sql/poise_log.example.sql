-- Example schema for the TMA dashboard API (adjust to match your real poise_log).
-- Run as a superuser against database aba_cards.

CREATE TABLE IF NOT EXISTS poise_log (
  int_id SERIAL PRIMARY KEY,
  dtm_timestamp TIMESTAMPTZ DEFAULT NOW(),
  txt_message_type TEXT,
  txt_message TEXT,
  text_name TEXT
);

-- Optional sample row
-- INSERT INTO poise_log (txt_message_type, txt_message, text_name)
-- VALUES ('scan', 'https://example.takemearound.gallery/card/1', 'Card 1');

-- Optional visitor registry used by app.py to assign persistent visitor numbers:
-- AR<LANG><8 digits> (example: ARENGB00000001), one number per SAR value.
CREATE TABLE IF NOT EXISTS visitor_registry (
  id BIGSERIAL PRIMARY KEY,
  sar TEXT UNIQUE NOT NULL,
  language_code TEXT NOT NULL,
  visitor_number TEXT UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
