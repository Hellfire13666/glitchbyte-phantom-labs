package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestInspect(t *testing.T) {
	s := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		w.WriteHeader(http.StatusAccepted)
	}))
	defer s.Close()
	r := inspect(s.URL, 3*time.Second)
	if r.Error != "" || r.Status != http.StatusAccepted || r.SecurityHeaders["X-Content-Type-Options"] != "nosniff" {
		t.Fatalf("unexpected result: %+v", r)
	}
}
func TestInvalidURL(t *testing.T) {
	r := inspect("file:///etc/passwd", time.Second)
	if r.Error == "" {
		t.Fatal("expected error")
	}
}
