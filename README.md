# Technology discussion Board Back-End
It is the Back-End for a technology discussion related Application. Any front-End such as Mobile can consume this. I will create a front-End consumer soon. Right nowm, one can signup by creating an user. They can add profile image. Then they can login to do all the activities. An authenticated user create Posts and write comments. View, update, delete of comments and posts are supported.

Used frameworks and technologies in this project are: 

- To create REST APIs, Django Rest Framework 3.12.2 is used.
- For Database, PostGres Database is Used.
- For authentication, DRF's Token Based authentication is used.

Supported Endpoints right now:
### Acquire Authentication
Most of the Endpoints require Authentication in the Back-End to create a successful request. In this project, a Token based authentication is implemented.
To acquire authentication, you need a valid user credentials (username and password). First create a user via calling the user creation API in the user section. Then
call this endpoint with a valid payload:

http://localhost:8000/users/

Sample payload: 
```javascript
{
   "username": "test-username",
   "password": "my-password",
}
```
You will receive a token in the response. Now add this token in the following payload format in the header to make an authenticated request. For Postman, select Auth->API auth, and then put the key and the value. 

Authentication Header payload format:
```javascript
{
   "Authorization": "Token your-token-value"
}
```
### User
- User creation(POST) : http://localhost:8000/users/

Provide username, email, firstname (optional), last name(optional) , password to create a new user. Does not require authentication.

sample payload: 
```javascript
{
   "username": "test-username",
   "email": "test@test.com"
   "password": "my-password",
   "first_name": "test-firstname",
   "lastname": "test-lastname"
}
```
- User update(PUT) : http://localhost:8000/users/user-id/

Update firstname, lastname, image id (image needs to be uploaded before referencing image here, then it will work as profile image). Image id has to be unique, means
this image(image with this primary key) should not be assigned to any other user's profile. If an image is assigned to another user, then choose any other image. Usually
after you upload a new image, you will get a new image id. A new ID will always work. Requires authentication. User can only update his information.


sample payload: 
```javascript
{
   "image": "2"
   "first_name": "test-firstname",
   "lastname": "test-lastname"
}
```
- User detail(GET): http://localhost:8000/users/user-id/

Get User's full profile with profile image. Requires Authentication, only logged in User can view his information.

### Image
CRUD(GET,DELETE,UPDATE,VIEW) endpoint: http://localhost:8000/images/
When viewing specific image details or delete or updating, pass image id. Authentication will be added soon.

sample payload: 
```javascript
{
   "image": image-file
   "name": "test-imagename"
}
```

Sample response:
```javascript
{
    "pk": 6,
    "name": "another image",
    "image": {
        "thumbnail": "http://127.0.0.1:8000/media/__sized__/images/xray_enc_xor_image-thumbnail-100x100.png",
        "full_size": "http://127.0.0.1:8000/media/images/xray_enc_xor_image.png"
    }
}
```

### Post

- Post Creation and Lists (POST, GET):http://localhost:8000/posts/

Provide title and description to create a post. Requires authentication, refer to Authentication section, how to provide authentication. Posts will bre created under
the logged in User.

Sample payload to create post: 
```javascript
{
   "title": "post title"
   "description": "this is description"
}
```
- Post Listing of logged in User (GET):http://localhost:8000/posts/

Get a list of posts created by the logged in User. Requires authentication.

- Post details and update Endpoint (PUT, DELETE):http://localhost:8000/posts/post-id/

### Comment
- Comment Creation and List of all comments by an user (POST, GET):http://localhost:8000/comments/

Provide post id and comment text as input to create a comment on a particular comment. It will be automatically count the logged in user as author of the comment. Only an
user can see his all comments.
Sample payload to create comment: 

```javascript
{
   "post": "4"
   "comment_text": "This is a test comment"
}
```
- Comment details, update, delete Endpoint (GET, PUT, DELETE):http://localhost:8000/comments/comment-id/

To edit a comment just provide the comment text. Post to which the comment was posted, cannot be changed.

- Get all comments of a post (GET): http://localhost:8000/comments-by-post/post-id/
