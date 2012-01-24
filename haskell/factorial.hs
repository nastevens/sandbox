module Main where

    factorial_with_guard :: Integer -> Integer
    factorial_with_guard x
        | x > 1 = x * factorial_with_guard (x - 1)
        | otherwise = 1

    factorial :: Integer -> Integer
    factorial 0 = 1
    factorial x = x * factorial (x - 1)
