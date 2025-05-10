# gamer-journey
Web app for tracking/rating games played

## Features Outline
- User profiles with a diary and wishlist
- Diary
  - Collection of games a user has played
  - Games in diary have rating, completion/done playing date, platform played on, hours played, if completed, etc.
  - User can manually edit or remove entries from diary
  - Stat about diary should be generated upon request
    - Total hours played
    - Favorite platform
    - Favorite genre?
    - etc. 
- Wishlist
  - Collection of games a user wants to play
  - Games in wishlist only have a name
  - Games added to user diary should be removed from their wishlist
  - User can also manually remove games from wishlist
- User
  - User should be properly authenticated when logged in
- API
  - Web app will utilize `https://www.igdb.com/api` for gathering information about games that are played or added to wishlist 
    
