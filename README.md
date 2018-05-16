# kaist-cs101-extract-code

## Setup

To use this project, follow the instructions below.

### Install Python 3

You need Python 3 installed on your environment to use this project.

### Setup venv

Setup venv to use this project.

```
$ python3 -m venv ./env
```

To activate, use the command below.

Linux/Mac:
```
$ source ./env/bin/activate
```

Windows:
```
> env/Scripts/activate.bat
```

### Install dependent Python libraries

Use pip to install libraries.

```
$ pip3 install -r requirements.txt
```

## Extract submitted user code

### Prepare "config.py"

Prepare `kaist-cs101-extract-code/config.py` file that includes 
information on target exercises to extract user code.

Copy example config file first. 
```
$ cp config.example.py config.py
```

Modify the values according to the comments in the file.
```python
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
```

### Run "extract_code.py"

Run `extract_code.py` to extract code from the users

```
(env)$ python extract_code.py
```

### Result files

Result files are saved in `/data` directory with 
a filename `{exercise_id}_{exercise_title}_code.json`
in a following format.

```
[
  {
    'user_id': <ELICE USER ID>, 
    'firstname': <FIRST NAME>, 
    'lastname': <LAST NAME>, 
    'organization_uid': <STUDENT ID>, 
    'code': <CODE>,
    'code_update_datetime': <CODE_UPDATE>
  },
  ...
]
```

where `<CODE>` is in a following format. 
It is `null` if student never submitted the code before the due datetime.

```
{
  <FILE 1 PATH>: <FILE 1 CONTENT>,
  <FILE 2 PATH>: <FILE 2 CONTENT>,
  ...
}
```

where `<FILE N CONTENT>` is a string value, 
or `null` if the student never opened up the file.