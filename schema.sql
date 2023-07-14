-- Company listed in stock market
create table company(
    id BIGSERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    date_of_listing DATE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- stock exchange example : NSE, BSE
create table stock_exchange(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- sector for a security example : TATAMOTORS will fall under Auto sector
create table sector(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- stock index such as NIFTY50, NIFTYNEXT50 ect.
create table stock_index(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    stock_exchange_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_stock_exchange FOREIGN KEY(stock_exchange_id) REFERENCES stock_exchange(id)
);

-- Security is other name for stock
create table security(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    code VARCHAR(12) NOT NULL UNIQUE, 
    company_id INTEGER NOT NULL UNIQUE,
    sector_id INTEGER NOT NULL,
    stock_exchange_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_stock_exchange FOREIGN KEY(stock_exchange_id) REFERENCES stock_exchange(id),
    CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES company(id),
    CONSTRAINT fk_sector FOREIGN KEY(sector_id) REFERENCES sector(id)
);

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
    phone VARCHAR(13),
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

-- Company Details
CREATE TABLE company_details(
    id BIGSERIAL PRIMARY KEY,
    bse VARCHAR(50) NOT NULL,
    nse VARCHAR(50) NOT NULL,
    series VARCHAR(50) NOT NULL,
    isin VARCHAR(12) NOT NULL UNIQUE,
    company_id INTEGER NOT NULL UNIQUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES company(id)
);

-- Company Management
CREATE TABLE company_management(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    company_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT u_management UNIQUE(name, designation, company_id),
    CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES company(id)
);

-- Company Overview
CREATE TABLE company_overview(
    id BIGSERIAL PRIMARY KEY,
    open NUMERIC(20,2), 
    previous_close NUMERIC(20,2), 
    volume NUMERIC(20,2), 
    value NUMERIC(20,2), 
    vwap NUMERIC(20,2), 
    beta NUMERIC(20,2), 
    high NUMERIC(20,2), 
    low NUMERIC(20,2), 
    uc_limit NUMERIC(20,2), 
    lc_limit NUMERIC(20,2), 
    _52_week_high NUMERIC(20,2), 
    _52_week_low NUMERIC(20,2), 
    ttm_eps NUMERIC(20,2), 
    ttm_pe NUMERIC(20,2), 
    sector_pe NUMERIC(20,2), 
    book_value_per_share NUMERIC(20,2), 
    pb NUMERIC(20,2), 
    face_value NUMERIC(20,2), 
    market_cap NUMERIC(20,2), 
    dividend_yeild NUMERIC(20,2), 
    _20d_avg_volume NUMERIC(20,2), 
    _20d_avg_volume_percentage NUMERIC(20,2),
    company_id INTEGER NOT NULL UNIQUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES company(id)
);

--Stock Index Constituents
create table stock_index_constituent(
    id BIGSERIAL PRIMARY KEY,
    security_id INTEGER NOT NULL,
    stock_index_id INTEGER NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT u_constituent UNIQUE(security_id, stock_index_id),
    CONSTRAINT fk_security FOREIGN KEY(security_id) REFERENCES security(id),
    CONSTRAINT fk_stock_index  FOREIGN KEY(stock_index_id) REFERENCES stock_index(id)
);

--functions and triggers
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON company
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON stock_exchange
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON sector
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON stock_index
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON security
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON stock_news
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON news_archive
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON logs
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON runners
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON app_user
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

--Initializing stock exchange
INSERT INTO stock_exchange(name) VALUES('NSE');
INSERT INTO stock_exchange(name) VALUES('BSE');