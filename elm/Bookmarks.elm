module Bookmarks exposing (..)

type alias Url = String
type alias Title = String
type alias Repo = String
type Bookmark
  = Plain Url Title
  | Github Repo

myBookmarks : List Bookmark
myBookmarks =
  [ Plain "https://www.google.com" "Google"
  , Github "rust-embedded/fixedvec-rs"
  ]
