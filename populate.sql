INSERT INTO Users (username, email, first_name, last_name, user_status)
VALUES
  ('johnd', 'john.doe@example.com', 'John', 'Doe', 'OK'),
  ('janes', 'smith_jane@example.com', 'Jane', 'Smith', 'OK'),
  ('alice', 'aalice@yourdomain.org', 'Alice', 'Johnson', 'OK'),
  ('anderson', 'anderson.mike@example.com', 'Mike', 'Anderson', 'OK');

INSERT INTO Blogs (blog_name, blog_description, user_id)
VALUES
  ('Tech Blog', 'Exploring the latest in technology', 1),
  ('Travel Adventures', 'Journey around the world', 2),
  ('Foodie Delights', 'Discovering culinary delights', 3),
  ('My random blog', NULL, 4);


INSERT INTO Posts (title, content, blog_id)
VALUES
  ('Latest Tech Trends', 'Exploring the world of technology', 1),
  ('The Rise of Artificial Intelligence', 'Exploring the impact of AI on technology', 1),
  ('Web Development Trends 2023', 'Key trends shaping the future of web development', 1),
  ('Around Europe in 30 Days', 'A travel diary of European adventures', 2),
  ('Delicious Desserts', 'Indulging in sweet treats', 3),
  ('The Art of Sushi Making', 'A step-by-step guide to crafting delicious sushi', 3);

INSERT INTO Reactions (user_id, post_id, likes)
VALUES
  (1, 1, TRUE),
  (2, 1, FALSE),
  (2, 2, TRUE),
  (3, 2, TRUE),
  (4, 2, TRUE),
  (1, 3, TRUE),
  (2, 3, FALSE),
  (3, 4, TRUE),
  (1, 4, TRUE),
  (2, 4, FALSE);

INSERT INTO Comments (content, user_id, post_id)
VALUES
  ('Great post!', 1, 1),
  ('I totally agree!', 2, 1),
  ('Looking forward to your next adventure', 1, 4),
  ('Fascinating topic!', 3, 1),
  ('Love the outdoor tips!', 4, 4),
  ('Thanks for the nutrition advice', 4, 5),
  ('Looking forward to more posts like this', 1, 4),
  ('I enjoyed reading this', 2, 3),
  ('Keep up the good work!', 3, 2),
  ('Interesting perspective', 4, 2),
  ('Can''t wait for your next adventure', 3, 4);

REFRESH MATERIALIZED VIEW UsersStats;
