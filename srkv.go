package main

import (
	"ddxgz/accountmanager/skv"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func allkvHandler(env *Env, w http.ResponseWriter, r *http.Request) error {

	switch r.Method {
	case "GET":
		// allkv := make(map[string][]byte, 20)
		var value []byte

		err := env.Store.Get(r.URL.Path[1:], &value)
		if err != nil {
			log.Println("error when get:", err)
			return StatusError{404, err}
			// http.Error(w, http.StatusText(http.StatusInternalServerError),
			// 	http.StatusInternalServerError)
			// fmt.Fprintf(w, "Hi, the key: %s does not exist", r.URL.Path[1:])
		}
		fmt.Fprintf(w, "Hi, you get: %s with value: %s", r.URL.Path[1:], value)
		// default:
		// 	fmt.Fprintf(w, "Hi, you request: %s", r.URL.Path[1:])
	default:
		fmt.Fprintf(w, "Hi, upsupported method for: %s", r.URL.Path[1:])
	}
	return nil
}

func kvHandler(env *Env, w http.ResponseWriter, r *http.Request) error {

	switch r.Method {
	case "PUT":
		// put: encodes value with gob and updates the boltdb
		key := r.URL.Path[1:]
		// body := r.Body
		value, err := ioutil.ReadAll(r.Body)
		if err != nil {
			log.Println("error when read put body:", err)
			return StatusError{400, err}
		}
		err = env.Store.Put(key, value)
		if err != nil {
			log.Println("error when put:", err)
			return StatusError{400, err}
		}
		// log.Println("put: ", sessionId, " with: ", info)
		fmt.Fprintf(w, "Hi, you put: %s with value: %s", r.URL.Path[1:], value)

	case "GET":
		var value []byte
		err := env.Store.Get(r.URL.Path[1:], &value)
		if err != nil {
			log.Println("error when get:", err)
			return StatusError{404, err}
			// http.Error(w, http.StatusText(http.StatusInternalServerError),
			// 	http.StatusInternalServerError)
			// fmt.Fprintf(w, "Hi, the key: %s does not exist", r.URL.Path[1:])
		}
		fmt.Fprintf(w, "Hi, you get: %s with value: %s", r.URL.Path[1:], value)
		// default:
		// 	fmt.Fprintf(w, "Hi, you request: %s", r.URL.Path[1:])
	case "DELETE":
		key := r.URL.Path[1:]

		err := env.Store.Delete(key)
		if err != nil {
			log.Println("error when delete:", err)
			return StatusError{400, err}
		}
		// log.Println("put: ", sessionId, " with: ", info)
		fmt.Fprintf(w, "Hi, deleted the key: %s", r.URL.Path[1:])
	default:
		fmt.Fprintf(w, "Hi, upsupported method for: %s", r.URL.Path[1:])
	}
	return nil
}

func (h Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	err := h.H(h.Env, w, r)
	if err != nil {
		switch e := err.(type) {
		case Error:
			// We can retrieve the status here and write out a specific
			// HTTP status code.
			log.Printf("HTTP %d - %s", e.Status(), e)
			http.Error(w, e.Error(), e.Status())
		default:
			// Any error types we don't specifically look out for default
			// to serving a HTTP 500
			http.Error(w, http.StatusText(http.StatusInternalServerError),
				http.StatusInternalServerError)
		}
	}
}

type Env struct {
	Store *skv.KVStore
}

type Handler struct {
	*Env
	H func(env *Env, w http.ResponseWriter, r *http.Request) error
}

// Error represents a handler error. It provides methods for a HTTP status
// code and embeds the built-in error interface.
type Error interface {
	error
	Status() int
}

// StatusError represents an error with an associated HTTP status code.
type StatusError struct {
	Code int
	Err  error
}

// Allows StatusError to satisfy the error interface.
func (se StatusError) Error() string {
	return se.Err.Error()
}

// Returns our HTTP status code.
func (se StatusError) Status() int {
	return se.Code
}

func main() {
	// open the store
	log.Println("Opening store...")
	// the db file cannot be located at a shared folder
	kvstore, err := skv.Open("/home/vagrant/accountmanager/bolt.db")
	if err != nil {
		log.Fatal("open error:", err)
	}
	log.Println("Store opened")
	defer kvstore.Close()

	// err = kvstore.Put("k1", "info1")
	// if err != nil {
	// 	log.Fatal("put error:", err)
	// }

	env := &Env{kvstore}

	// http.HandleFunc("/kv/", kvHandler)
	http.Handle("/kv/", Handler{env, kvHandler})
	// http.Handle("/all/kv", Handler{env, allkvHandler})
	log.Fatal(http.ListenAndServe("0.0.0.0:8080", nil))

}
