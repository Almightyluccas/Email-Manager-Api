## Notes

* Need to implement a way to fetch a small batch of emails when first logging into the service (maybe 40-60 emails) 
after receiving the first batch, I would like to display it while the rest of the emails are fetched in the background.
    * Perhaps for the first batch we pull the full data while the rest we only pull minimal data and only pull the body 
  the emails gets selected (this might have better performance as to what it is now)
    * Need to fine tune the batch number based on wifi connection, strong, medium, weak