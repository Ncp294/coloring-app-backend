CREATE TABLE IF NOT EXISTS template (
    id SERIAL PRIMARY KEY,
    template_id TEXT UNIQUE,
    user_id TEXT,
    public BOOLEAN,
    img TEXT
);
