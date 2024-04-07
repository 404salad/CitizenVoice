CREATE TABLE State (
  StateId INT PRIMARY KEY,
  StateName VARCHAR(255)
);


CREATE TABLE Department (
  DepartmentId VARCHAR(255) PRIMARY KEY,
  StateId INT REFERENCES State(StateId)
);

CREATE TABLE User (
  UserId VARCHAR(255) PRIMARY KEY,
  FirstName VARCHAR(255),
  LastName VARCHAR(255),
  Email VARCHAR(255) UNIQUE,
  PasswordHash VARCHAR(255) NOT NULL
);


CREATE TABLE Grievance (
  GrievanceId INT PRIMARY KEY,
  StateId INT REFERENCES State(StateId),
  DepartmentId VARCHAR(255) REFERENCES Department(DepartmentId),
  UserId VARCHAR(255),
  Category VARCHAR(255),
  Description VARCHAR(255),
  Status VARCHAR(255),
  DateSubmitted DATE,
  DateResolved DATE
);

CREATE TABLE Comment (
  CommentId INT PRIMARY KEY,
  GrievanceId INT REFERENCES Grievance(GrievanceId),
  UserId VARCHAR(255) REFERENCES User(UserId),
  Comment VARCHAR(255),
  DateCommented DATE
);

CREATE TABLE Attachment (
  AttachmentId INT PRIMARY KEY,
  GrievanceId INT REFERENCES Grievance(GrievanceId),
  Username VARCHAR(255),
  PhoneNo INT,
  DateAttached VARCHAR(255),
  Email VARCHAR(255),
  FileName VARCHAR(255),
  FilePath VARCHAR(255)
);
