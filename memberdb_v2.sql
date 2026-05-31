CREATE DATABASE memberdb_v2;

USE memberdb_v2;

/* These tables contain public data maintained by the administrator */

CREATE TABLE IF NOT EXISTS groups (
    user_name_os VARCHAR(255),
    member_id INT NOT NULL,
    in_admin BOOLEAN,
    in_personel BOOLEAN,
    in_timekeeping BOOLEAN,
    in_training BOOLEAN
)

/*
These tables a populated form the SPMemberDB Members table.  SPMemberDB
will have to be checked regularly to keep these tables up to date.
*/

/* These tables contain public data maintained by persanel */

CREATE TABLE IF NOT EXISTS members (
    KEY member_id INT AUTO_INCREMENT NOT NULL UIQUE,
    user_name_logdb CHAR(20)
        COMMENT 'Matches securitylog.mdb',
    surname CHAR(50),
    given_name CHAR(50),
    nickname CHAR(50),
    birthday DATE,
    deceased BOOLEAN,
    dl_number VARCHAR(255),
    dl_state_code CHAR(3)
        COMMENT 'State/Province/Teritory code use by USPS or Post Canada',
    dl_expiry_date DATE,
    dl_report_date DATETIME
        COMMENT 'Date of most recent driver record report'
);

CREATE TABLE IF NOT EXISTS telephone_number (
    member_id INT NOT NULL,
    phone_type INT,
    phone_country_code INT
        COMMENT 'Telco contry code, 1 for NADA (US, Canada, etc.)',
    phone_number INT,
    phone_ext INT
);

CREATE TABLE IF NOT EXISTS email_address (
    member_id INT NOT NULL,
    email_type INT,
    email_addr VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS physical_address (
    member_id INT NOT NULL,
    phys_addr_type INT,
    country_code CHAR(3)
        COMMENT 'ISO contry code',
    postal_code VARCHAR(16),
    state_code VARCHAR(16),
    city_name VARCHAR(255),
    unit_number INT,
    street_number INT,
    street_name VARCHAR(255),
    street_direction CHAR(3),
    scscai_number INT,
    renter BOOLEAN,
    lease_exp_date DATE
);

CREATE TABLE IF NOT EXISTS member_notes (
/* Publicly readable personel notes about a member */
    member_id INT NOT NULL,
    note_time DATETIME,
    member_note VARCHAR(255)
);

/*
These tables created from the DispatchLogDB.
*/

CREATE TABLE IF NOT EXISTS hours_earned (
    member_id INT NOT NULL,
    start_time DATETIME,
    clock_hours INT,
    earned_hours INT,
    suplamental_hours BOOLEAN
        COMMENT 'TRUE when hours not extracted from DispatchLogDB',
    description VARCHAR(255)
);
