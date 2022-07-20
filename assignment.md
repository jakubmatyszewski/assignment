Tasks
X Implement assignment using:
    • Language: Python
    • Framework: any framework
X Implement a REST API returning JSON based on the Content-Type header
X Implement a custom user model with a "author pseudonym" field
• Implement a book model. Each book should have a title, description, author (your custom user
model), cover image and price
    • Choose the data type for each field that makes the most sense
• Provide an endpoint to authenticate with the API using username, password and return a JWT
• Implement REST endpoints for the /books resource
    • No authentication required
    • Allows only GET (List/Detail) operations
• Provide REST resources for the authenticated user
    • Implement the typical CRUD operations for this resource
    • Implement an endpoint to unpublish a book (DELETE)
• Implement API tests for all endpoints

Evaluation Criteria
• Python best practices
• If you are using a framework make sure best practices are followed for models, configuration and
tests
• Write API tests for all implemented endpoints
• Make sure that users may only unpublish their own books
• Bonus: Make sure the user Darth Vader is unable to publish his work on Wookie Books

Submitting
Please organise, design, test and document your code as if it were going into production - then push
your changes to an online repository and share the URL with us.

