# A really Simple Remote Key-Value Store

For the purpose of learning Golang. The skv.go is forked from
[rapidloop](https://github.com/rapidloop/skv), which is built on [BoltDB](https://github.com/boltdb/bolt). The error handling part refered from (https://elithrar.github.io/article/http-handler-error-handling-revisited/).


## Usage
The kv store will listen on `0.0.0.0:8080/kv`. It supports `PUT`, `GET` and `DELETE` currently, use corresponding HTTP verb to operate the data.

To put a value to a key, just:

PUT `/kv/key` with: `value`


```shell
curl -XPUT http://localhost:8080/kv/key -d "value"
```

To get a value from a key:

GET `/kv/key`

```shell
curl -XGET http://localhost:8080/kv/key
```

To get a key-value pair:

DELETE `/kv/key`
```shell
curl -xDELETE http://localhost:8080/kv/key
```
