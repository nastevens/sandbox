proc yes(question: string): bool =
    echo(question, " (y/n)")
    while(true):
        case (readLine(stdin))
        of "y", "Y", "yes", "YES": return true
        of "n", "N", "no", "NO": return false
        else: echo("Please enter \"yes\" or \"no\"")

type
    TDirections = enum north, west, south, east
    TSet = set[TDirections]
    TPerson = tuple[name: string, age: int]
    PPerson = ref TPerson

var
    x*: seq[int]
    person: TPerson
    pp: PPerson

type
    TCallback = proc (x: int)

proc echoItem(x: int) = echo(x)

proc forEach(callback: TCallback) =
    const
        data = [2, 4, 7, 11, 15]
    for d in items(data):
        callback(d)

forEach(echoItem)


when isMainModule:
    discard


x = @[1, 2, 3, 4, 5]
person = ("Peter", 10)
(name, age) = person
new(pp)

proc myWriteLn(f: TFile, a: varargs[string, `$`]) =

if yes("Are you an geek?"):
    echo("Good of you to admit it")
else:
    echo("Then why are you running this program?")
