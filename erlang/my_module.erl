%% A simple Erlang module

-module(my_module).
-export([pie/0, print/1, either_or_both/2, yesno/1]).

pie() ->
    3.14.

print(Term) ->
    io:format("The value of Term is: ~w.~n", [Term]).

either_or_both(true, B) when is_boolean(B) ->
    true;
either_or_both(A, true) when is_boolean(A) ->
    true;
either_or_both(false, false) ->
    false.

yesno(F) ->
    case F(true, false) of
        true  -> io:format("yes~n");
        false -> io:format("no~n")
    end.
