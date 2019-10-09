# DP21-SceneDescriptor

## Install

All that is needed to run the project so far is docker and docker-compose. 


## Running

To run the project, simply run the command:

```
docker-compose up --build 
```

from the root of the project. The api should now be running at the address: localhost:8000.

## API

This is the list of paths and methods which are currently available for the api as of now.
As we do not want spamming, a token is required for most of these paths.
The token is given upon logging into the service


### /auth

These are the paths which mostly have to do with authentication, and meta info used for the rest.

##### /auth/login
[POST] \
req: email, password \
returns: auth_token, user
Logs in the user and returns a token which allows the usage of the api.

##### /auth/register
[POST] \
req: email, username, password
returns: user
Registers the user to the database allowing for login and access to api.


### /tasks

These are the paths for the creation and checking the status of jobs.

##### /tasks
[POST] \
token required \
req: type
returns: task_id
Creates a job and enqueues it to redis. (Type needs to be 0 for this path)

##### /tasks/<task_id>
[GET] \
token required \
req: task_id
returns: task_id, task_status, task_result
Main way to check if a job status and its result by polling this path.


### /urate

These are the paths for everything related to the images and the rating of said images.

##### /urate/images
[POST] \
token required \
req: caption, path
returns: image
Simple way to create image with the path to the image and the caption associated.

[GET] \
token required \
req: X
returns: list of all images
Path to get all images.

##### /urate/images/<image_id>
[GET] \
token required \
req: image_id
returns: image
Path to get the info of an image by its id.

[PATCH] \
token required \
req: image_id, payload(attribute to change)
returns: image
Updates the image with the new params passed.

[DELETE] \
token required \
req: image_id
returns: X
Deletes the image using the image id.

##### /urate/ratings
[POST] \
token required \
req: image_id, user_id, validity, minimalist, distinct_items, details, spatial_info \
returns: rating
Call to create new rating.

##### /urate/ratings/<image_id>/<user_id>
[GET] \
token required \
req: image_id, user_id
returns: rating
Call to get a rating associated between a user and an image.

[PATCH] \
token required \
req: image_id, user_id, payload(attribute to change)
returns: rating
Call to update a rating.

[DELETE] \
token required \
req: image_id, user_id
returns: X
Call to delete a rating.

##### /urate/ratings/<image_id>
[GET] \
token required \
req: image_id
returns: rating[]
Call to get all ratings associated with an image.

##### /urate/ratings/<user_id>
[GET] \
token required \
req: user_id
returns: rating[]
Call to get all ratings associated with a user.

## TODO
- add password support (email & reset)
- add user api
- limit number of images returns in all / have calls for various 
- api for images which a user has not rated yet

Written by: GuyHomme hehe
