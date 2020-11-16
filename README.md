# chatBackend
This is an instant messaging API developed in python using Flask framework and its extensions.  API allows creating an account and using it to create chats and add one or more users to them. Protocols used to access API are http and websockets via socket.io library. Idea was to use http to manage user data, chats and authentication, while socket.io was used for its simplicity to send and receive messages in real time. The app has three layers:

The blueprints layer exposes API's interface to the public. Receives requests and uses layers below to make a response.

The services layer manages more complex tasks like user authentication and distributing messages among chat participants

Data access layer communicates with databases. Mysql database has been used to manage user and chat data and dynamodb has been used for messages. Idea was to use sql to keep track of data is not frequently changed like users, and chats. The most recently used ones are cached in memory to reduce the number of requests to sql database, like when authenticating requests and checking if users can write to a particular chat. Dynamodb keeps messages because it is simple to use and fast to write and query messages sorted by time of the write.
