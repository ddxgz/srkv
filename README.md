# A really Simple Remote Key-Value Store

For the purpose of learning Golang. The skv.go is forked from
[rapidloop](https://github.com/rapidloop/skv), which is built on [BoltDB](https://github.com/boltdb/bolt).


## Usage
The kv store will listen on `0.0.0.0:8080`. It supports `PUT`, `GET` and `DELETE` currently, use corresponding HTTP verb to operate the data.

To put a value to a key, just:

PUT `/key`
```
value
```


To get a value from a key, just:

GET `/key`


To get a key-value pair, just:

DELETE `/key`
