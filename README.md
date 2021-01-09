# Technology discussion Board Back-End
This project is created to learn about DRF, PostGres database, Image, Testing in python.

Supported Endpoints right now:
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
after you upload a new image, you will get a new image id. A new ID will always work. Authentication will be added soon.


sample payload: 
```javascript
{
   "image": "2"
   "first_name": "test-firstname",
   "lastname": "test-lastname"
}
```
- User detail(GET): http://localhost:8000/users/user-id/

Get User's full profile with profile image. Authentication will be added soon.

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
