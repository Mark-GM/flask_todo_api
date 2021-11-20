# flask RESTful todo api
----------
1. Get all Todo tasks 
```HTTP
GET /api/v1/todos/
```
2. Add a new task
```HTTP
POST /api/v1/todos/
```
3. Get a task by id
```HTTP
GET /api/v1/todos/<int:id>/
```
4. Update a task
```HTTP
PATCH /api/v1/todos/<int:id>/
```
5. Delete a task
```HTTP
DELETE /api/v1/todos/<int:id>/
```