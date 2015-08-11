DROP TABLE IF EXISTS [Users];

DROP TABLE IF EXISTS [Accounts];

DROP TABLE IF EXISTS [Twitter];

DROP TABLE IF EXISTS [Tweets];

DROP TABLE IF EXISTS [Files];

DROP TABLE IF EXISTS [HTMLSettings];

CREATE TABLE [Users] (
  [UserId]    TEXT PRIMARY KEY  NOT NULL, -- Username
  [Password]  TEXT              NOT NULL, -- Password
  [FirstName] TEXT              NOT NULL, -- User's first name
  [LastName]  TEXT              NOT NULL, -- User's last name
  [Email]     TEXT              NOT NULL, -- User's email
  [Date]      TEXT              NOT NULL   -- Date when account was created
);

CREATE TABLE [Accounts] (
  [AccountId] TEXT PRIMARY KEY  NOT NULL, -- Account Id to authenticate with
  [AuthToken] TEXT              NOT NULL, -- Authentication Token used
  [DateAdded] TEXT              NOT NULL, -- When account was added to the database
  [Note]      TEXT              NOT NULL, -- Note on account
  [Service]   TEXT              NOT NULL   -- Name of the related service (e.g.: 'dropbox', 'twitter', ...)
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
  [TweetId]   INTEGER PRIMARY KEY NOT NULL, -- Tweet Id
  [Author]    TEXT                NOT NULL, -- Tweet's author
  [Tweet]     TEXT                NOT NULL, -- Tweet's text (actual tweet)
  [ToDisplay] INTEGER DEFAULT 0   NOT NULL   -- 'Boolean value' determining whether to display the tweet or not
);

CREATE TABLE [Files] (
  [FilePath]  TEXT PRIMARY KEY  NOT NULL, -- Absolute path to file
  [ToDisplay] INTEGER           NOT NULL, -- 'Boolean value' determining whether to use the file or not
  [AccountId] TEXT              NOT NULL, -- Refers which dropbox account the file belongs to
  FOREIGN KEY ([AccountId]) REFERENCES [Accounts] ([AccountId])
  ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE [HTMLSettings] (
  [IdName]  TEXT PRIMARY KEY NOT NULL, -- To be added
  [Content] TEXT             NOT NULL   -- To be added
);

INSERT INTO [Users] VALUES (
  'RJJ',
  '65304dac3823069673aa9d3b90dcb9f44938e2d12f58509addc915d08922b64b', -- "ricardo"
  'Ricardo',
  'Jesus',
  'ricardojesus@ua.pt',
  'January 1, 2015'
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
