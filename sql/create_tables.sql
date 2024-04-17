CREATE TABLE state (
  StateId INT PRIMARY KEY,
  StateName VARCHAR(255)
);


CREATE TABLE user (
  UserId VARCHAR(255) PRIMARY KEY,
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Email VARCHAR(255) UNIQUE,
  PasswordHash VARCHAR(255) NOT NULL
);

CREATE TABLE department (
  DepartmentId VARCHAR(255) PRIMARY KEY,
  StateId INT REFERENCES state(StateId)
);


CREATE TABLE grievance (
  GrievanceId INT PRIMARY KEY,
  StateId INT REFERENCES state(StateId),
  DepartmentId VARCHAR(255) REFERENCES department(DepartmentId),
  UserId VARCHAR(255),
  Category VARCHAR(255),
  Description VARCHAR(255),
  Status VARCHAR(255),
  DateSubmitted DATE,
  DateResolved DATE
);

CREATE TABLE comment (
  CommentId INT PRIMARY KEY,
  GrievanceId INT REFERENCES grievance(GrievanceId),
  UserId VARCHAR(255) REFERENCES user(UserId),
  Comment VARCHAR(255),
  DateCommented DATE
);

CREATE TABLE attachment (
  AttachmentId INT PRIMARY KEY,
  GrievanceId INT REFERENCES grievance(GrievanceId),
  Username VARCHAR(255),
  PhoneNo INT,
  DateAttached VARCHAR(255),
  Email VARCHAR(255),
  FileName VARCHAR(255),
  FilePath VARCHAR(255)
);
