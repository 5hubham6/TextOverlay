-- Initialize the database schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table for authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Images table to store generated overlays
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    image_path VARCHAR(500) NOT NULL,
    quote_text TEXT,
    quote_author VARCHAR(200),
    font_style VARCHAR(50) DEFAULT 'impact',
    text_position VARCHAR(20) DEFAULT 'bottom',
    is_public BOOLEAN DEFAULT TRUE,
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quotes table for storing custom quotes
CREATE TABLE quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    author VARCHAR(200),
    source_file VARCHAR(200),
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions for JWT blacklist
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Image likes/favorites
CREATE TABLE image_likes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    image_id UUID REFERENCES images(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, image_id)
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_images_user_id ON images(user_id);
CREATE INDEX idx_images_created_at ON images(created_at DESC);
CREATE INDEX idx_images_public ON images(is_public) WHERE is_public = TRUE;
CREATE INDEX idx_quotes_user_id ON quotes(user_id);
CREATE INDEX idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at);
CREATE INDEX idx_image_likes_user_image ON image_likes(user_id, image_id);

-- Insert some sample data
INSERT INTO users (username, email, password_hash, is_verified) VALUES
('demo_user', 'demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeAasdWFcFjlhJm/a', TRUE);

-- Sample quotes (keeping original data structure)
INSERT INTO quotes (body, author, source_file, is_approved) VALUES
('A dog is the only thing on earth that loves you more than you love yourself.', 'Josh Billings', 'sample_quotes.csv', TRUE),
('The world would be a nicer place if everyone had the ability to love as unconditionally as a dog.', 'M.K. Clinton', 'sample_quotes.csv', TRUE),
('Dogs do speak, but only to those who know how to listen.', 'Orhan Pamuk', 'sample_quotes.csv', TRUE),
('The more people I meet the more I like my dog.', 'Unknown', 'sample_quotes.csv', TRUE);
