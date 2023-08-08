## Notes

* Decided to limit mulitthreading and multiprocessing to users that login only and have access so it's limited. 
  * Make api v2 for this
* Need to implement a way to fetch a small batch of emails when first logging into the service (maybe 40-60 emails) 
after receiving the first batch, I would like to display it while the rest of the emails are fetched in the background.
    * Perhaps for the first batch we pull the full data while the rest we only pull minimal data and only pull the body 
  the emails gets selected (this might have better performance as to what it is now)
    * Need to fine tune the batch number based on WI-FI connection, strong, medium, weak
    * Add additional api route that passes in the currently received email_ids for another way to implement pagination
* Another way to improve the pagination is that I could take a note from gmail and outlook... outlook seems to
  initially get a certain number of emails then once you scroll far down enough they fetch more emails to display.
  Googles approach is basically the same besides the fact that they use different pages instead of scrolling down
  * From these two takes I kind of prefer the outlook approach since the user won't have to think about loading
  to the next page, although if this is too slow for slower internets I can also have the other version.
  * When implementing the scrolling version I might be able to check where the user is at the screen and once they get
  to the last few emails we start making the api call to fetch more emails 


