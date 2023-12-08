CREATE TABLE Users (
  user_id     INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  username    VARCHAR(30)  NOT NULL UNIQUE
                           CONSTRAINT UsernameMinLength
                           CHECK(LENGTH(username) >= 5),
  email       VARCHAR(500) NOT NULL UNIQUE,
  first_name  VARCHAR(30),
  last_name   VARCHAR(30),
  user_status VARCHAR(30)  CONSTRAINT UserStatus
                           CHECK(user_status IN ('OK', 'CLOSED', 'FLAGGED'))
                           DEFAULT 'OK',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Blogs (
  blog_id          INTEGER       PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  blog_name        VARCHAR(100)  NOT NULL UNIQUE,
  blog_description VARCHAR(500),
  blog_status      VARCHAR(30)   CONSTRAINT BlogStatus
                                 CHECK(blog_status IN ('OPEN', 'CLOSED', 'HIDDEN')) 
                                 DEFAULT 'OPEN',
  created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  closed_at        TIMESTAMP,
  user_id          INTEGER       NOT NULL

  CONSTRAINT CloseTimestampRequired
  CHECK(blog_status = 'OPEN' OR closed_at IS NOT NULL)
);
-- when blog is CLOSED no one can see it.
-- HIDDEN means that blog that was previously OPEN was closed by system or administration
-- (User got FLAGGED or CLOSED)
-- HIDDEN becomes OPEN when User is OK

CREATE TABLE Posts (
  post_id    INTEGER      PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  title      VARCHAR(100) NOT NULL,
  content    VARCHAR      NOT NULL,
  created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  blog_id    INTEGER      NOT NULL
);

CREATE TABLE Reactions (
  user_id    INTEGER,
  post_id    INTEGER,
  likes      BOOLEAN NOT NULL DEFAULT TRUE,
  reacted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY(user_id, post_id)
);

CREATE TABLE Comments (
  comment_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  content    VARCHAR NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  user_id    INTEGER   NOT NULL,
  post_id    INTEGER   NOT NULL
);

CREATE INDEX idx_blogs_user_id ON Blogs(user_id);
CREATE INDEX idx_posts_blog_id ON Posts(blog_id);
CREATE INDEX idx_comments_post_id ON Comments(post_id);
CREATE INDEX idx_comments_user_id ON Comments(user_id);

ALTER TABLE Blogs
  ADD CONSTRAINT IUser
  FOREIGN KEY(user_id)
  REFERENCES Users ON DELETE RESTRICT
                   ON UPDATE CASCADE;

ALTER TABLE Posts
  ADD CONSTRAINT IBlog
  FOREIGN KEY(blog_id)
  REFERENCES Blogs ON DELETE RESTRICT
                   ON UPDATE CASCADE;

ALTER TABLE Reactions
  ADD CONSTRAINT IUser
  FOREIGN KEY(user_id)
  REFERENCES Users ON DELETE CASCADE
                   ON UPDATE CASCADE;

ALTER TABLE Reactions
  ADD CONSTRAINT IPost
  FOREIGN KEY(post_id)
  REFERENCES Posts ON DELETE CASCADE
                   ON UPDATE CASCADE;

ALTER TABLE Comments
  ADD CONSTRAINT IUser
  FOREIGN KEY(user_id)
  REFERENCES Users ON DELETE CASCADE
                   ON UPDATE CASCADE;

ALTER TABLE Comments
  ADD CONSTRAINT IPost
  FOREIGN KEY(post_id)
  REFERENCES Posts ON DELETE CASCADE
                   ON UPDATE CASCADE;

CREATE FUNCTION FUpdateBlogStatus()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.user_status <> 'OK' THEN
    UPDATE Blogs SET blog_status = 'HIDDEN'
    WHERE user_id = NEW.user_id AND blog_status = 'OPEN';
  ELSE
    UPDATE Blogs SET blog_status = 'OPEN'
    WHERE user_id = NEW.user_id AND blog_status = 'HIDDEN';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TUpdateBlogStatus
AFTER UPDATE ON Users
FOR EACH ROW
WHEN (OLD.user_status <> NEW.user_status)
EXECUTE PROCEDURE FUpdateBlogStatus();

CREATE FUNCTION FValidateBlogStatus()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.blog_status = 'OPEN' AND
     (SELECT user_status FROM Users WHERE user_id = NEW.user_id) <> 'OK' THEN
     RAISE EXCEPTION 'Blog cannot be OPEN if User is not OK';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TValidateBlogStatus
BEFORE INSERT OR UPDATE ON Blogs
FOR EACH ROW
WHEN (NEW.blog_status = 'OPEN')
EXECUTE PROCEDURE FValidateBlogStatus();

CREATE FUNCTION FUpdateBlogCloseTimestamp()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.blog_status <> 'OPEN' THEN
    NEW.closed_at = CURRENT_TIMESTAMP;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TUpdateBlogCloseTimestamp
BEFORE UPDATE ON Blogs
FOR EACH ROW
WHEN (NEW.blog_status <> 'OPEN')
EXECUTE PROCEDURE FUpdateBlogCloseTimestamp();

CREATE FUNCTION FValidateCommentCount()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT COUNT(*) FROM Comments WHERE post_id = NEW.post_id) >= 500 THEN
    RAISE EXCEPTION 'Post comment limit exceeded';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TValidateCommentCount
BEFORE INSERT ON Comments
FOR EACH ROW
EXECUTE PROCEDURE FValidateCommentCount();

CREATE MATERIALIZED VIEW UsersStats (
  user_id,
  username,
  email,
  first_name,
  last_name,
  user_status,
  created_at,
  blog_count,
  post_count,
  received_comment_count)
AS SELECT Users.user_id,
          username,
          email,
          first_name,
          last_name,
          user_status,
          Users.created_at,
          COUNT(DISTINCT Blogs.blog_id),
          COUNT(DISTINCT Posts.post_id),
          COUNT(DISTINCT Comments.comment_id)
FROM Users
LEFT JOIN Blogs ON Users.user_id = Blogs.user_id
LEFT JOIN Posts ON Posts.blog_id = Blogs.blog_id
LEFT JOIN Comments ON Posts.post_id = Comments.post_id
GROUP BY Users.user_id;

CREATE VIEW FlaggedPosts (
  post_id,
  title,
  content,
  created_at,
  blog_id
)
AS SELECT p.post_id,
          p.title,
          p.content,
          p.created_at,
          p.blog_id
FROM Posts p
JOIN Blogs ON p.blog_id = Blogs.blog_id
JOIN Users ON Blogs.user_id = Users.user_id
WHERE Users.user_status = 'FLAGGED';

CREATE VIEW PostsInfo (
  post_id,
  title,
  content,
  created_at,
  blog_id,
  reaction_count,
  comment_count
)
AS SELECT p.post_id,
          p.title,
          p.content,
          p.created_at,
          p.blog_id,
          COUNT(DISTINCT Reactions.user_id),
          COUNT(DISTINCT Comments.comment_id)
FROM Posts p
LEFT JOIN Reactions ON Reactions.post_id = p.post_id
LEFT JOIN Comments ON Comments.post_id = p.post_id
GROUP BY p.post_id;
