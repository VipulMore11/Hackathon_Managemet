# API Endpoints

## User Registration
- **URL**: `/signup`
- **Method**: `POST`
- **Description**: Registers a new user.

---

## User Login
- **URL**: `/login`
- **Method**: `POST`
- **Description**: Authenticates a user and provides an access token.

---

## Admin User Management
- **URL**: `/admin`
- **Method**: `GET`
- **Description**: Fetches all users. Only accessible by Admin users.

---

## Submit Feedback
- **URL**: `/feedback`
- **Method**: `POST`
- **Description**: Submits user feedback.

---

## Get All Feedbacks
- **URL**: `/get_feedback`
- **Method**: `GET`
- **Description**: Retrieves all feedbacks.

---

## Get Specific Feedback
- **URL**: `/get_feedback/<id>`
- **Method**: `GET`
- **Description**: Retrieves feedback by its ID.

---

## Update Team Status
- **URL**: `/update_team_status/<teamno>`
- **Method**: `PUT`
- **Description**: Updates the status of a specific team.

---

## Get All Teams
- **URL**: `/get_all_teams`
- **Method**: `GET`
- **Description**: Retrieves a list of all teams with their details.

---

## Get Specific Team
- **URL**: `/get_team/<teamno>`
- **Method**: `GET`
- **Description**: Retrieves details of a specific team by team number.

---

## Get All Mentors
- **URL**: `/mentors`
- **Method**: `GET`
- **Description**: Retrieves a list of all mentors and their assigned teams.

---

## Create Mentor
- **URL**: `/mentors`
- **Method**: `POST`
- **Description**: Creates a new mentor.

---

## Assign Teams to Mentor
- **URL**: `/update_mentors/<mentor_id>`
- **Method**: `PUT`
- **Description**: Assigns teams to a specific mentor.

---

## Create Team
- **URL**: `/create_team`
- **Method**: `POST`
- **Description**: Creates a new team and its members.
