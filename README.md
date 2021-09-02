# My Games

## [Live](https://my-fav-games.herokuapp.com/)

This website allows users once logged in to search for video games and add them to their "likes". A user can also visit a videogames page to see what similar games there are to find new games to play.

## Features

-   The search page to allow users to find the games they want.
-   Separation by platform for users who play using specific mediums.
-   Homepage to display all of a users current likes for easy access.

## How it works

-   A user creates an account with a unique username and email (I do not send anything to your email).
-   The user searches for a specific title.
-   The app then accesses the giant bomb api with whatever the user's query was.
-   Then the results are returned and displayed on the page with a like option for every game to add the game to a user's likes.
-   When a game is liked if it is not already in the database it is then stored in our database.
-   When a user visits a videogame's page the same thing happens if it is not already in our database then the information is stored and then displayed to the user.
-   At the bottom of all game display pages there is a list of up to 5 video games similar to the one displayed this information comes from the tastedive api which is accessed on each game page.
-   The api and route handling is coded using Python and Flask. Handling of the api calls and data is done using JavaScript. The database is a PostgreSQL database.

## Tech

Python / JavaScript / Flask / PostgreSQL / CSS / HTML

## External APIs

-   Created using the [Giant Bomb api](https://www.giantbomb.com/api/) to retrieve the video game information and the [Taste Dive api](https://tastedive.com/read/api) to find the similar games.

## API Structure

![Api diagram](/Photos/API_Structure.png)

## Screenshots

### Landing

![Screenshot 1](/Photos/Landing.png)

### Sign up

![Screenshot 2](/Photos/signup.png)

### Login

![Screenshot 3](/Photos/login.png)

### Successful Login

![Screenshot 4](/Photos/After-login.png)

### Search

![Screenshot 5](/Photos/search.png)

### Search Results

![Screenshot 6](/Photos/results.png)

### Game Display

![Screenshot 7](/Photos/game-page.png)

### User Likes

![Screenshot 8](/Photos/user-likes.png)
