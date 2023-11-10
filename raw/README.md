# Raw Data Folder

Here files that are downloaded from []() can be placed so they can e automatically processed.

## Steps to Download Raw Data

1. Go to [NOAA's Local Climatological Data Tool](https://www.ncdc.noaa.gov/cdo-web/datatools/lcd).
2. Here you can find the weather station with several different filtering tools. Most commonly, the `State` filter is used.
3. Select your desired State.
4. A list of weather stations in that State should come up.
   - If there are several stations for your desired location, it's best practice to use the station with the longer `Period of Record`.
   - It is also possible to view the stations' WBAN number in the list. This can be helpful if you are matching [ASHRAE Climatic Design Conditions](http://ashrae-meteo.info/v2.0/).
5. Once you have found your desired station, click `Add to Cart`
6. Scroll to the top of the page and click on your cart.
7. Choose `LCD CSV` from the `Output Format`.
8. Select your desired date range
   - There is a limit of a maximum of 10 years
   - Normally 10 years ending at the beginning of the current year is selected.
9. Select `Continue`
10. Enter your email address so you can be notified when the data is ready to be downloaded.
11. Select `Submit Order`
12. Once the data is collected, you will receive and email with a download link. That link should download a `.csv` file with the name being the order number. This is the file that can be uploaded into this raw data folder.
