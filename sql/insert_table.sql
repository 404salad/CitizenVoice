-- states
insert into state (stateid, statename)
values (1, 'gujarat');
insert into state (stateid, statename)
values (2, 'maharashtra');
insert into state (stateid, statename)
values (3, 'karnataka');
insert into state (stateid, statename)
values (4, 'delhi');
insert into state (stateid, statename)
values (5, 'tamil nadu');

-- users (remember to replace with strong, unique passwords):
insert into user (userid, firstname, lastname, email, passwordhash)
values ('user123', 'rahul', 'sharma', 'user123@mycompany.com', 'pass123');
insert into user (userid, firstname, lastname, email, passwordhash)
values ('user456', 'priya', 'desai', 'user456@mycompany.com', 'pass456');
insert into user (userid, firstname, lastname, email, passwordhash)
values ('admin', 'system', 'admin', 'admin@mycompany.com', 'pass');
insert into user (userid, firstname, lastname, email, passwordhash)
values ('manager1', 'vikram', 'singh', 'manager1@mycompany.com', 'pass1');
insert into user (userid, firstname, lastname, email, passwordhash)
values ('hr_rep', 'aisha', 'kapoor', 'hr_rep@mycompany.com', 'pass');


-- departments
insert into department (departmentid, stateid)
values ('pw', 1); -- public works department
insert into department (departmentid, stateid)
values ('ud', 2); -- urban development department
insert into department (departmentid, stateid)
values ('mktg', 3); -- marketing department
insert into department (departmentid, stateid)
values ('fin', 1); -- finance department
insert into department (departmentid, stateid)
values ('sales', 2); -- sales department


-- grievances (indian-specific categories)

insert into grievance (grievanceid, stateid, departmentid, userid, category, description, status, datesubmitted, dateresolved)
values (26, 2,'pw', 'user123', 'water shortage', 'requesting immediate water supply restoration in my area', 'pending', '2024-04-01', null);
insert into grievance (grievanceid, stateid, departmentid, userid, category, description, status, datesubmitted, dateresolved)
values (27, 3,'ud', 'user456',     'pothole repair', 'large pothole on main road causing traffic congestion', 'pending', '2024-03-25', null);
insert into grievance (grievanceid, stateid, departmentid, userid, category, description, status, datesubmitted, dateresolved)
values (29, 2,'pw', 'user123', 'water shortage', 'need immediate water supply in my area', 'pending', '2024-02-01', null);

-- comments
insert into comment (commentid, grievanceid, userid, comment, datecommented)
values (1, 1, 'admin', 'water tanker dispatched to your area. expect supply within 2 hours', '2024-04-02');
insert into comment (commentid, grievanceid, userid, comment, datecommented)
values (2, 2, 'user456', 'images attached for reference', '2024-03-02');
