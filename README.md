# World Cup Seat Booking DevOps Project

<div dir="rtl">

## תיאור קצר של הפרויקט

זהו פרויקט גמר ב-DevOps שמבוסס על אפליקציית Flask פשוטה עם מסד נתונים MySQL.

האפליקציה היא מערכת דמו להזמנת מושבים למשחקי כדורגל בסגנון World Cup. משתמשים יכולים לראות משחקים, לבחור סוג מושב, ליצור הזמנה, לקבל קוד הזמנה, לנהל הזמנה קיימת לפי קוד הזמנה ואימייל, וגם לבטל הזמנה.

המטרה המרכזית של הפרויקט היא לא לבנות מערכת כרטיסים גדולה ומורכבת, אלא להדגים תהליך DevOps מלא סביב אפליקציה פשוטה וברורה.

## תכונות האפליקציה

- עמוד בית עם כרטיסי משחקים.
- עמוד פרטי משחק.
- הצגת סוגי מושבים ומספר מושבים זמינים.
- יצירת הזמנה חדשה.
- עמוד הצלחת הזמנה עם קוד הזמנה.
- ניהול הזמנה לפי קוד הזמנה ואימייל.
- ביטול הזמנה באמצעות soft delete על ידי `is_cancelled=True`.
- התחברות מנהל בסיסית.
- עמוד מנהל שמציג הזמנות וסטטיסטיקות משחקים.
- עמוד הסבר `/about`.
- נקודת בריאות `/health`.

## ארכיטקטורת הפרויקט

זרימת האפליקציה:

```text
Browser/User -> Flask -> SQLAlchemy -> MySQL
```

הסבר פשוט:

- המשתמש נכנס לאפליקציה דרך הדפדפן.
- Flask מקבל את הבקשה ומחזיר עמוד HTML או תשובת JSON.
- SQLAlchemy משמש כ-ORM ומאפשר לעבוד עם טבלאות בצורה של מחלקות Python.
- MySQL שומר את הנתונים של האצטדיונים, המשחקים, סוגי המושבים וההזמנות.

זרימת DevOps עתידית/נוכחית:

```text
Developer -> GitHub -> GitHub Actions -> Pytest -> Docker Build -> Docker Hub -> Deployment
```

## טכנולוגיות מרכזיות

- `Python` - שפת התכנות של האפליקציה.
- `Flask` - framework פשוט לבניית אפליקציות web.
- `SQLAlchemy` - כלי ORM שמחבר בין קוד Python למסד הנתונים.
- `MySQL` - מסד הנתונים של האפליקציה בזמן ריצה רגילה.
- `HTML templates` - עמודי HTML שנמצאים בתיקיית `templates`.
- `CSS static files` - עיצוב האפליקציה דרך קבצים בתיקיית `static`.
- `Docker` - בניית image לאפליקציית Flask.
- `Docker Compose` - הרצת Flask ו-MySQL ביחד בסביבה מקומית.
- `GitHub Actions` - הרצת בדיקות, בניית Docker image ושליחה ל-Docker Hub.
- `Pytest` - בדיקות אוטומטיות.
- `Docker Hub` - אחסון ה-Docker image.
- `Environment Variables` - הגדרות כמו סיסמאות ושמות משתמשים בלי להכניס סודות לקוד.
- `SQLite in testing mode` - מסד נתונים זמני ומהיר לבדיקות בלבד.

## מבנה תיקיות וקבצים

### `app.py`

הקובץ המרכזי של Flask. הוא כולל:

- יצירת האפליקציה.
- הגדרת חיבור למסד נתונים.
- מודלים של SQLAlchemy.
- routes של עמודים ציבוריים.
- routes של הזמנות.
- routes של מנהל.
- יצירת נתוני דמו אם מסד הנתונים ריק.

### `requirements.txt`

רשימת ספריות Python שהפרויקט צריך, כמו Flask, SQLAlchemy, PyMySQL ו-pytest.

### `Dockerfile`

מגדיר איך לבנות Docker image לאפליקציית Flask.

### `docker-compose.yml`

קובץ להרצה מקומית של האפליקציה יחד עם MySQL.

האפליקציה נפתחת על:

```text
http://localhost:5001
```

MySQL רץ בתוך ה-container על פורט `3306`, אבל במחשב המקומי הוא ממופה ל-`3307` כדי לא להתנגש עם MySQL מקומי של Windows.

### `docker-compose.prod.yml`

קובץ בסגנון production שמריץ את ה-image שכבר נשלח ל-Docker Hub יחד עם MySQL.

### `.env.example`

קובץ דוגמה בטוח למשתני סביבה. הוא כן נשמר ב-Git כי אין בו סודות אמיתיים.

### `.gitignore`

מונע העלאה של קבצים מקומיים או רגישים כמו `.env`, סביבות וירטואליות, קבצי cache וקבצי מערכת.

### `.github/workflows/ci.yml`

קובץ GitHub Actions שמריץ את תהליך ה-CI/CD.

### `templates/`

תיקיית עמודי HTML:

- `base.html` - תבנית בסיסית וניווט.
- `index.html` - עמוד הבית עם המשחקים.
- `match_detail.html` - עמוד פרטי משחק וטופס הזמנה.
- `booking_success.html` - עמוד פרטי הזמנה.
- `manage_booking.html` - ניהול הזמנה לפי קוד ואימייל.
- `admin_login.html` - התחברות מנהל.
- `admin_bookings.html` - צפייה בהזמנות וסטטיסטיקות.
- `about.html` - הסבר על הפרויקט.

### `static/`

קבצי עיצוב ותמונות:

- `static/css/main.css`
- `static/images/stadium-background.jpg`

### `tests/`

בדיקות pytest. כרגע יש בדיקות ל-health, עמוד הבית, עמוד משחק, ניהול הזמנה, ביטול הזמנה, עמוד about ועמוד מנהל.

### `db/mysqld.cnf`

קובץ הגדרות בסיסי ל-MySQL container.

## מבנה מסד הנתונים

הפרויקט משתמש בארבע טבלאות מרכזיות במקום טבלה אחת גדולה, כדי לשמור על סדר ולמנוע כפילויות.

### `stadiums`

שומרת מידע על אצטדיונים.

עמודות חשובות:

- `id`
- `name`
- `city`
- `capacity`

קשר:

- אצטדיון אחד יכול להכיל הרבה משחקים.

### `matches`

שומרת מידע על משחקים.

עמודות חשובות:

- `id`
- `home_team`
- `away_team`
- `match_date`
- `stadium_id`

קשר:

- כל משחק שייך לאצטדיון אחד.
- לכל משחק יכולים להיות כמה סוגי מושבים.
- לכל משחק יכולות להיות הרבה הזמנות.

### `seat_types`

שומרת סוגי מושבים לכל משחק.

עמודות חשובות:

- `id`
- `name`
- `price`
- `total_seats`
- `match_id`

קשר:

- כל סוג מושב שייך למשחק אחד.
- לדוגמה: Regular, Premium, VIP.

### `bookings`

שומרת הזמנות של משתמשים.

עמודות חשובות:

- `id`
- `booking_code`
- `customer_name`
- `customer_email`
- `seats_count`
- `is_cancelled`
- `created_at`
- `match_id`
- `seat_type_id`

קשר:

- כל הזמנה שייכת למשחק אחד.
- כל הזמנה שייכת לסוג מושב אחד.

## למה ארבע טבלאות ולא טבלה אחת?

אם כל המידע היה בטבלה אחת, היו הרבה כפילויות: שם אצטדיון, שם משחק, מחיר מושב וכדומה.

חלוקה לטבלאות מאפשרת:

- קוד מסודר יותר.
- קשרים ברורים בין נתונים.
- פחות כפילויות.
- הסבר טוב יותר בארכיטקטורה.
- בסיס נכון יותר לאפליקציה אמיתית.

## זרימת הזמנה

1. המשתמש פותח את עמוד הבית.
2. המשתמש בוחר משחק.
3. המשתמש רואה את פרטי המשחק, האצטדיון וסוגי המושבים.
4. המשתמש בוחר סוג מושב ומספר מושבים.
5. האפליקציה בודקת שיש מספיק מושבים זמינים.
6. אם הכל תקין, נוצרת שורת `Booking` במסד הנתונים.
7. המשתמש מקבל `booking_code`.
8. המשתמש יכול לנהל את ההזמנה בעזרת `booking_code` ו-`customer_email`.
9. המשתמש יכול לבטל הזמנה.
10. הזמנה מבוטלת לא נמחקת מהמסד, אלא מקבלת `is_cancelled=True`.

## לוגיקת מושבים זמינים

החישוב הוא:

```text
available seats = total seats - active booked seats
```

כאשר:

```text
active booked seats = bookings where is_cancelled == False
```

הזמנות מבוטלות נשארות במסד הנתונים, אבל לא נחשבות כמושבים תפוסים.

## משתני סביבה

הפרויקט משתמש במשתני סביבה כדי לא להכניס סודות לקוד.

קובץ `.env.example` נשמר ב-Git כדוגמה בטוחה:

```env
APP_ENV=development
IMAGE_TAG=latest
SESSION_COOKIE_SECURE=false
ADMIN_PASSWORD=replace-with-a-strong-admin-password
SECRET_KEY=replace-with-a-long-random-secret-key
DB_USER=flask
DB_PASSWORD=change-me
DB_NAME=flask
MYSQL_ROOT_PASSWORD=change-root-password
```

For an HTTP demo server, use:

```env
SESSION_COOKIE_SECURE=false
```

For real HTTPS production, use:

```env
SESSION_COOKIE_SECURE=true
```

קובץ `.env` הוא קובץ מקומי בלבד והוא לא נשמר ב-Git.

הסבר משתנים:

- `ADMIN_PASSWORD` - סיסמת מנהל.
- `SECRET_KEY` - מפתח session של Flask.
- `IMAGE_TAG` - Docker image tag used by `docker-compose.prod.yml`; default is `latest`.
- `SESSION_COOKIE_SECURE` - set to `false` for plain HTTP demo servers and `true` for real HTTPS production.
- `DB_USER` - משתמש MySQL.
- `DB_PASSWORD` - סיסמת MySQL.
- `DB_NAME` - שם מסד הנתונים.
- `MYSQL_ROOT_PASSWORD` - סיסמת root של MySQL.

חשוב: סיסמאות אמיתיות לא שומרים ב-GitHub. בסביבה אמיתית משתמשים ב-`.env` מקומי או ב-GitHub Secrets.

## בדיקות

GitHub Actions מריץ `pytest` בכל push ל-`main`.

במצב רגיל עם Docker, האפליקציה משתמשת ב-MySQL.

במצב בדיקות:

```text
TESTING=true
```

האפליקציה משתמשת ב-SQLite בזיכרון:

```text
sqlite:///:memory:
```

SQLite משמש רק לבדיקות מהירות ומבודדות, כדי שלא יהיה צורך להריץ MySQL בתוך GitHub Actions בזמן pytest.

נבדקים בין היתר:

- `/health`
- עמוד הבית.
- עמוד פרטי משחק.
- עמוד ניהול הזמנה.
- עמוד פרטי הזמנה.
- ביטול הזמנה.
- עמוד about.
- עמוד מנהל אחרי התחברות session בבדיקה.

## Docker ו-Docker Compose

`Dockerfile` בונה image לאפליקציית Flask.

`docker-compose.yml` מריץ מקומית:

- Flask app
- MySQL

`docker-compose.prod.yml` מריץ את ה-image שכבר פורסם ל-Docker Hub:

```text
shlomodevops/devops-final-projectshlomo
```

### Production Image Versioning

Docker image tags are labels for Docker images in Docker Hub. They let the server choose which version of the application to run.

This project pushes images to:

```text
shlomodevops/devops-final-projectshlomo
```

Each successful build from `main` creates two tags:

- `latest` - a moving tag that points to the newest image built from `main`.
- a 7-character commit SHA tag, for example `abc1234` - a fixed tag that points to the image built from one exact Git commit.

Using the commit SHA tag is safer than relying only on `latest` because it makes production predictable. `latest` can change every time a new build is pushed, but a commit SHA tag keeps pointing to the same image. This makes deployments easier to audit and rollbacks much clearer.

The production Compose file uses `IMAGE_TAG`:

```text
image: shlomodevops/devops-final-projectshlomo:${IMAGE_TAG:-latest}
```

If `IMAGE_TAG` is missing, Docker Compose falls back to `latest`. During automated deployment, GitHub Actions updates the EC2 `.env` file to use the exact short SHA tag that was just built.

### Rollback Procedure

Rollback means running a previous working Docker image instead of the newest one.

1. Choose a previous working Docker image tag from Docker Hub or Git history.
2. SSH into the EC2 server.
3. Edit `.env` and set `IMAGE_TAG` to the previous tag:

```env
IMAGE_TAG=abc1234
```

4. Pull and restart the production stack:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
curl http://localhost/health
```

Use the real previous tag instead of `abc1234`.

### How to verify what version is running

On the EC2 server, check the tag selected in `.env`:

```bash
grep IMAGE_TAG .env
```

Then check the image used by the running Flask container:

```bash
docker inspect flask_app_prod --format='{{.Config.Image}}'
```

MySQL בתוך ה-container משתמש בפורט `3306`.

במחשב המקומי הפורט ממופה ל-`3307`, כדי למנוע התנגשות עם MySQL מקומי שכבר משתמש ב-`3306`.

## CI/CD Pipeline

### CI/CD Flow

```text
Developer -> GitHub -> GitHub Actions -> Tests -> Docker Build -> Docker Hub -> EC2 -> Docker Compose -> Health Check
```

On every push to `main`, GitHub Actions runs the CI/CD workflow:

1. Checks out the code.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Runs tests with `pytest`.
5. Builds the Docker image.
6. Logs in to Docker Hub using GitHub Secrets.
7. Pushes two Docker image tags:
   - `latest`
   - the 7-character short commit SHA tag
8. Connects to the EC2 server over SSH.
9. Runs `git pull origin main` in `~/seat-booking-devops`.
10. Updates the EC2 `.env` file with:

```env
IMAGE_TAG=<short-sha>
```

11. Pulls and starts the production Docker Compose stack:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

12. Verifies the deployment with:

```text
http://localhost/health
```

התחברות ל-Docker Hub נעשית עם GitHub Secrets:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

### Automated EC2 deployment

GitHub Actions builds the Flask Docker image and pushes it to Docker Hub after the tests pass.
After the Docker image is pushed successfully, the deploy job connects to the EC2 server over SSH using these GitHub repository secrets:

- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`

On EC2, the deployment runs from `~/seat-booking-devops`, pulls the latest `main` branch, updates `IMAGE_TAG` in the server `.env` file, pulls the selected Docker images from Docker Hub, and restarts the production Docker Compose stack.
Docker Compose restarts Nginx, Gunicorn/Flask, MySQL, Prometheus, and Grafana, then the workflow checks `http://localhost/health`.

The server `.env` file stays only on EC2. It is not committed to Git and should not be copied into GitHub Actions.

## איך להריץ מקומית

קודם יוצרים קובץ `.env` מתוך הדוגמה:

```powershell
Copy-Item .env.example .env
```

אחר כך מריצים:

```powershell
docker compose up --build
```

פותחים בדפדפן:

```text
http://localhost:5001
```

בדיקת health:

```powershell
curl http://localhost:5001/health
```

עמוד התחברות מנהל:

```text
http://localhost:5001/admin/login
```

## Nginx reverse proxy

The Docker Compose setup now includes Nginx in front of the Flask app.

Nginx is the external reverse proxy. Gunicorn is the WSGI server that runs the Flask app inside the application container. Flask contains the application routes and business logic.

Request flow:

```text
User -> Nginx -> Gunicorn -> Flask -> SQLAlchemy -> MySQL
```

Nginx listens on port 80 and forwards requests to the Flask service at `app:5000`.
The Flask container listens internally on port `5000` through Gunicorn, so production containers do not use Flask's development server and the `This is a development server` warning is removed from the production runtime.
The Flask app is still available on `http://localhost:5001` for local debugging.

Local Nginx test URLs:

```text
http://localhost
http://localhost/health
http://localhost/admin/login
```

HTTPS is not configured yet. This is local HTTP reverse proxy support only.

## גישת מנהל

סיסמת המנהל מגיעה ממשתנה הסביבה:

```text
ADMIN_PASSWORD
```

יש ערך דמו מקומי:

```text
admin123
```

הערך הזה מתאים לפיתוח והדגמה בלבד. בפרויקט אמיתי סיסמה אמיתית צריכה להיות בקובץ `.env` מקומי או ב-GitHub Secrets, ולא בתוך הקוד.

## מצב הפרויקט הנוכחי

מה שכבר הושלם:

- אפליקציית Flask.
- מודלים של MySQL עם SQLAlchemy.
- עמוד בית עם משחקים.
- עמוד פרטי משחק.
- יצירת הזמנה.
- ניהול וביטול הזמנה.
- התחברות מנהל.
- עמוד מנהל עם הזמנות וסטטיסטיקות.
- עמוד about.
- `/health`.
- Dockerfile.
- Docker Compose מקומי.
- Docker Compose בסגנון production.
- GitHub Actions.
- Pytest.
- Docker image build.
- Push ל-Docker Hub.
- שימוש במשתני סביבה.
- `.env.example`.

## Planned / Next Steps

שלבים מתוכננים להמשך:

- הוספת Nginx כ-reverse proxy לפני Flask.
- פריסה ל-AWS EC2.
- הגדרת Security Groups ב-AWS.
- הוספת health checks בסביבת deployment.
- הוספת monitoring בסיסי.
- אופציונלי: Prometheus ו-Grafana.
- אופציונלי: כלי DevSecOps כמו Gitleaks, Bandit, pip-audit, Trivy ו-Hadolint.
- Terraform רק בהמשך, אחרי שהפריסה ל-AWS תהיה מובנת וברורה.

## הערות להגנה על הפרויקט

### למה Flask?

Flask פשוט, קל להבנה ומתאים לאפליקציית דמו קטנה. המטרה כאן היא DevOps, לא framework מורכב.

### למה MySQL?

MySQL הוא מסד נתונים נפוץ בעולם האמיתי, והוא מתאים להדגמת עבודה עם container נפרד למסד נתונים.

### למה SQLAlchemy?

SQLAlchemy מאפשר לעבוד עם טבלאות דרך מחלקות Python, במקום לכתוב SQL ידני בכל פעולה.

### למה ארבע טבלאות?

כי יש ישויות שונות: אצטדיונים, משחקים, סוגי מושבים והזמנות. ההפרדה יוצרת מבנה מסודר עם קשרים ברורים.

### למה Docker?

Docker מאפשר להריץ את האפליקציה בצורה אחידה בכל מחשב או שרת, עם אותן תלויות.

### למה Docker Compose?

כי יש יותר משירות אחד: Flask ו-MySQL. Docker Compose מריץ אותם יחד בפקודה אחת.

### למה GitHub Actions?

כדי להריץ בדיקות ובניית image אוטומטית בכל push, כחלק מתהליך CI/CD.

### למה SQLite בבדיקות?

SQLite בזיכרון מהיר ופשוט. הוא מאפשר להריץ pytest בלי להפעיל MySQL ב-GitHub Actions.

### למה להשתמש ב-`.env` ו-GitHub Secrets?

כדי לא לשמור סיסמאות, tokens או מפתחות בתוך הקוד. זה עיקרון בסיסי באבטחת DevOps.

</div>
