DROP TABLE IF EXISTS [Users];

DROP TABLE IF EXISTS [Accounts];

DROP TABLE IF EXISTS [Tweets];

CREATE TABLE [Users](
  [UserId]    TEXT PRIMARY KEY  NOT NULL,
  [Password]  TEXT              NOT NULL,
  [FirstName] TEXT              NOT NULL,
  [LastName]  TEXT              NOT NULL,
  [Email]     TEXT              NOT NULL
);

CREATE TABLE [Accounts](
  [Id]          TEXT PRIMARY KEY  NOT NULL,
  [Password]    TEXT              NOT NULL,
  [ServiceName] TEXT              NOT NULL
);

CREATE TABLE [Tweets](
  [Author] TEXT NOT NULL,
  [Tweet]  TEXT NOT NULL
);

INSERT INTO [Users] ([UserId], [Password], [FirstName], [LastName], [Email]) VALUES (
    'RJJ',
    'dd8d27869a119250722d213a5c1572b411f18d136e6f8587de6cf99045ca4d1e',  -- "RJJ"
    'Ricardo',
    'Jesus',
    'ricardojesus@ua.pt'
);
