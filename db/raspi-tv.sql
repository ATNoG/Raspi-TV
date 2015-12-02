DROP TABLE IF EXISTS [Users];

DROP TABLE IF EXISTS [Dropbox];

DROP TABLE IF EXISTS [Twitter];

DROP TABLE IF EXISTS [Tweets];

DROP TABLE IF EXISTS [Files];

DROP TABLE IF EXISTS [HTMLSettings];

DROP TABLE IF EXISTS [YouTube];

DROP TABLE IF EXISTS [News];

DROP TABLE IF EXISTS [Weather];

DROP TABLE IF EXISTS [FrontEndOrder];

CREATE TABLE [Users] (
  [UserId]    TEXT PRIMARY KEY  NOT NULL, -- Username
  [Password]  TEXT              NOT NULL, -- Password
  [FirstName] TEXT              NOT NULL, -- User's first name
  [LastName]  TEXT              NOT NULL, -- User's last name
  [Email]     TEXT              NOT NULL, -- User's email
  [Date]      TEXT              NOT NULL   -- Date when account was created
);

CREATE TABLE [Dropbox] (
  [AppKey]    TEXT PRIMARY KEY  NOT NULL, -- Account Id to authenticate with
  [AppSecret] TEXT              NOT NULL,
  [AuthToken] TEXT              NOT NULL, -- Authentication Token used
  [DateAdded] TEXT              NOT NULL, -- When account was added to the database
  [Note]      TEXT              NOT NULL
);

CREATE TABLE [Twitter] (
  [ConsumerKey]    TEXT PRIMARY KEY NOT NULL,  -- Consumer Key - Not to display     |   These need to be manually set
  [ConsumerSecret] TEXT             NOT NULL,  -- Consumer Secret - Not to display  | over SSH or similar.
  [AccessKey]      TEXT             NOT NULL,  -- Client's key
  [AccessSecret]   TEXT             NOT NULL,  -- Client's Secret
  [Note]           TEXT             NOT NULL,  -- Note on account
  [DateAdded]      TEXT             NOT NULL    -- When the account was added to the database
);

CREATE TABLE [Tweets] (
  [TweetId]    INTEGER PRIMARY KEY NOT NULL, -- Tweet Id
  [Author]     TEXT                NOT NULL, -- Tweet's author
  [Tweet]      TEXT                NOT NULL, -- Tweet's text (actual tweet)
  [ToDisplay]  INTEGER DEFAULT 1   NOT NULL,   -- 'Boolean value' determining whether to display the tweet or not
  [TweetOrder] INTEGER DEFAULT -1  NOT NULL   -- Order in main page presentation
);

CREATE TABLE [Files] (
  [FilePath]  TEXT PRIMARY KEY    NOT NULL, -- Absolute path to file
  [ToDisplay] INTEGER DEFAULT 0   NOT NULL, -- 'Boolean value' determining whether to use the file or not
  [FileOrder] INTEGER DEFAULT -1  NOT NULL,
  [Type]      TEXT                NOT NULL
);

CREATE TABLE [HTMLSettings] (
  [IdName]  TEXT PRIMARY KEY NOT NULL, -- To be added
  [Content] TEXT             NOT NULL   -- To be added
);

CREATE TABLE [YouTube] (
  [VideoId]   TEXT PRIMARY KEY NOT NULL,
  [FilePath]  TEXT             NOT NULL,
  [VideoName] TEXT
);

CREATE TABLE [News] (
  [NewsId]       INTEGER PRIMARY KEY AUTOINCREMENT,
  [Title]        TEXT                     NOT NULL,
  [Date_Updated] TEXT,
  [Author]       TEXT,
  [Content]      TEXT
);

CREATE TABLE [Weather] (
  [Wind] TEXT PRIMARY KEY NOT NULL,
  [Humidity] TEXT,
  [Temperature] TEXT,
  [Weather_Code] TEXT,
  [Sunrise_Time] TEXT,
  [Sunset_Time] TEXT
);

CREATE TABLE [FrontEndOrder] (
  [Service]       TEXT PRIMARY KEY  NOT NULL,
  [ToDisplay]     TEXT    DEFAULT 1 NOT NULL,
  [ServicesOrder] INTEGER DEFAULT 0 NOT NULL
);

INSERT INTO [Dropbox] VALUES (
    'rbfnah947b3iobb',
    'l4r9iivgz4onshk',
    '',
    '',
    '00:00AM on January 1, 2000'
);

INSERT INTO [Twitter] VALUES (
    'LBkx6ijeOITvfsArKgdKH2wOL',
    'GqQodc99leDRSBw1d89N8uKBKJlPkMvrFXNfLJauzMwxF4Chxx',
    '',
    '',
    '',
    '00:00AM on January 1, 2000'
);

INSERT INTO [HTMLSettings] VALUES (
    'location',
    'DETI'
);

INSERT INTO [HTMLSettings] VALUES (
    'locationDescription',
    'Departamento de Electrónica, Telecomunicações e Informática'
);

INSERT INTO [HTMLSettings] VALUES (
    'background',
    'To be added'
);

INSERT INTO [HTMLSettings] VALUES (
    'weather',
    'Aveiro'
);
INSERT INTO [HTMLSettings] VALUES (
    'feed',
    'http://deti-cdn.clients.ua.pt/'
);

INSERT INTO [FrontEndOrder] VALUES (
    'News',
    '1',
    1
);

INSERT INTO [FrontEndOrder] VALUES (
    'Youtube',
    '1',
    2
);

INSERT INTO [FrontEndOrder] VALUES (
    'Dropbox Photos',
    '1',
    3
);

INSERT INTO [FrontEndOrder] VALUES (
    'Dropbox Videos',
    '1',
    4
);
