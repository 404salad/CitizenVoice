-- Users (Remember to replace with strong, unique passwords):
INSERT INTO User (UserId, FirstName, LastName, Email, PasswordHash)
VALUES ('user123', 'Rahul', 'Sharma', 'user123@mycompany.com', 'pass123');
INSERT INTO User (UserId, FirstName, LastName, Email, PasswordHash)
VALUES ('user456', 'Priya', 'Desai', 'user456@mycompany.com', 'pass456');
INSERT INTO User (UserId, FirstName, LastName, Email, PasswordHash)
VALUES ('admin', 'System', 'Admin', 'admin@mycompany.com', 'pass');
INSERT INTO User (UserId, FirstName, LastName, Email, PasswordHash)
VALUES ('manager1', 'Vikram', 'Singh', 'manager1@mycompany.com', 'pass1');
INSERT INTO User (UserId, FirstName, LastName, Email, PasswordHash)
VALUES ('hr_rep', 'Aisha', 'Kapoor', 'hr_rep@mycompany.com', 'pass');

-- Departments
INSERT INTO Department (DepartmentId, StateId)
VALUES ('PW', 1); -- Public Works Department
INSERT INTO Department (DepartmentId, StateId)
VALUES ('UD', 2); -- Urban Development Department
INSERT INTO Department (DepartmentId, StateId)
VALUES ('Mktg', 3); -- Marketing Department
INSERT INTO Department (DepartmentId, StateId)
VALUES ('Fin', 1); -- Finance Department
INSERT INTO Department (DepartmentId, StateId)
VALUES ('Sales', 2); -- Sales Department

-- States
INSERT INTO State (StateId, StateName)
VALUES (1, 'Gujarat');
INSERT INTO State (StateId, StateName)
VALUES (2, 'Maharashtra');
INSERT INTO State (StateId, StateName)
VALUES (3, 'Karnataka');
INSERT INTO State (StateId, StateName)
VALUES (4, 'Delhi');
INSERT INTO State (StateId, StateName)
VALUES (5, 'Tamil Nadu');

-- Grievances (Indian-specific categories)
INSERT INTO Grievance (GrievanceId,DepartmentId, UserId, Category, Description, Status, DateSubmitted, DateResolved)
VALUES (1, 'PW', 'user123', 'Water Shortage', 'Requesting immediate water supply restoration in my area', 'Open', '2024-04-01', NULL);
INSERT INTO Grievance (GrievanceId,DepartmentId, UserId, Category, Description, Status, DateSubmitted, DateResolved)
VALUES (2, 'UD', 'user456',     'Pothole Repair', 'Large pothole on main road causing traffic congestion', 'Pending', '2024-03-25', NULL);

-- Comments
INSERT INTO Comment (CommentId, GrievanceId, UserId, Comment, DateCommented)
VALUES (1, 1, 'admin', 'Water tanker dispatched to your area. Expect supply within 2 hours', '2024-04-02');
INSERT INTO Comment (CommentId, GrievanceId, UserId, Comment, DateCommented)
VALUES (2, 2, 'user456', 'Images attached for reference', '2024-03-02');
