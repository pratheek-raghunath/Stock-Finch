create table stock_news(
    id BIGSERIAL PRIMARY KEY,
    headline text UNIQUE NOT NULL,
    description text,
    image_url text,
    source VARCHAR(50) NOT NULL,
    news_link text NOT NULL,
    publish_date TIMESTAMP NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- registered users
create table app_user(
    id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- User can add stocks to watchlist for a registered user
create table watchlist(
    id BIGSERIAL PRIMARY KEY,
    app_user_id INTEGER NOT NULL,
    security_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_app_user FOREIGN KEY(app_user_id) REFERENCES app_user(id),
    CONSTRAINT fk_security FOREIGN KEY(security_id) REFERENCES security(id)   
);

-- You can add news to archive to read later.
create table news_archive(
    id BIGSERIAL PRIMARY KEY,
    app_user_id INTEGER NOT NULL,
    news_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_app_user FOREIGN KEY(app_user_id) REFERENCES app_user(id),
    CONSTRAINT fk_news FOREIGN KEY(news_id) REFERENCES stock_news(id) 
);

-- Runner status ENUM
CREATE TYPE RUNNER_STATUS AS ENUM ('SUCCESS', 'FAILED', 'RUNNING');

-- Status of the extractors
CREATE TABLE runners(
    id BIGSERIAL PRIMARY KEY,
    extractor_name VARCHAR(100) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status RUNNER_STATUS
);


-- Log status ENUM
CREATE TYPE RUNNER_SEVERITY AS ENUM ('SUCCESS', 'FAILED');

-- Status of the logs
CREATE TABLE logs(
    id BIGSERIAL PRIMARY KEY,
    runner_id INTEGER NOT NULL,
    extractor_name VARCHAR(100) NOT NULL,
    log_date TIMESTAMP NOT NULL,
    severity RUNNER_SEVERITY,
    message TEXT,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_runner FOREIGN KEY(runner_id) REFERENCES runners(id)
);