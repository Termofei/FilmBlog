# 🎬 FilmBlog

**FilmBlog** is a full-stack web application that allows users to **discover, review, and discuss the latest films**.  
Built with Django, it offers a clean interface and a smooth user experience for movie enthusiasts to share opinions and discover new favorites.

---

## 🌟 Features

- 🧭 **Browse Movies** – Explore the newest films with full details (title, description, director, and cast).  
- ✍️ **Write Reviews** – Create and publish your own movie reviews.  
- 🛠 **Manage Reviews** – Edit or delete your reviews anytime.  
- 💬 **Community** – Read and engage with reviews from other users.  
- 🎨 **Clean UI** – Simple, modern, and responsive interface.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3, Bootstrap |
| **Database** | SQLite (Development) |
| **Authentication** | Django Allauth |

---

## Setup for New Users

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Load sample movies: `python manage.py loaddata movies_fixture.json`
5. Start server: `python manage.py runserver`
