#-------------------------------------#
#               LOGIN                 #
#-------------------------------------#



# Yousif navigates to the home page in his browser

# Yousif finds he is redirected to the login page as he is not logged in

# Yousif inputs the correct password and finds he is redirected to the home page


# Marek navigates to the home page in *his* browser

# Because Marek hasn't logged in yet he finds he is immediately redirected to a password screen

# Marek inputs an incorrect password

# Marek sees an error message saying 'incorrect password, 5 attempts remaining'

# Marek puts the incorrect password again 4 more times and each time finds the error message incrementally reducing his remaining attempts by 1 each time until it says 1 attempt remaining

# Marek inputs the incorrect password a 5th time and finds the website is now locked, no password form is visible and it has a message saying 'too many password attempts, an email has been sent to the administartor(s) with a link to unlock TOPAIMS'


# however Yousif is still able to do things as he is already logged in

# coincidentally Yousif decides to close his browser


# when Yousif tries to navigate to the home page he finds he is redirected to the locked password page


# Yousif checks his email and finds that the email has been CCed to Marek, David and Alexander

# Yousif follows the link in his email and finds the password page unlocked


# Marek also finds the password page unlocked

# Both Marek and Yousif enter the correct password and get redirected to the home page


# Yousif is finished with TOPAIMS and closes his browser


#-------------------------------------#
#            JOBS/JOB VIEW            #
#-------------------------------------#

# Marek clicks 'Jobs' on the navbar and is redirected to the jobs page

# sees the plus button and clicks it to create a new job, he is redirected to the new job form

# Marek fills the form with the client's name, contact details, and a few notes then hits 'CREATE' and finds he is redirected to the job view of the newly created job || FORM VALIDATION  || JOB APPEARS IN JOBS VIEW || alert?


#-PROFILE-#

# Marek sees in the top left corner a transparent box with the customer's name, email, phone and the word quote

# Marek clicks the word quote and finds he is redirected to a cloud service where the file is kept and editable DAVID HOW DO YOU WANT THIS ARRANGED

# Marek clicks the dropdown menu and finds three options: quote, ongoing, completed

# Marek clicks on 'ongoing' and finds that after the page has refreshed the box is blue and an alert saying || ICON CHANGES TO BLUE IN JOBS VIEW || SYNCHRONISATION -appears in 'ongoing' section in job view with correct colour scheme 

# Marek then clicks on 'completed' and finds that after the page has refreshed the box shows the completed status || ICON CHANGES TO COMPLETED VIEW IN JOBS VIEW ||SYNCHRONISATION -appears in 'completed' section in job view with correct colour scheme

# Marek has finished testing it out and clicks on 'quote' again and finds the page refreshes and the box is transparent again || ICON CHANGES TO TRANSPARENT AGAIN IN VIEW || SYNCHRONISATION -appears in 'completed' section in job view with correct colour scheme

#- NOTES -#

# Marek wants to sees the notes section in the bottom left corner and decides he wants to add a note

# Marek fills the form in and clicks 'add note', he finds the page refreshes and his note is visible with an alert saying 'note added' || FORM VALIDATION || SYNCHRONISATION -note appears in home page notes/'all' section 

# Marek decides he wants to add a second note, again he fills in the form and clicks 'add note', the page refreshes and both notes are now visible with the 'note added' alert, with the most recent note at the top 


#- SCHEDULE OF ITEMS -# NOTE TO SELF: helper methods: make schedule item, make purchase order, make shopping list item, || Schedule of items is self contained, the only time a schedule of item will appear in the 'needed' is if it isn't a shopping list item or a P.O, as soon as it is, it's status is 'handled' and will not appear in the site management console

# Marek can see the schedule of items as the middle column on the screen

# Marek fully fills the new item form with a date of one month from the current date. He then clicks 'add'. The page refreshes with an alert saying '{{full name}} was successfully scheduled for {{date}}'. He finds the item is in the schedule of items || FORM VALIDATION

# Marek adds another item to the schedule of items

# Marek adds a second item  with a date range where the median of the range is the day after the first scheduled item and finds the page refreshes again with the new item beneath the previous item (chronological order) and an alert that says '{{full name}} was successfully scheduled for {{date}}-{{date}}'

# time passes and now it is 7 days until the first item's scheduled date, Marek now sees the item in the 'needed' category of the site management panel

# even more time passes and now it is 1 day until the first item's scheduled date, Marek now sees the first scheduled item highlighted in green in the schedule of items and the second item is also in the 'needed' category of the site management panel

# Marek decides that actually the first item can wait a few more days so decides to change it's place in the schedule, he clicks on the date, a window appears and he changes the date to make it two days further into the future

# the page refreshes and Marek sees that the re-scheduled item now appears above the second item, is no longer highlighted in green and it's listed date has changed accordingly.

# Marek then decides that the re-scheduled item should come way later, so he changes its date to over a week from the current date. The page refreshes and he finds that it is no longer in the 'needed' section of the site management panel and it's listed date has changed accordingly.

# Finally Marek decides to remove the item from the schedule altogether, he clicks on the delete button and finds he is presented with an 'are you sure' prompt.

# Marek is not sure so clicks cancel and finds he is redirected to the job view

# now Marek is sure he wants to delete he tries again, he finds the same 'are you sure' prompt but this time clicks 'ok'. He finds he is redirected back to the job view with an alert saying 'delete successfull' and the item is no longer in the job schedule.

# after populating the job schedule with another five or six items Marek decides to print the job schedule

# Marek presses the print button and finds that a 'save as' dialogue opens (unit test will test the rest here)


#- SITE MANAGEMENT -# NOTE TO SELF see helper methods above

# Marek sees a scheduled item in the needed column and decides to make a purchase order. He clicks on the purchase order button and finds he is redirected to a purchase order form page

# Marek sees that the purchase order has an item pre-filled in with the fullname, description and job

# Marek fills the rest of the form and clicks create, he is redirected to the job view and finds the item is now in the 'en route' section with the status 'ordered' and showing the expected delivery date. || SYNCHRONISATION -home page delivery section

# Marek sees another scheduled item in the needed column and decides to make it a shopping list item, he clicks the shopping list button and finds he is redirected to a shopping list-form page with the job, desctiption and quantity pre filled in || FORM VALIDATION || SYNCHRONISATION -home page shopping list

# upon clicking 'submit' marek is redirected back to the job view where the new item appears in the 'needed' column as a shopping list item

# Marek now needs to fill out a brand new purchase order so clicks on the P.O tab on site management

# Here he sees a P.O form identical to that on the home page with the job immutable and pre filled

# Marek adds a few items with different arrival dates and clicks submit, the page reloads and he finds the items appear in the 'en-route' section of the site management panel || SYNCHRONISATIONcheck all other P.O locations, home page deliveries etc

# Eventually Marek delivers an 'en-route' item to site, 

#-------------------------------------#
#                JOBS                 #
#-------------------------------------#

# Marek has been using the software for a long time now and quite a lot of data has aggregated, with the software he has completed 2 jobs, 4 jobs are ongoing and he has put out 4 quotes || use real examples, schedule of items etc, full fledged details, notes, everything, this state can also be used for demonstrations

# When the page loads Marek sees all the ongoing jobs

# Marek sees there are three tabs to choose from 'ongoing', 'completed', 'jobs'.

# Marek sees that all the jobs are listed in reverse chronological order in their respective tab/section || POST MVP

# Marek finds that the colour of the ongoing jobs are a deep blue || POST MVP

# Marek sees that the colour of the completed jobs are red || POST MVP

# Marek sees that the colour of the quotes are clear/white || POST MVP

# Marek finds that when he hovers his mouse over a job profile the client's contact details appear || (disable this in client view?) || POST MVP


#-------------------------------------#
#              HOME PAGE              #
#-------------------------------------#

#- Deliveries -#

# When Marek enters the home page he sees all of the the day's deliveries on the far left, by default it displays all the deliveries being expected for 'today'

# Marek sees three tabs on the deliveries panel: 'today', 'this week', 'all'

# Marek clicks 'this week' and all the deliveries for this week are shown
# Marek clicks 'all' and the page refreshes to show every delivery in an unlimited time window
# Marek clicks 'today' and the page refreshes back to the original view || SYNCHRONISATION

# A delivery arrives and Marek sees it is all correct so clicks the 'accept delivery' button
# The page refreshes, the item disappears from the view || SYNCHRONISATION
# The item appears as status 'IN SHOWROOM' in it's en-route panel

# Another delivery arrives but this time Marek sees the item is damaged, he clicks the 'reject delivery' button, a modal pops up with the item rejection form.
# Marek reschedules for another delivery, adds a note and clicks submit, he finds he is redirected to the home page with an alert saying '{{ item description }} rejected' || SYNCHRONISATION || FORM VALIDATION

# Marek checks the 'this week' tab on the delivery items and sees the item rescheduled for the selected date

# Marek now needs to reject another item but does not reschedule, after he is redirected back to the home page he sees that the item does not appear anywhere, a note is left in the job view || SYNCHRONISATION

# POST MVP - Marek clicks on an item and finds he is redirected to the detailed item view
# POST MVP - Marek navigates back to the home page 

#- Shopping List -#

# Marek now checks the shopping list, he can see the items displaying in reverse chronological order

# Marek decides to add a new item to the shopping list, he fills in the form and hits submit, the page refreshes and the new item is at the top

# POST MVP - Marek then looks at an item on the shopping list and decides to make a purchase order from it
# POST MVP - Marek finds the form pre filled with the item's description, quantity and job, Marek clicks create and finds he is redirected back to the home page || VALIDATION

# POST MVP - Marek sees the item no longer on the shopping list

#- Notes -#

# Now Marek is looking at the notes section and sees that the admin notes are displayed by default in reverse chronological order

# Marek clicks the drop down menu and sees two tabs 'admin', 'all'

# Marek clicks 'all', and he can now see all the notes from every job (but not the admin notes) in reverse chronological order

# Marek clicks 'admin' again and finds the page reverts back to the default view

# Marek then decides to add a new note, he fills in the form and clicks add, the page refreshes with the alert 'note successfully added' and the new note appears in 'admin' on the top || FORM VALIDATION

#- Purchase Order -#
# (the code for this and purchase order form page are taken from the same place see there for more detailed testing)

# Marek needs to fill out a new purchase order, he sees that the order number is already pre-filled in and immutable

# Marek fills out item A to be delivered to the shop for job A for the same day
# Marek fills out item B to be delivered to site for job B
# Marek fills out item C to be delivered to the shop for job A for later on in the week
# Marek fills out item D to be delivered to the shop for job A two weeks time

# Marek clicks create and finds the page refreshes with item A appearing in the deliveries deliveries list
# Marek looks at the 'this week' section of the deliveries and sees item C appearing in the deliveries list
# Marek then looks at the 'all' section of the deliveries and sees item D appearing in the deliveries list 

#-------------------------------------#
#            CLIENT VIEW              #
#-------------------------------------#

#-------------------------------------#
#         DETAILED ITEM VIEW          #
#-------------------------------------#

#-------------------------------------#
#     DEDICATED SHOPPING LIST PAGE    #
#-------------------------------------#

# Marek navigates to the dedicated shopping list and finds all the shopping list items from every job

# on every shopping list item Marek sees description | quantity | job | acquired

# when Marek clicks acquired the item disappears from the shopping list - an alert saying 'x marked as aquired' appears - the item appears as 'acquired' in the 'en route' section of whichever job 

# at the bottom of the page marek sees an 'add shopping list item form'
	# fields: 
	# description
	# quantity
	# job

# when marek fills in the form and submits, the shopping list item appears at the top of the shopping list and in the 'needed items' section of the job view

# on every shopping list item Marek sees description | quantity | job | acquired

# when Marek clicks acquired the item disappears from the shopping list - an alert saying 'x marked as aquired' appears - the item appears as 'acquired' in the 'en route' section of whichever job 


#-------------------------------------#
#       ITEM REJECTION FORM PAGE      #
#-------------------------------------#

#-------------------------------------#
#          SYNCHRONISATIONS           #
#-------------------------------------#

# this section makes sure that when item's statuses are changed or added in different places they update correctly everywhere

# helper method for checking synchronicity of synchronised item at every one of it's synchronization points for every synchronised item
# trigger every synchronization point for every permutation and run synchronicity test each time.





#-------------------------------------#
#               SNAGGING              #
#-------------------------------------#
# I'm pretty sure I've missed a few alerts to be tested here, go over the original spec document and search for 'alert', see if anything is missed.

# Items need to have a date instantiated field so they show chronologically (shopping list items should display in reverse chronological order, can do this with pk though?)

# need to have the ability to delete anything (notes, items etc.)

# add categories of items to the supply schedule

# Category for supply only stuff or just things arriving for the office

# standalone delivery item that doesn't sync to anything?

# delivery date being a range of dates not exact date

# DEFINITELY  refractor with ajax so whole pages aren't reloading every time

#-------------------------------------#
#            POST PRODUCTION          #
#-------------------------------------#
"""

1. Same adress multiple jobs (perhaps instead of being job profiles you have adress profiles? you click and it has a merged schedule of items with merged quote, with a merged site management panel)

2. In the home page when viewing 'all' notes add option to add a note to a job directly from the home page/all tab

3. P.O items being delivered to site and not shop appearing in 'DELIVERIES' section