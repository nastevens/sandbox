#This is a comment
let name = readLine(stdin)
case name
of "":
    echo("No name")
of "name":
    echo("haha")
of "Bill", "Steve", "Linus":
    echo("I know a famous ", name, "...")
else:
    echo("Hi, ", name, "!")

