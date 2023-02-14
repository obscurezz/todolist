# TODOLIST for SKYPRO
[akopylov.ga](http://akopylov.ga)

***

# Stack

* __Backend__: python3.10 + django4.1.4
* __DB__: postgres15.1
* __Frontend__: Angular (carefully provided by Skypro team)
* __Deployment__: Docker

## Product contains:

* *Goal - allows you to create, prioritize and sort your tasks*
* *Category - allows you to organize your goals by their meanings*
* *Board - allows you to create categories and goals in it and share them with another users*

### And also:

* *VK auth - allows you to authorize into the app by your VK*
* *Telegram bot @todolist-obscure - allows you to manage your goals via Telegram*

***

# Local initialization

1. Install Docker
2. Copy this repository `git clone https://github.com/obscurezz/todolist`
3. Set up your environment via __.env__ file (you can use .testenv as example) and set env `export $(cat .env | xargs)`
4. Run this command to build and up application `docker-compose up -d --build`
5. Frontend will be available at `http://127.0.0.1`, backend at `http://127.0.0.1:8000`

> How to create your own VK app? Use [https://dev.vk.com](https://dev.vk.com)
> 
> In your environment variables should be:
> * VK_OAUTH2_KEY - your VK app ID
> * VK_OAUTH2_SECRET - your VK app secure key

***

## Tests

* Application is covered by pytest, you can find them in `skypro\tests`
* To test the app run `pytest` from skypro directory
* Current tests are successful
