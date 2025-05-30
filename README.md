# MovieBase

MovieBase is designed for film enthusiasts who want to discover, review, and discuss movies. It serves as a community-driven platform where users can explore a curated list of movies, submit ratings, and leave comments. The platform is tailored for both casual viewers and dedicated movie critics who wish to engage in discussion, rate films, and share their opinions. The admin acts a curator who decides what type of movies will be added, they might want to focus on a niche subject within movies or have a theme depending on the time of year. For example, horror movies in October for Halloween, or festive movies in Decemeber for Christmas. The top 25 movies from [IMDB](https://www.imdb.com/chart/top/?ref_=nv_mv_250) have been added to show how it'll look when properly filled.

This site allows users to:

- Browse a selection of movies.
- Submit and edit reviews for films.
- Comment on movies and engage with other users.
- Register and log in to personalise their experience.

![Screenshot of screens](readme-images/mockup.png)

## Features

### Navigation Bar

- Persistent across all pages.
- Provides links to key sections: Movie List, Login/Register, and Logout.
- Fully responsive for seamless navigation across devices.

### Movie List/Home Page

- Displays a curated list of published movies.
- Each movie item links to a detail view.

### Movie Detail Page

- Shows full movie details: title, description, and average rating.
- Includes all user reviews and comments related to that movie.
- Authenticated users can add reviews and comments.

### Rating System

- Users can leave one rating per movie.
- Reviews are rated from 1 to 5 stars.

![Rating System](readme-images/rating.png)

### Comment System

- Users can comment on each movie as many times as they like.
- Edit and delete options for comment authors.
- Modal popup confirmations for deletions.

![Comment section](readme-images/comment.png)
![Edit and Delete](readme-images/edit_delete.png)

### Authentication System

- Registration and login forms for user accounts.
- Secure user authentication and session handling.
- Login required for submitting reviews and comments.

### Responsive Design

- Optimised for mobile, tablet, and desktop screen sizes.
- Clean layout using Bootstrap 5 for consistent styling.

### Admin Panel

- Admin interface for managing movies, reviews, and comments.

### Search Page

- Search feature in navigation bar that can be used for searching keywords which can find movies based on title, genre and description.

![Search Feature](readme-images/search_results.png)

### Footer

- Consistent footer across all pages.
- Has links to 4 social media websites.
- Also shows pagination for movie posts, 9 per page.

![Footer](readme-images/footer.png)

## Planning

Wireframes that were used to plan out the layout and flow between pages.

![Wireframe](readme-images/wireframe.png)

## Database Model Relationships

- Each Movie can have many Reviews and Comments.
- Each Review is written by one User and belongs to one Movie.
- Each Comment is written by one User and belongs to one Movie.

![Model Diagram](readme-images/Model.png)

## Testing

All core features were tested manually and via automated Django tests.

### Forms Tested 
- Registration, Login, Review Submission, Comment Submission, Edit/Delete.

### Views Tested 
- Movie List and Detail views.
- Review and Comment logic for authenticated vs unauthenticated users.

### Django Tests
- 17 unit tests covering GET/POST views and form behavior.
- All tests passed successfully.

### JavaScript
- Modal functionality for editing and deleting comments manually tested.

### Validator Testing
- HTML: No errors using [W3C Validator](https://validator.w3.org/)
- CSS: No errors using [Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/)
- Python: All warnings in VS Code Problems panel resolved.

### Browser & Screen Compatibility
- Verified in Chrome and Edge.
- Display tested on widescreen monitor, laptop, tablet, and phone.

### Deployment

## The project is deployed to Heroku

Deployment Steps:

- Create a new Heroku app.
- Connect Heroku to GitHub repo.
- Set environment variables including DATABASE_URL and SECRET_KEY.
- Add required buildpacks (Python).
- Push code to Github.
- Run python manage.py migrate, createsuperuser, and collectstatic.

[Live Link](https://moviebase-reviewer-9b00ad1bd4d7.herokuapp.com/movies/)

### Credits

- Movie list and descriptions from [IMDB](https://www.imdb.com/chart/top/?ref_=nv_mv_250)
- Fonts from [Google Fonts](https://fonts.google.com/)
- Favicon from [RealFaviconGenerator](https://realfavicongenerator.net/)
- Graphics for project came from [Flat Icon](https://www.flaticon.com/)
- [Code Institute](https://codeinstitute.net/) project 'I Think Therefore I Blog' was used as a starting point, especially the navigation and footer layout.
- Stars for rating from [Font Awesome](https://fontawesome.com/) 
