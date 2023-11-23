-- Triggers
UPDATE Users SET user_status = 'FLAGGED' WHERE user_id = 1;
SELECT * FROM Blogs WHERE user_id = 1;

UPDATE Blogs SET blog_status = 'OPEN' WHERE user_id = 1;
UPDATE Users SET user_status = 'OK' WHERE user_id = 1;

UPDATE Blogs SET blog_status = 'CLOSED' where user_id = 2;

INSERT INTO Comments (user_id, post_id, content)
SELECT 1, 1, 'Comment ' || generate_series(1, 499);