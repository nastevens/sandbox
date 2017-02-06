import Bookmarks exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)

main =
  let
    bookmarks = renderBookmarks myBookmarks
  in
    dl
      []
      ((dt [] [ text "Title" ]) :: (List.map (dd []) (wrapList bookmarks)))

-- Wrap each item in a list in its own list
wrapList : List a -> List (List a)
wrapList list =
  List.map (\x -> [ x ]) list

renderBookmarks : List Bookmark -> List (Html a)
renderBookmarks bookmarks =
  List.map renderBookmark bookmarks

renderBookmark : Bookmark -> Html a
renderBookmark bookmark =
  case bookmark of
    Plain url title ->
      a [ href url ] [ text title ]
    Github repo ->
      a [ href ("https://github.com/" ++ repo) ] [ text repo ]
