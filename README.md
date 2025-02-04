# Web platform for the purchasing collective in Youville

**this is a work in progress**

Platform written in python django for a community-driven group to organize bulk grocery orders directly from a food distributor. The workflow goes something like this:

1. build bulk grocery lists from a large list of available items
2. collect orders from members for purchases of various items from the list in step 1
3. allowing members to take on various tasks associated with weekly bulk purchasing

# dev

Built to run using `docker compose`, so `git clone` the repo and launch a local instance of the stack using:

```
docker compose -f docker-compose.dev.yml up --build -d
docker compose -f docker-compose.dev.yml exec -ti web python3 manage.py makemigrations
docker compose -f docker-compose.dev.yml exec -ti web python3 manage.py migrate
# optionally create an admin user
docker compose -f docker-compose.dev.yml exec -ti web python3 manage.py createsuperuser
```

You should have a hydrated DB and working dev instance.
