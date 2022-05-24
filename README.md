# Post-API

RESTful flask app with Elasticsearch for vacansy task.

## Installing / Getting started

```shell
git clone https://github.com/Equwece/post-api
cd post-api
```

Put posts.csv to post-api/app/ folder.

```shell
docker-compose build
docker-compose up -d
```

First API request may take about ten seconds, it is ok - posts.csv imports to Elasticsearch.

To search through posts request GET http://localhost:5000/search?q=query

To get post by its uuid request GET http://localhost:5000/post/uuid 

To delete post by its uuid request DELETE http://localhost:5000/post/uuid 

## Links

- Repository: https://github.com/Equwece/post-api
- Website: https://victorkuznetsov.net/
- E-mail: me@victorkuznetsov.net

## Licensing

The code in this project is licensed under GPL3 license.
