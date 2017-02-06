import Html exposing (..)

type Msg = None

staticView : Html x
staticView =
  div [] [ text "Hello, my name is" ]

main =
  div
    []
    [ staticView ]
