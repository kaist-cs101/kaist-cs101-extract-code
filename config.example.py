
# Organization id for target exercises. Find this in url. https://{id}.elice.io
# (e.g. 'kaist' for https://kaist.elice.io)
organization = 'kaist' 

# Email for logging in.
email = 'jmbyun91@gmail.com'

# Paths for target exercises, 
# in "/courses/{digits}/lectures/{digits}/materials/{digits}" form.
target_paths = [
    '/courses/262/lectures/2140/materials/2',
    '/courses/262/lectures/2140/materials/3'
]

# Due datetime for target exercises,
# in "YYYY-MM-DD HH:MM" form, where HH is hours is value >= 0 and < 24.
# The application will extract the code from the latest submission that was
# done before the due datetime.
due_datetime = '2018-04-04 23:59'
