# Business Requirements Document (BRD)

## ✨ Project Name
**WhatsApp Job Board Bot**

---

## 🎯 Objective
To build an automated WhatsApp chatbot that connects **job seekers** with **employers**, enabling:
- Job seekers to register interests (role/location)
- Employers to post available roles
- The bot to match and send job alerts via WhatsApp

---

## 🤩 Scope

### ✅ In Scope
- WhatsApp Bot via **Twilio Sandbox**
- Command-based interactions:
  - `register <role> <location>`
  - `post <role> <location>`
- Basic match-making logic
- Real-time job notifications
- Python + Flask server backend

### ❌ Out of Scope (for MVP)
- Authentication system
- Payment integration
- Web dashboard
- AI/NLP natural language processing

---

## 👤 Target Users

| User Type     | Goal                                           |
|---------------|------------------------------------------------|
| Job Seeker    | Receive job listings that match skills/location |
| Employer      | Post jobs and reach interested workers instantly |

---

## 📲 Functional Requirements

### 1. User Registration
- Command: `register <role> <location>`
- Store user’s preferred role and location

### 2. Post a Job
- Command: `post <role> <location>`
- Stores job info and alerts matching users

### 3. Message Handling
- Bot receives incoming messages from Twilio
- Uses webhooks (Flask) to reply dynamically

### 4. Job Matching & Alert
- If a new job matches a user’s role + location
- Send them a WhatsApp message with job details

---

## 🔒 Non-Functional Requirements

| Requirement     | Description                                |
|-----------------|--------------------------------------------|
| Scalability     | Should support at least 100 users initially |
| Security        | No personal data stored beyond role/location |
| Performance     | Alerts should be sent within 5 seconds of posting |

---

## 🧰 Tech Stack

| Component         | Tool/Service               |
|-------------------|----------------------------|
| WhatsApp API      | Twilio Sandbox (testing)   |
| Backend           | Python + Flask             |
| Deployment        | Local (for now) via ngrok  |
| Hosting (Later)   | Render, Vercel, or Heroku  |
| Database (Later)  | Firebase or Supabase       |

---

## 🔁 Future Features (Post-MVP)
- Admin interface for posting
- Category filters
- AI-based matching
- Subscription-based access
- Analytics dashboard
- Voice command integration

---

## ✅ MVP Completion Criteria
- User can register
- Employer can post
- Matching users receive a real WhatsApp alert
- No manual intervention required
